#include "selector.h"

#include <Arduino.h>
#include <Wire.h>
#include <freertos/FreeRTOS.h>
#include <freertos/semphr.h>

#include "config.h"
#include "relays.h"

#ifndef MUTE_VIA_GPIO14
#define MUTE_VIA_GPIO14 1
#endif

namespace selector {
namespace {
constexpr uint8_t ADDR = 0x20;
constexpr uint8_t REG_IODIRA = 0x00;  // IOCON.BANK = 0, adresy A/B kolejno
constexpr uint8_t REG_OLATA = 0x14;
constexpr uint8_t IODIR_A = 0x00;  // GPA0-7 wyjscia
constexpr uint8_t IODIR_B = 0xF8;  // GPB0-2 wyjscia, GPB3-7 wolne (zostaja wejsciami)

SemaphoreHandle_t s_mtx = nullptr;
bool s_ok = false;
uint8_t s_inMask = 0;  // bity K1-K4
uint8_t s_code = cfg::ATT_MAX;
bool s_gpb2 = false;

bool write2(uint8_t reg, uint8_t a, uint8_t b) {
  Wire.beginTransmission(ADDR);
  Wire.write(reg);
  Wire.write(a);
  Wire.write(b);
  return Wire.endTransmission() == 0;
}

// GPA0-3 wejscia, GPA4-7 bity 0-3 kodu, GPB0-1 bity 4-5, GPB2 = K11
bool push(uint8_t inMask, uint8_t code, bool gpb2) {
  uint8_t a = (inMask & 0x0F) | ((code & 0x0F) << 4);
  uint8_t b = ((code >> 4) & 0x03) | (gpb2 ? 0x04 : 0x00);
  bool ok = write2(REG_OLATA, a, b);
  if (!ok) s_ok = false;
  return ok;
}

struct Guard {
  bool held;
  explicit Guard(TickType_t wait) { held = xSemaphoreTake(s_mtx, wait) == pdTRUE; }
  ~Guard() {
    if (held) xSemaphoreGive(s_mtx);
  }
};
}  // namespace

bool init() {
  if (!s_mtx) s_mtx = xSemaphoreCreateMutex();
  Guard g(portMAX_DELAY);
  s_inMask = 0;
  s_code = cfg::ATT_MAX;
  s_gpb2 = false;
  // najpierw zatrzaski (OLAT), potem kierunek: piny startuja od razu w bezpiecznym stanie
  s_ok = true;
  bool ok = push(s_inMask, s_code, s_gpb2) && write2(REG_IODIRA, IODIR_A, IODIR_B);
  s_ok = ok;
  return ok;
}

bool ok() { return s_ok; }

bool setSound(bool on) {
#if MUTE_VIA_GPIO14
  relays::set(relays::SOUND, on);
  return true;
#else
  if (!s_mtx) return false;
  // wywolywane tez z zadania safety: nie czekamy dluzej niz 50 ms
  Guard g(pdMS_TO_TICKS(50));
  if (!g.held) return false;
  s_gpb2 = on;
  return push(s_inMask, s_code, s_gpb2);
#endif
}

bool setInput(int idx) {
  if (!s_mtx) return false;
  Guard g(portMAX_DELAY);
  bool ok = push(0, s_code, s_gpb2);
  s_inMask = 0;
  if (idx >= 0 && idx < 4) {
    vTaskDelay(pdMS_TO_TICKS(cfg::INPUT_BREAK_MS));
    s_inMask = 1u << idx;
    ok = push(s_inMask, s_code, s_gpb2) && ok;
  }
  return ok;
}

bool setAtt(uint8_t code) {
  if (!s_mtx) return false;
  if (code > cfg::ATT_MAX) code = cfg::ATT_MAX;
  Guard g(portMAX_DELAY);
  bool ok = true;
  uint8_t added = code & ~s_code;
  if (added && code != s_code) {
    // najpierw dolacz nowe bity (chwilowo wieksze tlumienie), potem zdejmij zbedne
    ok = push(s_inMask, s_code | code, s_gpb2);
    vTaskDelay(pdMS_TO_TICKS(cfg::LADDER_OVERLAP_MS));
  }
  ok = push(s_inMask, code, s_gpb2) && ok;
  s_code = code;
  return ok;
}

uint8_t att() { return s_code; }

int input() {
  for (int i = 0; i < 4; i++)
    if (s_inMask & (1u << i)) return i;
  return -1;
}
}  // namespace selector
