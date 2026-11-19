#include "console.h"

#include <Arduino.h>
#include <Wire.h>
#include <freertos/FreeRTOS.h>
#include <freertos/semphr.h>
#include <strings.h>

#include <cmath>
#include <cstdarg>
#include <cstdlib>
#include <cstring>

#include "commands.h"
#include "config.h"
#include "measure.h"
#include "relays.h"
#include "settings.h"
#include "state.h"

namespace console {
namespace {
SemaphoreHandle_t s_mtx = nullptr;
bool s_meas = false;

void vout(bool stamp, const char* fmt, va_list ap) {
  char buf[256];
  vsnprintf(buf, sizeof buf, fmt, ap);
  if (s_mtx) xSemaphoreTake(s_mtx, portMAX_DELAY);
  if (stamp) Serial.printf("[%8.1f] %s\n", millis() / 1000.0, buf);
  else Serial.print(buf);
  if (s_mtx) xSemaphoreGive(s_mtx);
}

bool is(const char* a, const char* b) { return a && strcasecmp(a, b) == 0; }
bool onOff(const char* a, bool& out) {
  if (is(a, "on") || is(a, "1")) return out = true, true;
  if (is(a, "off") || is(a, "0")) return out = false, true;
  return false;
}

void printMeas(const Measurements& m) {
  if (!m.valid) {
    out("pomiary: brak\n");
    return;
  }
  out("Ik V5 %5.1f  V6 %5.1f  V7 %5.1f  V8 %5.1f mA | bias %6.1f V | Ua %5.0f V | %4.1f C\n", m.ik[0], m.ik[1],
      m.ik[2], m.ik[3], m.vbias, m.ua, m.tempC);
}

void printStatus() {
  const AmpState s = state::get();
  const Settings c = settings::get();
  const uint32_t inPhase = (millis() - s.phaseSinceMs) / 1000;
  out("faza:      %s (%lu s)", phaseName(s.phase), (unsigned long)inPhase);
  if (s.countdownMs) out(", zostalo %lu s", (unsigned long)(s.countdownMs / 1000));
  out("%s\n", s.service ? "  [TRYB SERWISOWY]" : "");
  if (s.fault != Fault::NONE) out("ALARM:     %s %s\n", faultName(s.fault), tubeName(s.faultTube));
  for (uint32_t b = 1; b; b <<= 1)
    if (s.warnings & b) out("uwaga:     %s\n", warnName(b));
  if (s.hv) out("uwaga:     HV - Ua > 50 V przy wylaczonych anodach\n");
  out("wejscie:   %d %s, tlumienie %u dB (limit %u), %s%s\n", s.input + 1, c.in[s.input].name, s.att,
      c.in[s.input].minAtt, s.sound ? "GRA" : "cisza", s.userMute ? " (MUTE)" : "");
  out("tryb:      %s, kolumny: %s, trigger: %s, selektor: %s\n", s.triode ? "trioda" : "UL",
      s.spkLamp ? "lampa" : "Marantz", s.trigger ? "12 V" : "brak", s.selectorOk ? "ok" : "BRAK");
  out("przekazn.:");
  for (uint8_t i = 0; i < relays::COUNT; i++)
    out(" %s=%s", relays::name((relays::Id)i), (s.relays & (1u << i)) ? "ON" : "-");
  out("\n");
  printMeas(s.m);
}

void printLog() {
  const uint8_t n = settings::logCount();
  if (!n) {
    out("dziennik pusty\n");
    return;
  }
  for (uint8_t i = 0; i < n; i++) {
    FaultRec r;
    if (!settings::logGet(i, r)) break;
    out("%2u. %6.1f h  %-28s %-3s %8.1f  (faza %s)\n", i + 1, r.kt88s / 3600.0, faultName((Fault)r.code),
        tubeName(r.tube), r.value, phaseName((Phase)r.phase));
  }
}

void help() {
  out(
      "status                 stan, przekazniki, pomiary\n"
      "meas on|off            strumien pomiarow co 0,5 s\n"
      "on | off | ack         wlacz / wylacz / potwierdz alarm\n"
      "vol <dB> | vol + | -   tlumienie 0..63 dB (w PLAY)\n"
      "in <1-4>               wejscie\n"
      "mute [on|off]          wyciszenie\n"
      "mode ul|triode         UL / trioda (PLAY: z wylaczeniem anod)\n"
      "spk lamp|marantz       kolumny\n"
      "trig on|off            symulacja triggera 12 V\n"
      "service on|off         tryb serwisowy (tylko STANDBY)\n"
      "relay <k1..k4|sound|ul|spk> on|off   (tryb serwisowy)\n"
      "input <1-4> name <txt> | limit <dB> | trim <dB>\n"
      "triginput <1-4> <dB>   wejscie i stale tlumienie przy triggerze\n"
      "safe <dB>              bezpieczne tlumienie startowe\n"
      "hours [reset kt88|6sn7]  liczniki godzin lamp\n"
      "log [clear]            dziennik alarmow\n"
      "i2c                    skan magistrali I2C\n"
      "nvs reset              ustawienia fabryczne (bez godzin i dziennika)\n"
      "reboot\n"
#ifdef BENCH_SIM
      "sim                    stan symulacji\n"
      "sim bias|ua|temp <v>   wartosc reczna, 'sim ik <1-4> <mA>'\n"
      "sim auto               wszystko z modelu\n"
      "sim lost on|off        zanik pomiarow\n"
#endif
  );
}

void exec(char* line) {
  char* argv[8] = {};
  int argc = 0;
  char* save = nullptr;
  for (char* t = strtok_r(line, " \t", &save); t && argc < 8; t = strtok_r(nullptr, " \t", &save)) argv[argc++] = t;
  if (!argc) return;
  const char* a0 = argv[0];
  const char* a1 = argc > 1 ? argv[1] : nullptr;
  const char* a2 = argc > 2 ? argv[2] : nullptr;
  bool b;

  if (is(a0, "help") || is(a0, "?")) help();
  else if (is(a0, "status") || is(a0, "s")) printStatus();
  else if (is(a0, "meas")) {
    if (a1 && onOff(a1, b)) s_meas = b;
    else printMeas(state::get().m);
  } else if (is(a0, "on")) commands::post(Cmd::POWER_ON, 0);
  else if (is(a0, "off")) commands::post(Cmd::POWER_OFF);
  else if (is(a0, "ack")) commands::post(Cmd::FAULT_ACK);
  else if (is(a0, "vol") && a1) {
    if (is(a1, "+")) commands::post(Cmd::VOL_STEP, 1);
    else if (is(a1, "-")) commands::post(Cmd::VOL_STEP, -1);
    else commands::post(Cmd::VOL_SET, (int16_t)abs(atoi(a1)));
  } else if (is(a0, "in") && a1) commands::post(Cmd::INPUT_SET, (int16_t)(atoi(a1) - 1));
  else if (is(a0, "mute")) {
    if (a1 && onOff(a1, b)) commands::post(Cmd::MUTE_SET, b);
    else commands::post(Cmd::MUTE_TOGGLE);
  } else if (is(a0, "mode") && a1) {
    if (is(a1, "ul")) commands::post(Cmd::MODE_SET, 0);
    else if (is(a1, "triode") || is(a1, "trioda")) commands::post(Cmd::MODE_SET, 1);
    else out("mode ul|triode\n");
  } else if (is(a0, "spk") && a1) {
    commands::post(Cmd::SPK_SET, is(a1, "lamp") || is(a1, "lampa") ? 1 : 0);
  } else if (is(a0, "trig") && a1 && onOff(a1, b)) {
    commands::post(b ? Cmd::TRIGGER_ON : Cmd::TRIGGER_OFF);
  } else if (is(a0, "service") && a1 && onOff(a1, b)) {
    commands::post(Cmd::SERVICE_SET, b);
  } else if (is(a0, "relay") && a1 && a2 && onOff(a2, b)) {
    const int id = relays::fromName(a1);
    if (id < 0) out("nieznany przekaznik: %s\n", a1);
    else commands::post(Cmd::RELAY_SET, (int16_t)id, b);
  } else if (is(a0, "input") && a1 && a2 && argc > 3) {
    const int n = atoi(a1) - 1;
    if (n < 0 || n > 3) {
      out("wejscie 1-4\n");
      return;
    }
    const char* v = argv[3];
    if (is(a2, "name")) settings::modify([&](Settings& c) { strlcpy(c.in[n].name, v, sizeof c.in[n].name); });
    else if (is(a2, "limit")) settings::modify([&](Settings& c) { c.in[n].minAtt = (uint8_t)abs(atoi(v)); });
    else if (is(a2, "trim")) settings::modify([&](Settings& c) { c.in[n].trim = (int8_t)atoi(v); });
    else {
      out("input <1-4> name|limit|trim <wartosc>\n");
      return;
    }
    out("zapisane (NVS za ok. 10 s)\n");
  } else if (is(a0, "triginput") && a1 && a2) {
    const int n = atoi(a1) - 1;
    if (n < 0 || n > 3) return;
    settings::modify([&](Settings& c) {
      c.trigInput = (uint8_t)n;
      c.trigAtt = (uint8_t)abs(atoi(a2));
    });
  } else if (is(a0, "safe") && a1) {
    settings::modify([&](Settings& c) { c.safeAtt = (uint8_t)abs(atoi(a1)); });
  } else if (is(a0, "hours")) {
    if (is(a1, "reset") && a2) {
      settings::hoursReset(is(a2, "kt88"), is(a2, "6sn7"));
    }
    const Hours h = settings::hours();
    out("KT88: %.1f h, 6SN7: %.1f h\n", h.kt88s / 3600.0, h.sn7s / 3600.0);
  } else if (is(a0, "log")) {
    if (is(a1, "clear")) {
      settings::logClear();
      out("dziennik wyczyszczony\n");
    } else {
      printLog();
    }
  } else if (is(a0, "i2c")) {
    for (uint8_t addr = 1; addr < 127; addr++) {
      Wire.beginTransmission(addr);
      if (Wire.endTransmission() == 0) out("I2C 0x%02X\n", addr);
    }
    out("koniec skanu (oczekiwane: 0x20 selektor, 0x48/0x49 ADS1115, 0x60 MCP4728)\n");
  } else if (is(a0, "nvs") && is(a1, "reset")) {
    settings::factoryReset();
    out("ustawienia fabryczne zapisane; 'reboot', zeby wczytac\n");
  } else if (is(a0, "reboot")) {
    if (state::get().phase != Phase::STANDBY) {
      out("najpierw 'off' (reset w pracy wylacza anody bez sekwencji)\n");
      return;
    }
    settings::saveIfDue(true);
    settings::hoursSave();
    delay(100);
    ESP.restart();
  }
#ifdef BENCH_SIM
  else if (is(a0, "sim")) {
    if (!a1) measure::simPrint();
    else if (is(a1, "auto")) measure::simClear();
    else if (is(a1, "lost") && a2 && onOff(a2, b)) measure::simLost(b);
    else if (is(a1, "ik") && a2 && argc > 3) {
      const float v = is(argv[3], "auto") ? NAN : (float)atof(argv[3]);
      if (!measure::simSet("ik", atoi(a2) - 1, v)) out("sim ik <1-4> <mA|auto>\n");
    } else if (a2) {
      const float v = is(a2, "auto") ? NAN : (float)atof(a2);
      if (!measure::simSet(a1, 0, v)) out("sim bias|ua|temp <wartosc|auto>\n");
    } else {
      out("sim bias|ua|temp <v> | sim ik <1-4> <mA> | sim auto | sim lost on|off\n");
    }
  }
#endif
  else out("nieznana komenda, 'help'\n");
}
}  // namespace

void init() {
  Serial.setTxBufferSize(4096);
  Serial.begin(115200);
  Serial.setTxTimeoutMs(0);  // bez podlaczonego USB nie blokuj zadan
  s_mtx = xSemaphoreCreateMutex();
}

void out(const char* fmt, ...) {
  va_list ap;
  va_start(ap, fmt);
  vout(false, fmt, ap);
  va_end(ap);
}

void logf(const char* fmt, ...) {
  va_list ap;
  va_start(ap, fmt);
  vout(true, fmt, ap);
  va_end(ap);
}

void task(void*) {
  char buf[128];
  size_t len = 0;
  uint32_t lastMeas = 0;
  out("\nWilliamson KT88 sterownik " FW_VERSION
#ifdef BENCH_SIM
      " [BENCH: pomiary symulowane]"
#endif
      "\n'help' - lista komend\n");
  for (;;) {
    while (Serial.available()) {
      const int ch = Serial.read();
      if (ch == '\r' || ch == '\n') {
        if (len) {
          out("\n");
          buf[len] = 0;
          exec(buf);
          len = 0;
        }
      } else if ((ch == 8 || ch == 127) && len) {
        len--;
        out("\b \b");
      } else if (ch >= 32 && len < sizeof buf - 1) {
        buf[len++] = (char)ch;
        out("%c", ch);  // echo
      }
    }
    if (s_meas && millis() - lastMeas >= 500) {
      lastMeas = millis();
      const AmpState s = state::get();
      out("%-11s ", phaseName(s.phase));
      printMeas(s.m);
    }
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}
}  // namespace console
