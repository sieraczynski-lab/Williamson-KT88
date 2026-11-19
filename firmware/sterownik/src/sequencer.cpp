#include "sequencer.h"

#include <Arduino.h>
#include <esp_attr.h>
#include <esp_system.h>
#include <esp_task_wdt.h>
#include <sys/time.h>

#include <algorithm>
#include <atomic>
#include <cmath>

#include "commands.h"
#include "config.h"
#include "console.h"
#include "relays.h"
#include "selector.h"
#include "settings.h"
#include "state.h"

namespace sequencer {
namespace {

// Pamiec RTC przezywa reset programowy i watchdog, ginie przy zaniku zasilania.
constexpr uint32_t RTC_MAGIC = 0x4B543838;  // "KT88"
struct RtcMem {
  uint32_t magic;
  int64_t lastHeatUs;  // ostatnia chwila z wlaczonym zarzeniem (zegar systemowy)
  uint8_t wasOn;       // reset w trakcie pracy -> wznowienie
  uint8_t resumeCount;
};
RTC_NOINIT_ATTR RtcMem s_rtc;

Phase s_phase = Phase::STANDBY;
uint32_t s_phaseT0 = 0;
uint32_t s_stepT0 = 0;
uint8_t s_step = 0;

uint32_t s_warmupMs = cfg::WARMUP_MS;
uint32_t s_stableSince = 0;
bool s_trigStart = false;
bool s_fromModeSwitch = false;
bool s_modeTarget = false;
uint8_t s_unmuteTarget = cfg::ATT_MAX;
uint8_t s_rampCode = cfg::ATT_MAX;

uint8_t s_input = 0;
uint8_t s_att = cfg::ATT_MAX;
bool s_userMute = false;
bool s_transientMute = false;
bool s_soundEnabled = false;  // faza pozwala grac
bool s_soundOut = false;      // ostatnio wyslane do K11
bool s_triode = false;
bool s_spkLamp = false;
bool s_trigger = false;
bool s_service = false;

Fault s_fault = Fault::NONE;
int8_t s_faultTube = -1;
std::atomic<uint8_t> s_pendingFault{0};
volatile int8_t s_pendingTube = -1;
volatile float s_pendingValue = 0;

uint32_t s_lastSecond = 0;
uint32_t s_lastHoursSave = 0;
uint32_t s_lastSelectorProbe = 0;
bool s_hoursDirty = false;

int64_t nowUs() {
  timeval tv;
  gettimeofday(&tv, nullptr);
  return (int64_t)tv.tv_sec * 1000000 + tv.tv_usec;
}

bool powered(Phase p) { return p >= Phase::MAINS && p <= Phase::MODE_SWITCH; }

void enter(Phase p) {
  s_phase = p;
  s_phaseT0 = s_stepT0 = millis();
  s_step = 0;
  console::logf("faza: %s", phaseName(p));
}

// czeka, nie wyzwalajac watchdoga (przelaczanie wejsc i kolumn)
void waitMs(uint32_t ms) {
  while (ms) {
    uint32_t d = std::min<uint32_t>(ms, 100);
    vTaskDelay(pdMS_TO_TICKS(d));
    esp_task_wdt_reset();
    ms -= d;
  }
}

uint8_t minAttFor(uint8_t input) { return settings::get().in[input].minAtt; }

// tlumienie widoczne dla uzytkownika -> kod drabinki (korekta poziomu wejscia)
uint8_t codeFor(uint8_t att) {
  int code = (int)att - settings::get().in[s_input].trim;
  return (uint8_t)std::clamp(code, 0, (int)cfg::ATT_MAX);
}

void applySound(bool force = false) {
  const bool want = s_soundEnabled && !s_userMute && !s_transientMute && selector::ok();
  if (want != s_soundOut || force) {
    selector::setSound(want);
    s_soundOut = want;
  }
}

void persistAudio() {
  settings::modify([](Settings& c) {
    c.input = s_input;
    c.att = s_att;
    c.triode = s_triode;
  });
}

void publish() {
  const uint32_t now = millis();
  uint32_t countdown = 0;
  if (s_phase == Phase::WARMUP) {
    const uint32_t el = now - s_phaseT0;
    countdown = el < s_warmupMs ? s_warmupMs - el : 0;
  } else if (s_phase == Phase::MODE_SWITCH && s_step == 0) {
    const uint32_t el = now - s_phaseT0;
    countdown = el < cfg::UA_DISCHARGE_TIMEOUT_MS ? cfg::UA_DISCHARGE_TIMEOUT_MS - el : 0;
  }
  state::modify([&](AmpState& s) {
    s.phase = s_phase;
    s.phaseSinceMs = s_phaseT0;
    s.countdownMs = countdown;
    s.fault = s_fault;
    s.faultTube = s_faultTube;
    s.input = s_input;
    s.att = s_att;
    s.userMute = s_userMute;
    s.sound = s_soundOut;
    s.triode = s_triode;
    s.spkLamp = relays::get(relays::SPK);
    s.trigger = s_trigger;
    s.service = s_service;
    s.selectorOk = selector::ok();
  });
}

// ---------------------------------------------------------------- przejscia

void powerOn(bool byTrigger) {
  if (s_phase != Phase::STANDBY) return;
  if (s_service) {
    console::logf("tryb serwisowy: najpierw 'service off'");
    return;
  }
  const AmpState st = state::get();
  s_trigStart = byTrigger;
  s_fromModeSwitch = false;
  s_userMute = false;
  s_fault = Fault::NONE;
  s_faultTube = -1;

  s_soundEnabled = false;
  applySound(true);
  relays::set(relays::SPK, false);
  selector::setAtt(cfg::ATT_MAX);
  relays::set(relays::UL, s_triode);  // anody wylaczone, wolno przelaczac

  bool warm = false;
  if (s_rtc.magic == RTC_MAGIC && s_rtc.lastHeatUs > 0) {
    const int64_t since = nowUs() - s_rtc.lastHeatUs;
    warm = since >= 0 && since < (int64_t)cfg::WARM_RESTART_MAX_MS * 1000 && st.m.valid &&
           st.m.ua < cfg::HV_PRESENT_V;
  }
  s_warmupMs = warm ? cfg::WARMUP_WARM_MS : cfg::WARMUP_MS;
  s_rtc.wasOn = 1;

  relays::set(relays::K1, true);
  enter(Phase::MAINS);
  console::logf("wlaczanie (%s), tryb %s, nagrzewanie %u s%s", byTrigger ? "trigger" : "recznie",
                s_triode ? "trioda" : "UL", (unsigned)(s_warmupMs / 1000), warm ? " (lampy cieple)" : "");
}

// SHUTDOWN albo FAULT: dzwiek, kolumny, anody od razu; zarzenie po 3 s w step()
void beginShutdown(Phase target) {
  s_soundEnabled = false;
  applySound(true);
  relays::set(relays::SPK, false);
  relays::set(relays::K4, false);
  relays::set(relays::K3, false);
  enter(target);
}

void finishHeatersOff() {
  relays::set(relays::K2, false);
  relays::set(relays::K1, false);
  selector::setInput(-1);
  selector::setAtt(cfg::ATT_MAX);
  s_rtc.wasOn = 0;
  persistAudio();
  settings::saveIfDue(true);
  settings::hoursSave();
  s_hoursDirty = false;
}

void startAnodes() {
  relays::set(relays::UL, s_triode);
  relays::set(relays::K3, true);
  enter(Phase::ANODES);
}

void startUnmute() {
  const Settings c = settings::get();
  uint8_t target;
  if (s_fromModeSwitch) {
    target = s_att;
  } else if (s_trigStart) {
    s_input = c.trigInput;
    target = c.trigAtt;
  } else {
    target = std::max(s_att, c.safeAtt);  // nie glosniej niz bezpieczna startowa
  }
  target = std::max(target, c.in[s_input].minAtt);
  s_unmuteTarget = target;

  s_soundEnabled = false;
  applySound();
  selector::setAtt(cfg::ATT_MAX);
  s_rampCode = cfg::ATT_MAX;
  selector::setInput(s_input);
  relays::set(relays::SPK, true);  // MUTE -> kolumny na lampe -> 0,5 s -> MUTE OFF
  enter(Phase::UNMUTE);
}

void beginModeSwitch(bool triode) {
  s_modeTarget = triode;
  s_soundEnabled = false;
  applySound();
  relays::set(relays::SPK, false);
  relays::set(relays::K4, false);
  relays::set(relays::K3, false);
  enter(Phase::MODE_SWITCH);
  console::logf("zmiana trybu na %s: czekam na Ua < %.0f V", triode ? "trioda" : "UL", cfg::UA_SWITCH_MAX_V);
}

void checkPendingFault() {
  const uint8_t f = s_pendingFault.exchange(0);
  if (!f) return;
  const Fault fault = (Fault)f;
  const int8_t tube = s_pendingTube;
  const float value = s_pendingValue;

  if (s_phase == Phase::STANDBY && s_service) {
    // tryb serwisowy: relays::emergency() juz wylaczylo anody, wylacz reszte
    relays::allOff();
    console::logf("ALARM w trybie serwisowym: %s %s %.1f, przekazniki wylaczone", faultName(fault),
                  tubeName(tube), value);
    return;
  }
  if (!powered(s_phase)) return;

  s_fault = fault;
  s_faultTube = tube;
  FaultRec r{};
  r.kt88s = settings::hours().kt88s;
  r.code = f;
  r.tube = tube;
  r.phase = (uint8_t)s_phase;
  r.value = value;
  settings::logFault(r);
  console::logf("ALARM: %s %s (%.1f) w fazie %s", faultName(fault), tubeName(tube), value, phaseName(s_phase));
  beginShutdown(Phase::FAULT);
}

// ---------------------------------------------------------------- komendy

void setVolume(int att) {
  att = std::clamp(att, (int)minAttFor(s_input), (int)cfg::ATT_MAX);
  if (att == s_att) return;
  s_att = (uint8_t)att;
  selector::setAtt(codeFor(s_att));
  persistAudio();
}

void switchInput(int idx) {
  if (idx < 0 || idx > 3 || idx == s_input) return;
  s_transientMute = true;
  applySound();
  waitMs(cfg::INPUT_MUTE_PRE_MS);
  s_input = (uint8_t)idx;
  selector::setInput(idx);
  s_att = std::max(s_att, minAttFor(s_input));
  selector::setAtt(codeFor(s_att));
  waitMs(cfg::INPUT_MUTE_POST_MS);
  s_transientMute = false;
  applySound();
  persistAudio();
  console::logf("wejscie %d: %s", idx + 1, settings::get().in[idx].name);
}

void switchSpeakers(bool lamp) {
  if (lamp == relays::get(relays::SPK)) return;
  s_transientMute = true;
  applySound();
  waitMs(cfg::INPUT_MUTE_PRE_MS);
  relays::set(relays::SPK, lamp);
  waitMs(cfg::SPK_SETTLE_MS);
  s_transientMute = false;
  applySound();
  console::logf("kolumny: %s", lamp ? "lampa" : "Marantz");
}

void serviceRelay(int id, bool on) {
  if (!s_service) {
    console::logf("przekazniki recznie tylko w trybie serwisowym ('service on')");
    return;
  }
  if (id < 0 || id >= relays::COUNT) return;
  const AmpState st = state::get();
#ifndef BENCH_SIM
  if (on && (id == relays::K3 || id == relays::K4)) {
    const bool biasOk = st.m.valid && st.m.vbias >= cfg::BIAS_OK_MIN_V && st.m.vbias <= cfg::BIAS_OK_MAX_V;
    if (!relays::get(relays::K1) || !relays::get(relays::K2) || !biasOk) {
      console::logf("odmowa: anody tylko przy K1+K2 i biasie w normie");
      return;
    }
  }
  if (id == relays::UL && relays::get(relays::K3)) {
    console::logf("odmowa: UL/trioda tylko przy wylaczonych anodach");
    return;
  }
  if (id == relays::UL && !(st.m.valid && st.m.ua < cfg::UA_SWITCH_MAX_V)) {
    console::logf("odmowa: UL/trioda dopiero przy Ua < %.0f V", cfg::UA_SWITCH_MAX_V);
    return;
  }
#else
  (void)st;
#endif
  relays::set((relays::Id)id, on);
  console::logf("serwis: %s %s", relays::name((relays::Id)id), on ? "ON" : "OFF");
}

void handle(const Command& c) {
  switch (c.cmd) {
    case Cmd::POWER_TOGGLE:
      if (s_phase == Phase::STANDBY)
        powerOn(false);
      else if (powered(s_phase))
        beginShutdown(Phase::SHUTDOWN);
      break;
    case Cmd::POWER_ON:
      powerOn(c.a != 0);
      break;
    case Cmd::POWER_OFF:
      if (powered(s_phase)) beginShutdown(Phase::SHUTDOWN);
      break;
    case Cmd::FAULT_ACK:
      if (s_phase == Phase::FAULT) {
        relays::allOff();
        s_rtc.wasOn = 0;
        s_fault = Fault::NONE;
        s_faultTube = -1;
        enter(Phase::STANDBY);
        console::logf("alarm potwierdzony");
      }
      break;
    case Cmd::VOL_SET:
      if (s_phase == Phase::PLAY) setVolume(c.a);
      break;
    case Cmd::VOL_STEP:
      if (s_phase == Phase::PLAY) setVolume((int)s_att - c.a);
      break;
    case Cmd::INPUT_SET:
      if (s_phase == Phase::PLAY) {
        switchInput(c.a);
      } else if (s_phase == Phase::STANDBY && c.a >= 0 && c.a < 4) {
        s_input = (uint8_t)c.a;
        persistAudio();
      }
      break;
    case Cmd::INPUT_STEP:
      if (s_phase == Phase::PLAY) switchInput((s_input + 4 + c.a) % 4);
      break;
    case Cmd::MUTE_TOGGLE:
      s_userMute = !s_userMute;
      applySound();
      break;
    case Cmd::MUTE_SET:
      s_userMute = c.a != 0;
      applySound();
      break;
    case Cmd::MODE_SET: {
      const bool triode = c.a != 0;
      if (s_phase == Phase::STANDBY) {
        s_triode = triode;
        persistAudio();
        console::logf("tryb %s (od nastepnego wlaczenia)", triode ? "trioda" : "UL");
      } else if (s_phase == Phase::PLAY && triode != s_triode) {
        beginModeSwitch(triode);
      } else if (triode != s_triode) {
        console::logf("UL/trioda tylko w PLAY albo STANDBY");
      }
      break;
    }
    case Cmd::SPK_SET:
      if (s_phase == Phase::PLAY) switchSpeakers(c.a != 0);
      break;
    case Cmd::TRIGGER_ON:
      s_trigger = true;
      console::logf("trigger: 12 V");
      if (s_phase == Phase::STANDBY && !s_service) powerOn(true);
      break;
    case Cmd::TRIGGER_OFF:
      s_trigger = false;
      console::logf("trigger: brak");
      if (powered(s_phase)) beginShutdown(Phase::SHUTDOWN);
      break;
    case Cmd::SERVICE_SET:
      if (s_phase != Phase::STANDBY) {
        console::logf("tryb serwisowy tylko w STANDBY");
        break;
      }
      s_service = c.a != 0;
      if (!s_service) relays::allOff();
      console::logf("tryb serwisowy %s", s_service ? "WL" : "WYL (przekazniki OFF)");
      break;
    case Cmd::RELAY_SET:
      serviceRelay(c.a, c.b != 0);
      break;
  }
}

// ---------------------------------------------------------------- krok maszyny

void step() {
  const uint32_t now = millis();
  const uint32_t el = now - s_phaseT0;
  const AmpState st = state::get();
  const Measurements& m = st.m;
  const bool biasOk = m.valid && m.vbias >= cfg::BIAS_OK_MIN_V && m.vbias <= cfg::BIAS_OK_MAX_V;

  switch (s_phase) {
    case Phase::STANDBY:
      // cewka UL (trioda) nie musi wisiec w czuwaniu: zwolnij, gdy anody rozladowane
      if (!s_service && relays::get(relays::UL) &&
          ((m.valid && m.ua < cfg::UA_SWITCH_MAX_V) || el > cfg::UA_DISCHARGE_TIMEOUT_MS))
        relays::set(relays::UL, false);
      break;

    case Phase::MAINS:
      if (el >= cfg::MAINS_MS) {
        relays::set(relays::K2, true);
        enter(Phase::BYPASS);
      }
      break;

    case Phase::BYPASS:
      enter(Phase::BIAS_CHECK);
      break;

    case Phase::BIAS_CHECK:
      if (el >= cfg::BIAS_CHECK_MIN_MS && biasOk)
        enter(Phase::WARMUP);
      else if (el >= cfg::BIAS_CHECK_MAX_MS)
        raiseFault(Fault::BIAS_RANGE, -1, m.vbias);
      break;

    case Phase::WARMUP:
      if (el >= s_warmupMs) {
        if (biasOk)
          startAnodes();
        else if (el >= s_warmupMs + cfg::WARMUP_BIAS_GRACE_MS)
          raiseFault(Fault::BIAS_RANGE, -1, m.vbias);
      }
      break;

    case Phase::ANODES:
      if (s_step == 0) {
        if (now - s_stepT0 >= cfg::K3_K4_DELAY_MS) {
          relays::set(relays::K4, true);
          s_step = 1;
          s_stepT0 = now;
        }
      } else if (m.valid && m.ua > cfg::UA_RUN_MIN_V) {
        s_stableSince = 0;
        enter(Phase::STABILIZE);
      } else if (now - s_stepT0 >= cfg::UA_RISE_TIMEOUT_MS) {
        raiseFault(Fault::UA_NO_RISE, -1, m.ua);
      }
      break;

    case Phase::STABILIZE: {
      bool ok = m.valid;
      int worst = 0;
      float worstErr = -1;
      for (int i = 0; i < 4; i++) {
        if (m.ik[i] < cfg::IK_STABLE_MIN_MA || m.ik[i] > cfg::IK_STABLE_MAX_MA) ok = false;
        const float err = fabsf(m.ik[i] - 0.5f * (cfg::IK_STABLE_MIN_MA + cfg::IK_STABLE_MAX_MA));
        if (err > worstErr) {
          worstErr = err;
          worst = i;
        }
      }
      if (ok) {
        if (!s_stableSince) s_stableSince = now ? now : 1;
        if (now - s_stableSince >= cfg::STABLE_HOLD_MS) startUnmute();
      } else {
        s_stableSince = 0;
      }
      if (s_phase == Phase::STABILIZE && el >= cfg::STABILIZE_TIMEOUT_MS)
        raiseFault(Fault::IK_UNSTABLE, (int8_t)worst, m.ik[worst]);
      break;
    }

    case Phase::UNMUTE:
      if (s_step == 0) {
        if (now - s_stepT0 >= cfg::SPK_SETTLE_MS) {
          s_soundEnabled = true;
          applySound();
          s_step = 1;
          s_stepT0 = now;
        }
      } else {
        const uint32_t t = now - s_stepT0;
        const uint8_t target = codeFor(s_unmuteTarget);
        const uint8_t code =
            t >= cfg::VOL_RAMP_MS ? target
                                  : (uint8_t)(cfg::ATT_MAX - (uint32_t)(cfg::ATT_MAX - target) * t / cfg::VOL_RAMP_MS);
        if (code != s_rampCode) {
          selector::setAtt(code);
          s_rampCode = code;
        }
        if (t >= cfg::VOL_RAMP_MS) {
          s_att = s_unmuteTarget;
          s_fromModeSwitch = false;
          persistAudio();
          enter(Phase::PLAY);
        }
      }
      break;

    case Phase::PLAY:
      if (el >= cfg::RESUME_CLEAR_PLAY_MS) s_rtc.resumeCount = 0;
      break;

    case Phase::MODE_SWITCH:
      if (s_step == 0) {
        if (m.valid && m.ua < cfg::UA_SWITCH_MAX_V) {
          relays::set(relays::UL, s_modeTarget);
          s_step = 1;
          s_stepT0 = now;
        } else if (el >= cfg::UA_DISCHARGE_TIMEOUT_MS) {
          raiseFault(Fault::HV_NO_DISCHARGE, -1, m.ua);
        }
      } else if (now - s_stepT0 >= cfg::UL_RELAY_SETTLE_MS) {
        s_triode = s_modeTarget;
        s_fromModeSwitch = true;
        persistAudio();
        startAnodes();
      }
      break;

    case Phase::SHUTDOWN:
      if (el >= cfg::SHUTDOWN_HEATER_DELAY_MS) {
        finishHeatersOff();
        s_rtc.resumeCount = 0;
        enter(Phase::STANDBY);
      }
      break;

    case Phase::FAULT:
      if (s_step == 0 && el >= cfg::SHUTDOWN_HEATER_DELAY_MS) {
        finishHeatersOff();
        s_step = 1;
        console::logf("FAULT: %s %s. Potwierdzenie: dlugie nacisniecie przycisku albo 'ack'", faultName(s_fault),
                      tubeName(s_faultTube));
      }
      break;
  }
}

void housekeeping() {
  const uint32_t now = millis();
  if (now - s_lastSecond >= 1000) {
    s_lastSecond = (now - s_lastSecond > 3000) ? now : s_lastSecond + 1000;
    if (relays::get(relays::K3)) {
      settings::hoursAdd(1, 1);
      s_hoursDirty = true;
    }
    if (relays::get(relays::K1)) s_rtc.lastHeatUs = nowUs();
  }
  if (s_hoursDirty && now - s_lastHoursSave >= cfg::HOURS_SAVE_PERIOD_MS) {
    settings::hoursSave();
    s_hoursDirty = false;
    s_lastHoursSave = now;
  }
  settings::saveIfDue();

  if (!selector::ok()) {
    if (s_soundOut) applySound();  // brak selektora = cisza
    if (now - s_lastSelectorProbe >= 2000) {
      s_lastSelectorProbe = now;
      if (selector::init()) {
        console::logf("selektor: odpowiada");
        if (s_phase == Phase::PLAY || s_phase == Phase::UNMUTE) {
          selector::setInput(s_input);
          selector::setAtt(s_phase == Phase::PLAY ? codeFor(s_att) : s_rampCode);
        }
        applySound(true);
      }
    }
  }
}
}  // namespace

// ---------------------------------------------------------------- API

void raiseFault(Fault f, int8_t tube, float value) {
  relays::emergency();
  selector::setSound(false);
  uint8_t expected = 0;
  if (s_pendingFault.compare_exchange_strong(expected, (uint8_t)f)) {
    s_pendingTube = tube;
    s_pendingValue = value;
  }
}

void init() {
  const Settings c = settings::get();
  s_input = c.input;
  s_att = c.att;
  s_triode = c.triode != 0;

  const esp_reset_reason_t rr = esp_reset_reason();
  if (rr == ESP_RST_POWERON || s_rtc.magic != RTC_MAGIC) {
    s_rtc = RtcMem{};
    s_rtc.magic = RTC_MAGIC;
  }

  const bool crash = rr == ESP_RST_PANIC || rr == ESP_RST_INT_WDT || rr == ESP_RST_TASK_WDT ||
                     rr == ESP_RST_WDT || rr == ESP_RST_BROWNOUT;
  if (crash) {
    FaultRec r{};
    r.kt88s = settings::hours().kt88s;
    r.code = (uint8_t)Fault::RESET;
    r.tube = -1;
    r.phase = s_rtc.wasOn ? (uint8_t)Phase::PLAY : (uint8_t)Phase::STANDBY;
    r.value = (float)rr;
    settings::logFault(r);
    console::logf("reset ESP32 (powod %d) zapisany w dzienniku", (int)rr);
  }

  if (s_rtc.wasOn) {
    if (s_rtc.resumeCount < cfg::MAX_AUTO_RESUME) {
      s_rtc.resumeCount++;
      console::logf("reset w trakcie pracy: wznawiam (%u/%u)", s_rtc.resumeCount, cfg::MAX_AUTO_RESUME);
      commands::post(Cmd::POWER_ON, 0);
    } else {
      console::logf("kolejny reset w trakcie pracy: zostaje w STANDBY");
      s_rtc.wasOn = 0;
    }
  }
  s_lastSecond = millis();
  publish();
}

void task(void*) {
  esp_task_wdt_add(nullptr);
  TickType_t last = xTaskGetTickCount();
  for (;;) {
    esp_task_wdt_reset();
    Command c;
    while (commands::receive(c, 0)) handle(c);
    checkPendingFault();
    step();
    checkPendingFault();  // alarm z kroku wyzej obsluz od razu
    housekeeping();
    publish();
    vTaskDelayUntil(&last, pdMS_TO_TICKS(cfg::SEQ_PERIOD_MS));
  }
}
}  // namespace sequencer
