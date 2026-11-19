#pragma once

// Pomiary (docs/10, rozdz. 5). Etap 1: tylko symulacja (BENCH_SIM), bez niej pomiary sa niewazne.
// Etap 2: ADS1115 0x48 (prady), 0x49 (bias, Ua), DS18B20.
namespace measure {
void init();
void task(void*);

#ifdef BENCH_SIM
// what: "bias", "ua", "ik" (idx 0..3), "temp"; NAN = wroc do modelu
bool simSet(const char* what, int idx, float value);
void simClear();
void simLost(bool lost);
void simPrint();
#endif
}  // namespace measure
