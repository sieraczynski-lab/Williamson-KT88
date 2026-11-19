#pragma once
#include <cstdint>

// Plytka selektora: MCP23017 0x20 (docs/soloist/11-selektor.md, rozdz. 7).
// Tylko sprzet; kolejnosc wyciszania przy przelaczaniu robi sequencer.
namespace selector {
bool init();  // konfiguracja wyjsc: brak wejscia, tlumienie 63 dB, cisza. false = brak odpowiedzi
bool ok();
bool setSound(bool on);   // K11: on = dzwiek (GPIO14 albo GPB2, patrz MUTE_VIA_GPIO14)
bool setInput(int idx);   // 0..3, -1 = zadne; najpierw wszystkie OFF, potem wybrane
bool setAtt(uint8_t code);  // kod drabinki 0..63 = tlumienie dB, z nakladaniem (bez skoku glosnosci)
uint8_t att();
int input();
}  // namespace selector
