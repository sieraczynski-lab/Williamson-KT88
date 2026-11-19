#include "settings.h"

#include <Arduino.h>
#include <Preferences.h>
#include <freertos/FreeRTOS.h>
#include <freertos/semphr.h>

#include <cstring>

#include "config.h"

namespace settings {
namespace {
constexpr uint16_t VERSION = 1;

struct LogBlob {
  uint8_t head;   // nastepny wolny
  uint8_t count;
  uint8_t pad[2];
  FaultRec rec[LOG_SIZE];
};

Preferences s_prefs;
SemaphoreHandle_t s_mtx = nullptr;
Settings s_cfg;
Hours s_hours;
LogBlob s_log;
bool s_dirty = false;
uint32_t s_changedMs = 0;

void defaults(Settings& c) {
  memset(&c, 0, sizeof c);
  c.version = VERSION;
  c.input = 0;
  c.att = 40;
  c.triode = 0;
  c.trigInput = 1;
  c.trigAtt = 20;
  c.safeAtt = cfg::SAFE_START_ATT;
  // nazwy i limity z docs/10 rozdz. 8: DAC 2 V -10 dB, Marantz 1,2 V -5 dB, 1 V -4 dB
  const char* names[4] = {"DAC", "Marantz", "CD", "AUX"};
  const uint8_t limits[4] = {10, 5, 4, 4};
  for (int i = 0; i < 4; i++) {
    strncpy(c.in[i].name, names[i], sizeof c.in[i].name - 1);
    c.in[i].minAtt = limits[i];
    c.in[i].trim = 0;
  }
  c.ikTarget = 52.0f;
  for (float& r : c.shunt) r = 10.0f;
  c.uaK = (3000000.0f + 15000.0f) / 15000.0f;
  c.biasK = 0.0f;
}

void sanitize(Settings& c) {
  if (c.input > 3) c.input = 0;
  if (c.att > cfg::ATT_MAX) c.att = cfg::ATT_MAX;
  if (c.trigInput > 3) c.trigInput = 1;
  if (c.trigAtt > cfg::ATT_MAX) c.trigAtt = cfg::ATT_MAX;
  if (c.safeAtt > cfg::ATT_MAX) c.safeAtt = cfg::SAFE_START_ATT;
  for (auto& in : c.in) {
    in.name[sizeof in.name - 1] = 0;
    if (in.minAtt > cfg::ATT_MAX) in.minAtt = cfg::ATT_MAX;
    if (in.trim < -6 || in.trim > 6) in.trim = 0;
  }
}

template <class T>
bool loadBlob(const char* key, T& out) {
  if (s_prefs.getBytesLength(key) != sizeof(T)) return false;
  return s_prefs.getBytes(key, &out, sizeof(T)) == sizeof(T);
}
}  // namespace

void load() {
  s_mtx = xSemaphoreCreateMutex();
  s_prefs.begin("amp", false);
  if (!loadBlob("cfg", s_cfg) || s_cfg.version != VERSION) defaults(s_cfg);
  sanitize(s_cfg);
  if (!loadBlob("hours", s_hours)) memset(&s_hours, 0, sizeof s_hours);
  if (!loadBlob("log", s_log) || s_log.head >= LOG_SIZE || s_log.count > LOG_SIZE) memset(&s_log, 0, sizeof s_log);
}

Settings get() {
  lock();
  Settings c = s_cfg;
  unlock();
  return c;
}

void lock() { xSemaphoreTake(s_mtx, portMAX_DELAY); }
void unlock() { xSemaphoreGive(s_mtx); }
Settings& raw() { return s_cfg; }

void markDirtyLocked() {
  sanitize(s_cfg);
  s_dirty = true;
  s_changedMs = millis();
}

void saveIfDue(bool force) {
  lock();
  if (s_dirty && (force || millis() - s_changedMs >= cfg::SETTINGS_SAVE_DELAY_MS)) {
    s_prefs.putBytes("cfg", &s_cfg, sizeof s_cfg);
    s_dirty = false;
  }
  unlock();
}

void factoryReset() {
  lock();
  defaults(s_cfg);
  s_prefs.putBytes("cfg", &s_cfg, sizeof s_cfg);
  s_dirty = false;
  unlock();
}

void hoursAdd(uint32_t kt88s, uint32_t sn7s) {
  lock();
  s_hours.kt88s += kt88s;
  s_hours.sn7s += sn7s;
  unlock();
}

Hours hours() {
  lock();
  Hours h = s_hours;
  unlock();
  return h;
}

void hoursReset(bool kt88, bool sn7) {
  lock();
  if (kt88) s_hours.kt88s = 0;
  if (sn7) s_hours.sn7s = 0;
  s_prefs.putBytes("hours", &s_hours, sizeof s_hours);
  unlock();
}

void hoursSave() {
  lock();
  s_prefs.putBytes("hours", &s_hours, sizeof s_hours);
  unlock();
}

void logFault(const FaultRec& r) {
  lock();
  s_log.rec[s_log.head] = r;
  s_log.head = (s_log.head + 1) % LOG_SIZE;
  if (s_log.count < LOG_SIZE) s_log.count++;
  s_prefs.putBytes("log", &s_log, sizeof s_log);
  unlock();
}

uint8_t logCount() {
  lock();
  uint8_t n = s_log.count;
  unlock();
  return n;
}

bool logGet(uint8_t idx, FaultRec& out) {
  lock();
  bool ok = idx < s_log.count;
  if (ok) out = s_log.rec[(s_log.head + LOG_SIZE - 1 - idx) % LOG_SIZE];
  unlock();
  return ok;
}

void logClear() {
  lock();
  memset(&s_log, 0, sizeof s_log);
  s_prefs.putBytes("log", &s_log, sizeof s_log);
  unlock();
}
}  // namespace settings
