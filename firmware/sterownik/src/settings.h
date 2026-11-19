#pragma once
#include <cstdint>

struct InputCfg {
  char name[12];
  uint8_t minAtt;  // limit najmniejszego tlumienia (docs/09, 9.9)
  int8_t trim;     // korekta poziomu -6..+6 dB (+ = glosniej)
};

struct Settings {
  uint16_t version;
  uint8_t input;
  uint8_t att;
  uint8_t triode;
  uint8_t trigInput;  // wejscie wybierane triggerem (Marantz)
  uint8_t trigAtt;    // stale tlumienie przy triggerze
  uint8_t safeAtt;    // bezpieczna glosnosc startowa
  InputCfg in[4];
  float ikTarget;     // mA (rozdz. 6)
  float shunt[4];     // Ohm, R123/R124/R223/R224 (kalibracja, etap 2)
  float uaK;          // V/V dzielnika Ua (etap 2)
  float biasK;        // V/V dzielnika biasu, 0 = nieskalibrowany (etap 2)
};

struct Hours {
  uint32_t kt88s;
  uint32_t sn7s;
};

struct FaultRec {
  uint32_t kt88s;  // godziny pracy KT88 w chwili zdarzenia (s)
  uint8_t code;    // Fault
  int8_t tube;
  uint8_t phase;   // Phase
  uint8_t reserved;
  float value;
};

namespace settings {
constexpr uint8_t LOG_SIZE = 32;

void load();
Settings get();
void lock();
void unlock();
Settings& raw();       // tylko pod lock()
void markDirtyLocked();

template <class F>
void modify(F f) {
  lock();
  f(raw());
  markDirtyLocked();
  unlock();
}

void saveIfDue(bool force = false);
void factoryReset();

void hoursAdd(uint32_t kt88s, uint32_t sn7s);
Hours hours();
void hoursReset(bool kt88, bool sn7);
void hoursSave();

void logFault(const FaultRec& r);
uint8_t logCount();
bool logGet(uint8_t idx, FaultRec& out);  // 0 = najnowszy
void logClear();
}  // namespace settings
