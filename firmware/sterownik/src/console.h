#pragma once

// Konsola USB CDC (docs/10, rozdz. 16). Wszystkie wydruki ida przez out()/logf().
namespace console {
void init();
void task(void*);
void out(const char* fmt, ...) __attribute__((format(printf, 1, 2)));
void logf(const char* fmt, ...) __attribute__((format(printf, 1, 2)));  // ze znacznikiem czasu
}  // namespace console
