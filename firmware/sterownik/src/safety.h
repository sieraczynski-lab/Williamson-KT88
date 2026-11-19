#pragma once

// Zabezpieczenia (docs/10, rozdz. 15) i watchdog zadan (TWDT).
// Programowe zabezpieczenia nie zastepuja bezpiecznikow F1-F4.
namespace safety {
void init();  // konfiguracja TWDT, przed startem zadan
void task(void*);
}  // namespace safety
