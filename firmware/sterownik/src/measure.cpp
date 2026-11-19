#include "measure.h"

#include <Arduino.h>
#include <esp_task_wdt.h>
#include <strings.h>

#include <algorithm>
#include <cmath>

#include "config.h"
#include "console.h"
#include "relays.h"
#include "state.h"

namespace measure {
namespace {

#ifdef BENCH_SIM
// Prosty model wzmacniacza do testow na stole: przekazniki -> napiecia i prady.
struct Sim {
  float vbias = 0, ua = 0, temp = 25, heatS = 0;
  float ik[4] = {0, 0, 0, 0};
  float nominal[4] = {52.0f, 51.5f, 52.5f, 52.0f};
  float ovBias = NAN, ovUa = NAN, ovTemp = NAN;
  float ovIk[4] = {NAN, NAN, NAN, NAN};
  bool lost = false;
};
Sim s_sim;
portMUX_TYPE s_simMux = portMUX_INITIALIZER_UNLOCKED;

void approach(float& v, float target, float tau, float dt) { v += (target - v) * (1.0f - expf(-dt / tau)); }

void simStep(Measurements& m, float dt) {
  const bool k1 = relays::get(relays::K1);
  const bool k3 = relays::get(relays::K3);
  const bool k4 = relays::get(relays::K4);

  portENTER_CRITICAL(&s_simMux);
  Sim& s = s_sim;
  approach(s.vbias, k1 ? -80.0f : 0.0f, 0.3f, dt);
  const float uaTarget = k3 ? (k4 ? 465.0f : 300.0f) : 0.0f;
  // narastanie szybkie, rozladowanie przez 560k: wolne
  approach(s.ua, uaTarget, uaTarget > s.ua ? 0.8f : 15.0f, dt);
  s.heatS = k1 ? std::min(s.heatS + dt, 60.0f) : std::max(s.heatS - dt * 0.5f, 0.0f);
  const float warm = std::min(s.heatS / 30.0f, 1.0f);  // katody grzeja sie ok. 30 s
  for (int i = 0; i < 4; i++) {
    const float target = s.ua > 100.0f ? s.nominal[i] * warm * (s.ua / 465.0f) : 0.0f;
    approach(s.ik[i], target, 1.0f, dt);
  }
  approach(s.temp, k1 ? 55.0f : 25.0f, 120.0f, dt);

  m.vbias = std::isnan(s.ovBias) ? s.vbias : s.ovBias;
  m.ua = std::isnan(s.ovUa) ? s.ua : s.ovUa;
  m.tempC = std::isnan(s.ovTemp) ? s.temp : s.ovTemp;
  for (int i = 0; i < 4; i++) m.ik[i] = std::isnan(s.ovIk[i]) ? s.ik[i] : s.ovIk[i];
  m.valid = !s.lost;
  portEXIT_CRITICAL(&s_simMux);
}
#endif
}  // namespace

void init() {}

void task(void*) {
  esp_task_wdt_add(nullptr);
  TickType_t last = xTaskGetTickCount();
  for (;;) {
    esp_task_wdt_reset();
    Measurements m;
#ifdef BENCH_SIM
    simStep(m, cfg::MEAS_PERIOD_MS / 1000.0f);
#else
    m.valid = false;  // etap 2: ADS1115 + DS18B20
#endif
    m.stampMs = millis();
    state::modify([&](AmpState& st) { st.m = m; });
    vTaskDelayUntil(&last, pdMS_TO_TICKS(cfg::MEAS_PERIOD_MS));
  }
}

#ifdef BENCH_SIM
bool simSet(const char* what, int idx, float value) {
  bool ok = true;
  portENTER_CRITICAL(&s_simMux);
  if (strcasecmp(what, "bias") == 0)
    s_sim.ovBias = value;
  else if (strcasecmp(what, "ua") == 0)
    s_sim.ovUa = value;
  else if (strcasecmp(what, "temp") == 0)
    s_sim.ovTemp = value;
  else if (strcasecmp(what, "ik") == 0 && idx >= 0 && idx < 4)
    s_sim.ovIk[idx] = value;
  else
    ok = false;
  portEXIT_CRITICAL(&s_simMux);
  return ok;
}

void simClear() {
  portENTER_CRITICAL(&s_simMux);
  s_sim.ovBias = s_sim.ovUa = s_sim.ovTemp = NAN;
  for (float& v : s_sim.ovIk) v = NAN;
  s_sim.lost = false;
  portEXIT_CRITICAL(&s_simMux);
}

void simLost(bool lost) {
  portENTER_CRITICAL(&s_simMux);
  s_sim.lost = lost;
  portEXIT_CRITICAL(&s_simMux);
}

void simPrint() {
  portENTER_CRITICAL(&s_simMux);
  Sim s = s_sim;
  portEXIT_CRITICAL(&s_simMux);
  auto ov = [](float v) { return std::isnan(v) ? "model" : "RECZNIE"; };
  console::out("sim: bias %s, ua %s, temp %s, ik %s/%s/%s/%s, pomiary %s\n", ov(s.ovBias), ov(s.ovUa),
               ov(s.ovTemp), ov(s.ovIk[0]), ov(s.ovIk[1]), ov(s.ovIk[2]), ov(s.ovIk[3]),
               s.lost ? "ZANIKLY" : "ok");
}
#endif
}  // namespace measure
