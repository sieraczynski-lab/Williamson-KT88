#pragma once
#include <cstdint>

// Wyjscia ESP32 na ULN2803 plytki sterowania. Jedyne miejsce, ktore pisze te piny.
namespace relays {
enum Id : uint8_t { K1, K2, K3, K4, SOUND, UL, SPK, COUNT };

void init();  // wszystko OFF, wywolac jako pierwsze w setup()
void set(Id id, bool on);
bool get(Id id);
uint8_t mask();
void allOff();
void emergency();  // dzwiek OFF, kolumny do Marantza, K4/K3 OFF (zarzenie zostaje)
const char* name(Id id);
int fromName(const char* s);  // -1 gdy nieznana
}  // namespace relays
