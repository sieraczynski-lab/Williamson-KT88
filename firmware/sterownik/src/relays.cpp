#include "relays.h"

#include <Arduino.h>
#include <driver/gpio.h>
#include <strings.h>

#include <atomic>

#include "pins.h"

namespace relays {
namespace {
const uint8_t kPin[COUNT] = {pins::RLY_K1,    pins::RLY_K2, pins::RLY_K3, pins::RLY_K4,
                             pins::RLY_SOUND, pins::RLY_UL, pins::RLY_SPK};
const char* const kName[COUNT] = {"k1", "k2", "k3", "k4", "sound", "ul", "spk"};
std::atomic<uint8_t> s_mask{0};
portMUX_TYPE s_mux = portMUX_INITIALIZER_UNLOCKED;
}  // namespace

void init() {
  for (uint8_t i = 0; i < COUNT; i++) {
    digitalWrite(kPin[i], LOW);
    pinMode(kPin[i], OUTPUT);
    digitalWrite(kPin[i], LOW);
  }
  s_mask = 0;
}

void set(Id id, bool on) {
  if (id >= COUNT) return;
  portENTER_CRITICAL(&s_mux);
  gpio_set_level((gpio_num_t)kPin[id], on ? 1 : 0);
  uint8_t m = s_mask.load();
  s_mask = on ? (m | (1u << id)) : (m & ~(1u << id));
  portEXIT_CRITICAL(&s_mux);
}

bool get(Id id) { return id < COUNT && (s_mask.load() & (1u << id)); }
uint8_t mask() { return s_mask.load(); }

void allOff() {
  // kolejnosc jak przy wylaczaniu: najpierw dzwiek i kolumny, potem anody, na koncu siec
  set(SOUND, false);
  set(SPK, false);
  set(K4, false);
  set(K3, false);
  set(K2, false);
  set(K1, false);
  set(UL, false);
}

void emergency() {
  set(SOUND, false);
  set(SPK, false);
  set(K4, false);
  set(K3, false);
}

const char* name(Id id) { return id < COUNT ? kName[id] : "?"; }

int fromName(const char* s) {
  for (uint8_t i = 0; i < COUNT; i++)
    if (strcasecmp(s, kName[i]) == 0) return i;
  return -1;
}
}  // namespace relays
