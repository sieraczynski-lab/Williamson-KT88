// Williamson KT88 - sterownik (plytka "sterowanie", ESP32-S3)
// Zalozenia: docs/10-oprogramowanie-esp32.md. Etap 1: szkielet, kolejka komend, konsola, NVS, przekazniki.

#include <Arduino.h>
#include <Wire.h>

#include "commands.h"
#include "console.h"
#include "input.h"
#include "measure.h"
#include "pins.h"
#include "relays.h"
#include "safety.h"
#include "selector.h"
#include "sequencer.h"
#include "settings.h"
#include "state.h"

void setup() {
  relays::init();  // najpierw: wszystkie przekazniki OFF (kolumny na Marantzu, anody wylaczone)

  console::init();
  settings::load();
  state::init();
  commands::init();

  Wire.begin(pins::I2C_SDA, pins::I2C_SCL, 400000);
  Wire.setTimeOut(20);
  if (!selector::init()) console::logf("selektor MCP23017 0x20: brak odpowiedzi");

  measure::init();
  safety::init();
  sequencer::init();

  // rdzen 1: sterowanie; rdzen 0 zostaje dla WiFi (etap 7) i konsoli
  xTaskCreatePinnedToCore(safety::task, "safety", 4096, nullptr, 20, nullptr, 1);
  xTaskCreatePinnedToCore(sequencer::task, "sequencer", 6144, nullptr, 15, nullptr, 1);
  xTaskCreatePinnedToCore(measure::task, "measure", 4096, nullptr, 14, nullptr, 1);
  xTaskCreatePinnedToCore(input::task, "input", 3072, nullptr, 10, nullptr, 1);
  xTaskCreatePinnedToCore(console::task, "console", 6144, nullptr, 2, nullptr, 0);
}

void loop() { vTaskDelete(nullptr); }
