# Sterownik ESP32-S3: program

Program płytki `sterowanie` (ESP32-S3-DevKitC-1 N16R8). Założenia: [docs/10-oprogramowanie-esp32.md](../../docs/10-oprogramowanie-esp32.md).

**Stan: etap 1** (rozdz. 16): szkielet, zadania, kolejka komend, maszyna stanów, zabezpieczenia, NVS, konsola USB, przekaźniki. Pomiary są na razie tylko symulowane.

## Budowanie

PlatformIO z platformą **pioarduino** (Arduino core 3.x, ESP-IDF 5.x). Projekt ma własny katalog PlatformIO (`core_dir = %USERPROFILE%\.platformio-pioarduino`). pioarduino instaluje do niego własne pakiety Pythona i fork PlatformIO Core, więc nie miesza w środowisku innych projektów.

| Środowisko | Do czego |
|---|---|
| `bench` (domyślne) | test na stole: diody zamiast cewek, pomiary z modelu, ustawiane komendą `sim` |
| `amp` | wzmacniacz, tylko prawdziwe pomiary. Do etapu 2 (ADS1115) włączenie kończy się alarmem „brak pomiarów”, i tak ma być |

```
pio run -e bench -t upload
pio device monitor
```

Flaga `MUTE_VIA_GPIO14` w `platformio.ini` wybiera sterowanie K11 selektora (selektor 7.5): `1` = przez GPIO14 i J6 pin 3 (fail-safe przy zawieszeniu ESP32), `0` = przez GPB2 MCP23017.

## Budowa programu

| Plik | Zadanie | Zakres |
|---|---|---|
| `sequencer.cpp` | `sequencer`, 10 ms | maszyna stanów (rozdz. 4), UL/trioda (7), selektor (8), kolumny i trigger (9); jedyny właściciel przekaźników |
| `safety.cpp` | `safety`, 20 ms, najwyższy priorytet | progi z rozdz. 15, watchdog zadań (TWDT 2 s → reset → wszystko OFF) |
| `measure.cpp` | `measure`, 50 ms | etap 1: model wzmacniacza (`bench`); etap 2: ADS1115, DS18B20 |
| `input.cpp` | `input`, 10 ms | przycisk (krótko: wł./wył., długo: potwierdzenie alarmu), trigger 12 V |
| `console.cpp` | `console` | komendy USB, `help` |
| `selector.cpp` | | MCP23017: wejścia, drabinka z nakładaniem bitów, K11 |
| `settings.cpp` | | NVS: ustawienia (zapis 10 s po zmianie), liczniki godzin (co 10 min), dziennik 32 alarmów |
| `config.h` | | wszystkie progi i czasy z dokumentu |

Przycisk, trigger i konsola tylko wysyłają komendy do kolejki. Alarm z `safety` od razu wyłącza dźwięk, kolumny i anody (`relays::emergency()`), resztę wyłączania robi sekwencer.

## Test na stole (etap 1)

```
on                 sekwencja: MAINS → BIAS_CHECK → WARMUP 45 s → ANODES → STABILIZE → UNMUTE → PLAY
meas on            strumień pomiarów z modelu
sim ik 2 140       V6 = 140 mA → po 3 s FAULT „prąd lampy > 130 mA”
ack                potwierdzenie alarmu
sim auto
mode triode        w PLAY: anody OFF, czekanie na Ua < 30 V, przełączenie, ponowny start anod
sim bias -50       zanik biasu → natychmiast FAULT
trig on / trig off włączenie i wyłączenie triggerem (wejście „Marantz”, stała głośność)
log                dziennik alarmów
```

## Do zrobienia

- Etap 2: ADS1115 (0x48 prądy, 0x49 bias/Ua), DS18B20, filtry, komendy `cal`.
- Etap 4: enkodery (PCNT), pilot (RMT, nauka kodów).
- Etap 5: korekta biasu (MCP4728), tryb ustawiania biasu.
- Etap 6: VU (ADC DMA), łącze z wyświetlaczami, punkt pracy, menu.
- Przycisk BTN (GPIO16) jest przyjęty jako zwierany do masy: sprawdzić na płytce.
