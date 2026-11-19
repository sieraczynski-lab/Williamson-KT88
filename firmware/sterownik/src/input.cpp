#include "input.h"

#include <Arduino.h>

#include "commands.h"
#include "config.h"
#include "pins.h"

namespace input {
namespace {
struct Debounce {
  bool stable;
  bool last;
  uint32_t changed;
  // true, gdy stan ustalony sie zmienil
  bool update(bool raw, uint32_t now, uint32_t ms) {
    if (raw != last) {
      last = raw;
      changed = now;
    }
    if (raw != stable && now - changed >= ms) {
      stable = raw;
      return true;
    }
    return false;
  }
};
}  // namespace

void task(void*) {
  pinMode(pins::BTN_POWER, INPUT_PULLUP);
  pinMode(pins::TRIG_IN, INPUT_PULLUP);
  delay(5);

  const uint32_t t0 = millis();
  Debounce btn{false, false, t0};
  // trigger: stan przy starcie przyjety bez zbocza (wlacza dopiero narastajace zbocze)
  const bool trigNow = digitalRead(pins::TRIG_IN) == LOW;
  Debounce trig{trigNow, trigNow, t0};

  uint32_t pressedAt = 0;
  bool longSent = false;

  TickType_t last = xTaskGetTickCount();
  for (;;) {
    const uint32_t now = millis();

    if (btn.update(digitalRead(pins::BTN_POWER) == LOW, now, cfg::BTN_DEBOUNCE_MS)) {
      if (btn.stable) {
        pressedAt = now;
        longSent = false;
      } else if (!longSent) {
        commands::post(Cmd::POWER_TOGGLE);
      }
    }
    if (btn.stable && !longSent && now - pressedAt >= cfg::BTN_LONG_MS) {
      commands::post(Cmd::FAULT_ACK);  // dlugie nacisniecie: potwierdzenie alarmu
      longSent = true;
    }

    if (trig.update(digitalRead(pins::TRIG_IN) == LOW, now, cfg::TRIG_DEBOUNCE_MS))
      commands::post(trig.stable ? Cmd::TRIGGER_ON : Cmd::TRIGGER_OFF);

    vTaskDelayUntil(&last, pdMS_TO_TICKS(cfg::INPUT_PERIOD_MS));
  }
}
}  // namespace input
