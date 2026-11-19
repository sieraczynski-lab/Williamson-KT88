#include "commands.h"

#include <freertos/queue.h>

namespace commands {
namespace {
QueueHandle_t s_q = nullptr;
}

void init() { s_q = xQueueCreate(16, sizeof(Command)); }

bool post(Cmd cmd, int16_t a, int16_t b) {
  Command c{cmd, a, b};
  return s_q && xQueueSend(s_q, &c, 0) == pdTRUE;
}

bool receive(Command& out, TickType_t wait) { return s_q && xQueueReceive(s_q, &out, wait) == pdTRUE; }
}  // namespace commands
