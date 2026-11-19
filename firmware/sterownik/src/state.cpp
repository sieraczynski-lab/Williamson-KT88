#include "state.h"

#include <freertos/FreeRTOS.h>
#include <freertos/semphr.h>

#include "relays.h"

namespace state {
namespace {
AmpState s_state;
SemaphoreHandle_t s_mtx = nullptr;
}  // namespace

void init() { s_mtx = xSemaphoreCreateMutex(); }
void lock() { xSemaphoreTake(s_mtx, portMAX_DELAY); }
void unlock() { xSemaphoreGive(s_mtx); }
AmpState& raw() { return s_state; }

AmpState get() {
  lock();
  AmpState copy = s_state;
  unlock();
  copy.relays = relays::mask();
  return copy;
}
}  // namespace state
