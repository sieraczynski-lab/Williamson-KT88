#pragma once
#include <cstdint>

// Progi i czasy z docs/10 (rozdz. 4, 7, 15). Zmiana tutaj = zmiana w dokumencie.
namespace cfg {
// Sekwencja wlaczania (rozdz. 4)
constexpr uint32_t MAINS_MS = 1500;               // K1 -> K2
constexpr uint32_t BIAS_CHECK_MIN_MS = 2000;
constexpr uint32_t BIAS_CHECK_MAX_MS = 5000;
constexpr float BIAS_OK_MIN_V = -92.0f;
constexpr float BIAS_OK_MAX_V = -68.0f;
constexpr uint32_t WARMUP_MS = 45000;
constexpr uint32_t WARMUP_WARM_MS = 15000;        // lampy cieple (krotka przerwa)
constexpr uint32_t WARM_RESTART_MAX_MS = 120000;  // "krotka przerwa" < 2 min
constexpr uint32_t WARMUP_BIAS_GRACE_MS = 10000;  // po nagrzewaniu bias nadal poza norma -> FAULT
constexpr uint32_t K3_K4_DELAY_MS = 1500;
constexpr uint32_t UA_RISE_TIMEOUT_MS = 10000;
constexpr float UA_RUN_MIN_V = 380.0f;
constexpr float IK_STABLE_MIN_MA = 35.0f;
constexpr float IK_STABLE_MAX_MA = 75.0f;
constexpr uint32_t STABLE_HOLD_MS = 5000;
constexpr uint32_t STABILIZE_TIMEOUT_MS = 60000;
constexpr uint32_t SPK_SETTLE_MS = 500;           // MUTE -> RLY_SPK -> 0,5 s -> MUTE OFF
constexpr uint32_t VOL_RAMP_MS = 1000;            // narastanie glosnosci po wlaczeniu
constexpr uint32_t SHUTDOWN_HEATER_DELAY_MS = 3000;

// UL / trioda (rozdz. 7)
constexpr float UA_SWITCH_MAX_V = 30.0f;
constexpr uint32_t UA_DISCHARGE_TIMEOUT_MS = 90000;
constexpr uint32_t UL_RELAY_SETTLE_MS = 200;

// Selektor (rozdz. 8)
constexpr uint32_t INPUT_MUTE_PRE_MS = 50;
constexpr uint32_t INPUT_MUTE_POST_MS = 100;
constexpr uint32_t INPUT_BREAK_MS = 10;           // wszystkie K1-K4 OFF -> wybrany ON
constexpr uint32_t LADDER_OVERLAP_MS = 5;         // drabinka: najpierw nowe bity, potem zbedne
constexpr uint8_t ATT_MAX = 63;
constexpr uint8_t SAFE_START_ATT = 30;
constexpr uint8_t SILENCE_ATT = 50;               // "cisza": tlumienie >= 50 dB albo MUTE

// Zabezpieczenia (rozdz. 15)
constexpr float BIAS_FAULT_V = -65.0f;            // mniej ujemna niz -65 V -> natychmiast FAULT
constexpr float IK_OVER_MA = 130.0f;
constexpr uint32_t IK_OVER_MS = 3000;
constexpr float IK_IDLE_MAX_MA = 70.0f;
constexpr uint32_t IK_IDLE_MS = 5000;
constexpr float IK_LOW_WARN_MA = 20.0f;
constexpr float PAIR_DIFF_WARN_MA = 5.0f;
constexpr float UA_WARN_LOW_V = 380.0f;
constexpr float UA_WARN_HIGH_V = 520.0f;
constexpr float UA_FAULT_LOW_V = 300.0f;
constexpr uint32_t UA_FAULT_MS = 500;
constexpr float HV_PRESENT_V = 50.0f;
constexpr float TEMP_WARN_C = 70.0f;
constexpr float TEMP_FAULT_C = 80.0f;
constexpr uint32_t MEAS_STALE_MS = 1000;
constexpr uint32_t MEAS_LOST_MS = 500;
constexpr uint32_t WDT_TIMEOUT_MS = 2000;

// Wznawianie po resecie w trakcie pracy
constexpr uint8_t MAX_AUTO_RESUME = 2;
constexpr uint32_t RESUME_CLEAR_PLAY_MS = 600000;  // 10 min PLAY bez resetu kasuje licznik

// NVS
constexpr uint32_t SETTINGS_SAVE_DELAY_MS = 10000;
constexpr uint32_t HOURS_SAVE_PERIOD_MS = 600000;

// Okresy zadan
constexpr uint32_t SAFETY_PERIOD_MS = 20;
constexpr uint32_t SEQ_PERIOD_MS = 10;
constexpr uint32_t MEAS_PERIOD_MS = 50;
constexpr uint32_t INPUT_PERIOD_MS = 10;
constexpr uint32_t BTN_DEBOUNCE_MS = 20;
constexpr uint32_t BTN_LONG_MS = 2000;
constexpr uint32_t TRIG_DEBOUNCE_MS = 100;
}  // namespace cfg
