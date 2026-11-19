#pragma once
#include <freertos/FreeRTOS.h>

#include <cstdint>

// Jedna kolejka komend (docs/10, rozdz. 3): przycisk, trigger, konsola, pozniej enkodery,
// pilot i WWW tylko wysylaja komendy. Przekaznikami steruje wylacznie sequencer.
enum class Cmd : uint8_t {
  POWER_TOGGLE,
  POWER_ON,      // a = 1: wlaczenie triggerem
  POWER_OFF,
  FAULT_ACK,
  VOL_SET,       // a = tlumienie dB
  VOL_STEP,      // a = dB glosniej (ujemne = ciszej)
  INPUT_SET,     // a = 0..3
  INPUT_STEP,    // a = +1 / -1
  MUTE_TOGGLE,
  MUTE_SET,      // a = 0/1
  MODE_SET,      // a = 0 UL, 1 trioda
  SPK_SET,       // a = 1 lampa, 0 Marantz
  TRIGGER_ON,
  TRIGGER_OFF,
  SERVICE_SET,   // a = 0/1
  RELAY_SET,     // a = relays::Id, b = 0/1 (tylko tryb serwisowy)
};

struct Command {
  Cmd cmd;
  int16_t a;
  int16_t b;
};

namespace commands {
void init();
bool post(Cmd cmd, int16_t a = 0, int16_t b = 0);
bool receive(Command& out, TickType_t wait);
}  // namespace commands
