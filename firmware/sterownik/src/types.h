#pragma once
#include <cstdint>

// Kolejnosc ma znaczenie: zakresy faz sa sprawdzane przez porownanie (poweredPhase itp.)
enum class Phase : uint8_t {
  STANDBY,
  MAINS,
  BYPASS,
  BIAS_CHECK,
  WARMUP,
  ANODES,
  STABILIZE,
  UNMUTE,
  PLAY,
  MODE_SWITCH,
  SHUTDOWN,
  FAULT,
};

enum class Fault : uint8_t {
  NONE,
  BIAS_RANGE,       // szyna biasu poza -68...-92 V przy kontroli / po nagrzewaniu
  BIAS_LOST,        // szyna biasu mniej ujemna niz -65 V w trakcie pracy
  UA_NO_RISE,       // Ua nie przekroczylo 380 V w 10 s
  UA_LOW,           // Ua < 300 V w pracy
  IK_UNSTABLE,      // prady nie ustabilizowaly sie w 35-75 mA w 60 s
  IK_OVER,          // prad > 130 mA przez 3 s
  IK_IDLE_HIGH,     // prad > 70 mA w ciszy przez 5 s
  OVERTEMP,         // > 80 C
  MEAS_LOST,        // brak pomiarow
  HV_NO_DISCHARGE,  // Ua nie spadlo < 30 V w 90 s (UL/trioda)
  RESET,            // tylko wpis w dzienniku: reset ESP32 (watchdog, panic, brownout)
};

// Ostrzezenia (maska bitowa), liczone przez zadanie safety
enum Warn : uint32_t {
  W_IK_LOW = 1u << 0,
  W_PAIR_DIFF = 1u << 1,
  W_UA_LOW = 1u << 2,
  W_UA_HIGH = 1u << 3,
  W_TEMP = 1u << 4,
  W_NO_TEMP = 1u << 5,
};

const char* phaseName(Phase p);
const char* faultName(Fault f);
const char* warnName(uint32_t bit);
const char* tubeName(int8_t idx);  // 0..3 -> V5..V8
