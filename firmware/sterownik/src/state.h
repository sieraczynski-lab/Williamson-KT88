#pragma once
#include <cmath>
#include <cstdint>

#include "types.h"

struct Measurements {
  float ik[4] = {0, 0, 0, 0};  // mA, V5 V6 (L), V7 V8 (P)
  float vbias = 0;             // V (ujemne)
  float ua = 0;                // V
  float tempC = NAN;           // NAN = brak czujnika
  bool valid = false;
  uint32_t stampMs = 0;
};

// Stan calosci. Pisza: sequencer (faza, audio), measure (m), safety (warnings, hv).
// Pozostali tylko czytaja kopie przez state::get().
struct AmpState {
  Phase phase = Phase::STANDBY;
  uint32_t phaseSinceMs = 0;
  uint32_t countdownMs = 0;  // nagrzewanie / rozladowanie przed UL-trioda
  Fault fault = Fault::NONE;
  int8_t faultTube = -1;
  uint32_t warnings = 0;
  bool hv = false;  // Ua > 50 V przy wylaczonych anodach

  uint8_t input = 0;  // 0..3
  uint8_t att = 63;   // tlumienie dB (0 = najglosniej)
  bool userMute = false;
  bool sound = false;  // K11 zalaczony (faktycznie gra)
  bool triode = false;
  bool spkLamp = false;
  bool trigger = false;
  bool service = false;
  bool selectorOk = false;

  uint8_t relays = 0;  // maska relays::Id, uzupelniana przy get()
  Measurements m;
};

namespace state {
void init();
AmpState get();
void lock();
void unlock();
AmpState& raw();  // tylko pod lock()

template <class F>
void modify(F f) {
  lock();
  f(raw());
  unlock();
}
}  // namespace state
