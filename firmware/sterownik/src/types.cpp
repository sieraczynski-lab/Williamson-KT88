#include "types.h"

const char* phaseName(Phase p) {
  switch (p) {
    case Phase::STANDBY: return "STANDBY";
    case Phase::MAINS: return "MAINS";
    case Phase::BYPASS: return "BYPASS";
    case Phase::BIAS_CHECK: return "BIAS_CHECK";
    case Phase::WARMUP: return "WARMUP";
    case Phase::ANODES: return "ANODES";
    case Phase::STABILIZE: return "STABILIZE";
    case Phase::UNMUTE: return "UNMUTE";
    case Phase::PLAY: return "PLAY";
    case Phase::MODE_SWITCH: return "MODE_SWITCH";
    case Phase::SHUTDOWN: return "SHUTDOWN";
    case Phase::FAULT: return "FAULT";
  }
  return "?";
}

const char* faultName(Fault f) {
  switch (f) {
    case Fault::NONE: return "-";
    case Fault::BIAS_RANGE: return "bias poza zakresem";
    case Fault::BIAS_LOST: return "zanik biasu";
    case Fault::UA_NO_RISE: return "Ua nie narasta";
    case Fault::UA_LOW: return "Ua za niskie";
    case Fault::IK_UNSTABLE: return "prad lampy niestabilny";
    case Fault::IK_OVER: return "prad lampy > 130 mA";
    case Fault::IK_IDLE_HIGH: return "prad spoczynkowy > 70 mA";
    case Fault::OVERTEMP: return "temperatura > 80 C";
    case Fault::MEAS_LOST: return "brak pomiarow";
    case Fault::HV_NO_DISCHARGE: return "Ua nie spada (UL/trioda)";
    case Fault::RESET: return "reset ESP32";
  }
  return "?";
}

const char* warnName(uint32_t bit) {
  switch (bit) {
    case W_IK_LOW: return "prad lampy < 20 mA (zarzenie / zuzyta)";
    case W_PAIR_DIFF: return "roznica w parze > 5 mA";
    case W_UA_LOW: return "Ua < 380 V";
    case W_UA_HIGH: return "Ua > 520 V";
    case W_TEMP: return "temperatura > 70 C";
    case W_NO_TEMP: return "brak czujnika temperatury";
  }
  return "?";
}

const char* tubeName(int8_t idx) {
  static const char* const names[4] = {"V5", "V6", "V7", "V8"};
  return (idx >= 0 && idx < 4) ? names[idx] : "";
}
