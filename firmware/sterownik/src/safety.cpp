#include "safety.h"

#include <Arduino.h>
#include <esp_task_wdt.h>

#include <cmath>

#include "config.h"
#include "relays.h"
#include "sequencer.h"
#include "state.h"

namespace safety {
namespace {
// zakresy faz (kolejnosc w enum Phase)
bool measRequired(Phase p) { return p >= Phase::BIAS_CHECK && p <= Phase::MODE_SWITCH; }
bool biasSupervised(Phase p) { return p >= Phase::WARMUP && p <= Phase::MODE_SWITCH; }
bool uaSupervised(Phase p) { return p == Phase::STABILIZE || p == Phase::UNMUTE || p == Phase::PLAY; }
bool powered(Phase p) { return p >= Phase::MAINS && p <= Phase::MODE_SWITCH; }

// licznik "warunek trwa od": 0 = nie trwa
struct Hold {
  uint32_t since = 0;
  bool active(bool cond, uint32_t now, uint32_t ms) {
    if (!cond) {
      since = 0;
      return false;
    }
    if (!since) since = now ? now : 1;
    return now - since >= ms;
  }
};

Hold s_lost, s_uaLow;
Hold s_ikOver[4], s_ikIdle[4];
}  // namespace

void init() {
  esp_task_wdt_config_t c = {};
  c.timeout_ms = cfg::WDT_TIMEOUT_MS;
  c.idle_core_mask = 0;  // pilnujemy wlasnych zadan, nie idle
  c.trigger_panic = true;  // panic -> reset -> bezpieczny stan
  if (esp_task_wdt_reconfigure(&c) != ESP_OK) esp_task_wdt_init(&c);
}

void task(void*) {
  esp_task_wdt_add(nullptr);
  TickType_t last = xTaskGetTickCount();
  for (;;) {
    esp_task_wdt_reset();
    const uint32_t now = millis();
    const AmpState st = state::get();
    const Measurements& m = st.m;
    const bool fresh = m.valid && (now - m.stampMs) <= cfg::MEAS_STALE_MS;
    const bool anodesOn = st.relays & (1u << relays::K3);
    uint32_t warn = 0;
    bool hv = st.hv;

    // anody wlaczone recznie (tryb serwisowy) tez sa pilnowane
    const bool needMeas = measRequired(st.phase) || anodesOn;
    if (s_lost.active(needMeas && !fresh, now, cfg::MEAS_LOST_MS))
      sequencer::raiseFault(Fault::MEAS_LOST, -1, 0);

    if (fresh) {
      if ((biasSupervised(st.phase) || anodesOn) && m.vbias > cfg::BIAS_FAULT_V)
        sequencer::raiseFault(Fault::BIAS_LOST, -1, m.vbias);

      const bool silence = st.phase == Phase::PLAY && (!st.sound || st.att >= cfg::SILENCE_ATT);
      for (int i = 0; i < 4; i++) {
        if (s_ikOver[i].active(anodesOn && m.ik[i] > cfg::IK_OVER_MA, now, cfg::IK_OVER_MS))
          sequencer::raiseFault(Fault::IK_OVER, i, m.ik[i]);
        if (s_ikIdle[i].active(silence && m.ik[i] > cfg::IK_IDLE_MAX_MA, now, cfg::IK_IDLE_MS))
          sequencer::raiseFault(Fault::IK_IDLE_HIGH, i, m.ik[i]);
      }

      if (st.phase == Phase::PLAY) {
        for (int pair = 0; pair < 2; pair++) {
          const float a = m.ik[pair * 2], b = m.ik[pair * 2 + 1];
          if ((a < cfg::IK_LOW_WARN_MA && b >= cfg::IK_STABLE_MIN_MA) ||
              (b < cfg::IK_LOW_WARN_MA && a >= cfg::IK_STABLE_MIN_MA))
            warn |= W_IK_LOW;
          if (silence && fabsf(a - b) > cfg::PAIR_DIFF_WARN_MA) warn |= W_PAIR_DIFF;
        }
      }

      if (s_uaLow.active(uaSupervised(st.phase) && m.ua < cfg::UA_FAULT_LOW_V, now, cfg::UA_FAULT_MS))
        sequencer::raiseFault(Fault::UA_LOW, -1, m.ua);
      if (st.phase == Phase::PLAY && m.ua < cfg::UA_WARN_LOW_V) warn |= W_UA_LOW;
      if (st.phase == Phase::PLAY && m.ua > cfg::UA_WARN_HIGH_V) warn |= W_UA_HIGH;

      hv = !anodesOn && m.ua > cfg::HV_PRESENT_V;

      if (std::isnan(m.tempC)) {
        warn |= W_NO_TEMP;
      } else {
        if (m.tempC > cfg::TEMP_WARN_C) warn |= W_TEMP;
        if (powered(st.phase) && m.tempC > cfg::TEMP_FAULT_C) sequencer::raiseFault(Fault::OVERTEMP, -1, m.tempC);
      }
    } else {
      warn = st.warnings;  // brak swiezych danych: zostaw ostatnie ostrzezenia
    }

    state::modify([&](AmpState& s) {
      s.warnings = warn;
      s.hv = hv;
    });
    vTaskDelayUntil(&last, pdMS_TO_TICKS(cfg::SAFETY_PERIOD_MS));
  }
}
}  // namespace safety
