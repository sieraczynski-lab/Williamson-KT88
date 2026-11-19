#pragma once
#include <cstdint>

#include "types.h"

// Maszyna stanow (docs/10, rozdz. 4, 7, 8, 9). Jedyny wlasciciel przekaznikow (poza awaryjnym
// wylaczeniem z safety) i selektora.
namespace sequencer {
void init();  // po settings::load(): odczyt NVS, powod resetu, ewentualne wznowienie
void task(void*);

// Wolane z dowolnego zadania: natychmiast relays::emergency() i wyciszenie,
// reszte wylaczania robi sequencer w nastepnym kroku (faza FAULT).
void raiseFault(Fault f, int8_t tube, float value);
}  // namespace sequencer
