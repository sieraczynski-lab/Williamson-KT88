# 10. Oprogramowanie ESP32: założenia

Założenia do napisania programu sterownika (płytka `sterowanie`, ESP32-S3) dla Williamsona KT88. Opis sprzętu: [docs/soloist/03-sterowanie.md](soloist/03-sterowanie.md), selektor: [docs/soloist/11-selektor.md](soloist/11-selektor.md), różnice względem Soloista: [docs/09](09-integracja-soloist.md) (9.10). Połączenia: [pcb/CZYTAJ_MNIE.txt](../pcb/CZYTAJ_MNIE.txt).

Rzeczy oznaczone **[DECYZJA]** są do ustalenia przed pisaniem kodu (zebrane na końcu, rozdz. 17).

## 1. Zakres

| Funkcja | Krótko |
|---|---|
| Sekwencja włączania | miękki start (K1, K2), kontrola biasu, nagrzewanie, opóźnione anody (K3, K4), stabilizacja, zdjęcie MUTE, kolumny na lampę |
| Selektor i głośność | 4 wejścia, drabinka przekaźnikowa 0–63 dB, MUTE, limity głośności na wejście |
| Enkodery | głośność (istniejący) i selektor (drugi, nowy) |
| Pilot IR | wszystkie funkcje z frontu + strona punktu pracy + rzadkie ustawienia |
| Pomiary | prądy 4× KT88, szyna biasu, Ua, temperatura, poziom wysterowania L/P |
| Korekta biasu | automatyczna, w ciszy, małymi krokami |
| UL / trioda | przełączanie tylko przy wyłączonych anodach |
| Kolumny | Marantz ↔ lampa, trigger 12 V z Marantza |
| Wyświetlacze | 2 okrągłe LCD: wskaźniki wysterowania (VU) L i P, nakładki głośności i wejścia, punkt pracy, komunikaty |
| Zabezpieczenia | progi prądów i napięć, temperatura, watchdog, bezpieczny stan |
| Serwis | konsola USB, kalibracja, licznik godzin lamp, dziennik alarmów |

## 2. Sprzęt i przydział pinów

### 2.1 Co jest na płytce sterowania (bez zmian)

| Blok | Układ / pin | Uwagi |
|---|---|---|
| I²C | SDA GPIO8, SCL GPIO9 | 400 kHz |
| Prądy KT88 | ADS1115 0x48, A0–A3 = V5, V6, V7, V8 | spadek na R123/R124/R223/R224 (10 Ω 1 %) |
| Szyna biasu, Ua | ADS1115 0x49, A0 = VBIAS (J5-1, Bias-L Onyxa), A1 = HV_SENSE (J5-2) | **A2, A3 wolne** |
| Korekta biasu | MCP4728 0x60, kanały A–D = V5, V6, V7, V8 | wyjścia przez LM324 i przesuwniki do J10 |
| Selektor | MCP23017 0x20 (płytka selektora) | wejścia K1–K4, drabinka K5–K10, MUTE K11 |
| Przekaźniki | ULN2803: GPIO10–13 = K1–K4, GPIO14 = MUTE, GPIO17 = RLY_UL, GPIO18 = RLY_SPK | |
| Trigger | GPIO1 (TRIG_IN, 0 = 12 V obecne) | transoptor |
| Temperatura | DS18B20 na GPIO4 | pod płytką Onyxa, przy rzędzie KT88 |
| IR | TSOP38238 na GPIO5 | |
| Enkoder głośności | A GPIO6, B GPIO7, SW GPIO15 | |
| Przycisk | GPIO16 (BTN) | włącz / czuwanie |

### 2.2 Nowe (do dołączenia)

ESP32-S3-DevKitC-1 ma wolne piny tylko na prawej listwie, której płytka sterowania nie wyprowadza. Do czasu nowej wersji PCB: dolutować złącze (goldpin) do listwy modułu.

| Funkcja | Pin | Uwagi |
|---|---|---|
| Enkoder selektora A / B / SW | GPIO21 / GPIO47 / GPIO48 | GPIO48 lub GPIO38 zależnie od wersji DevKitC: na drugim jest dioda RGB, sprawdzić nadruk modułu |
| Wyświetlacz L (UART1) | TX GPIO41, RX GPIO42 | wariant A wyświetlaczy (2.3) |
| Wyświetlacz P (UART2) | TX GPIO39, RX GPIO40 | wariant A |
| Poziom L (VU) | GPIO2, ADC1 | 2.4 |
| Poziom P (VU) | GPIO3, ADC1 | pin strapping JTAG: bez znaczenia przy fabrycznych eFuse, sygnał musi mieć polaryzację 1,65 V, nie zwierać do masy |

Nie używać: GPIO0, 45, 46 (strapping), 19/20 (USB), 35–37 (PSRAM w wersji N16R8), 43/44 (konsola).

### 2.3 Wyświetlacze **[DECYZJA]**

Okrągły LCD 2,1" ma 480 × 480 pikseli i interfejs RGB (ok. 18 linii na wyświetlacz). Dwóch takich główny ESP32 nie obsłuży (brak pinów, pamięci i czasu na rysowanie przy pracy sterownika).

| Wariant | Co | Plusy | Minusy |
|---|---|---|---|
| **A (zalecany)** | 2 gotowe moduły **ESP32-S3 + okrągły dotykowy LCD 2,1" 480 × 480** (np. Waveshare ESP32-S3-Touch-LCD-2.1), każdy z własnym programem; sterownik wysyła im dane po UART | duży, ładny obraz (płynna wskazówka 50 fps), sterownik wolny od grafiki, **dotyk** (wywołanie punktu pracy bez przycisków), osobny program wyświetlaczy łatwo zmieniać | drugi program do napisania, dwa dodatkowe moduły (ok. 2× 40 USD), zasilanie 5 V ok. 2× 250 mA |
| B | 2× okrągły LCD 1,28" 240 × 240 GC9A01 (SPI) na wspólnej magistrali, rysowane przez sterownik (LVGL) | tanie, bez drugiego programu | mały (32 mm), bez dotyku, obciąża sterownik, 7 pinów |

Przy wariancie A: zasilanie modułów z 5 V płytki sterowania (sprawdzić wydajność przetwornicy U2, w razie potrzeby osobna 5 V / 1 A), masa wspólna, przewody UART skręcone z masą, z dala od anod. Wymiary i wycięcie we froncie drewnianym dopasować do modułu.

### 2.4 Sygnał do wskaźników wysterowania **[DECYZJA]**

Płytka sterowania nie ma wejścia sygnału audio, trzeba dołożyć mały układ (np. na płytce uniwersalnej obok sterowania), po jednym na kanał:

- źródło: odczep **4 Ω** toroidu (strona lampy, **przed** przekaźnikiem kolumn), względem masy wzmacniacza; wskaźnik pokazuje więc tylko lampę (w trybie Marantz wyświetlacze pokazują „MARANTZ”);
- dzielnik 100 kΩ / 5,1 kΩ do punktu 1,65 V (bufor albo 2× 1 kΩ + 10 µF z 3,3 V), 1 nF równolegle do 5,1 kΩ, diody BAT54S do 3,3 V i masy;
- skala: 45 W / 4 Ω = 13,4 V RMS (19 V szczytowo) → ok. ±0,93 V na ADC, zapas +3 dB do obcinania;
- ESP32: ADC1 w trybie ciągłym (DMA), 2 kanały po ok. 10 kS/s.

Alternatywa: detektor obwiedni (wzmacniacz operacyjny) na wolne wejścia ADS1115 0x49 A2/A3. Wolniejsze (ok. 400 próbek/s na kanał, dzielone z pomiarami biasu) i bez prawdziwego RMS, ale bez nowych pinów.

## 3. Platforma i architektura

- **pioarduino** (PlatformIO, Arduino core 3.x na ESP-IDF 5), płytka `esp32-s3-devkitc-1`, jak w zaleceniach selektora (11.1). Program wyświetlaczy (wariant A) w tym samym środowisku, grafika w **LVGL**.
- Zadania FreeRTOS:

| Zadanie | Priorytet | Okres | Zakres |
|---|---|---|---|
| `safety` | najwyższy | 20 ms | progi, stany awaryjne, watchdog sprzętowy (TWDT) |
| `sequencer` | wysoki | 10 ms | maszyna stanów (rozdz. 4), przekaźniki K1–K4, MUTE, UL, kolumny |
| `measure` | wysoki | ciągle | ADS1115 (kolejno 6 kanałów), DS18B20 co 2 s, filtry |
| `audio_level` | średni | blok 20 ms | ADC DMA → RMS, szczyt, wskazówka VU |
| `input` | średni | zdarzenia | enkodery (PCNT), przyciski, IR (RMT), trigger |
| `selector` | średni | kolejka | MCP23017: wejścia, drabinka, mute selektora |
| `bias_ctrl` | niski | 1 s | korekta biasu (rozdz. 6) |
| `display_link` | niski | 20 ms / 1 s | ramki do wyświetlaczy (rozdz. 12) |
| `console` | najniższy | zdarzenia | USB CDC: komendy serwisowe, log |
| `wifi` (opcja) | najniższy | | strona WWW / WebSocket, OTA |

- **Jedna kolejka komend** do `sequencer` i `selector`: enkoder, pilot, trigger i ewentualna aplikacja wysyłają komendy (`VOL_UP`, `INPUT_SET 2`, `MODE_TRIODE`, `POWER_OFF`…), nikt nie steruje przekaźnikami bezpośrednio.
- Stan całości w jednej strukturze (`AmpState`) chronionej muteksem; wyświetlacze i konsola tylko ją czytają.

## 4. Maszyna stanów i sekwencje

```
STANDBY ─(przycisk / IR POWER / trigger)→ MAINS ─1,5 s→ BYPASS ─→ BIAS_CHECK ─ok→ WARMUP ─45 s→ ANODES
   ↑                                                        │ błąd                                  │
   │                                                        ↓                                        ↓
   └──────────────── SHUTDOWN ←── (POWER / trigger off) ── PLAY ←── UNMUTE ←── STABILIZE ←── (K3, K4)
                         ↑                                    │
                       FAULT ←──────── każdy alarm ───────────┘        MODE_SWITCH (UL ↔ trioda): rozdz. 7
```

| Stan | Wejście | Robi | Wyjście |
|---|---|---|---|
| STANDBY | po zasileniu PS1 / po SHUTDOWN | wszystkie przekaźniki wyłączone, wyświetlacze wygaszone (albo zegar, opcja), sprawdza HV | przycisk, IR POWER, narastające 12 V triggera |
| MAINS | | K1 ON (TR1 przez R_SS), MUTE, selektor: tłumienie 63 dB | po 1,5 s |
| BYPASS | | K2 ON | od razu |
| BIAS_CHECK | | mierzy szynę biasu przez 2–5 s | −68…−92 V → WARMUP, inaczej FAULT („bias”) |
| WARMUP | | odlicza 45 s (pasek na wyświetlaczach), DAC korekty z NVS | 45 s i bias w normie |
| ANODES | | K3 ON, po 1,5 s K4 ON | Ua > 380 V w ciągu 10 s, inaczej FAULT („Ua”) |
| STABILIZE | | czeka, aż każda KT88 ma 35–75 mA stabilnie przez 5 s (max 60 s) | → UNMUTE, inaczej FAULT („prąd Vx”) |
| UNMUTE | | ustawia wejście i głośność (z limitem), MUTE OFF, kolumny na lampę (MUTE → RLY_SPK → 0,5 s → MUTE OFF), opcjonalnie narastanie głośności przez ok. 1 s | PLAY |
| PLAY | | normalna praca | komendy, alarmy |
| SHUTDOWN | | MUTE → RLY_SPK OFF (kolumny do Marantza) → K4, K3 OFF → 3 s → K2, K1 OFF, zapis NVS | STANDBY |
| FAULT | | jak SHUTDOWN, ale zostaje komunikat; ponowne włączenie dopiero po potwierdzeniu (przycisk / IR) | STANDBY |

- Po resecie ESP32 (np. watchdog) w trakcie pracy: start zawsze od bezpiecznego stanu (wszystko OFF), potem normalna sekwencja. Lampy są ciepłe, więc przy Ua < 50 V i krótkiej przerwie (< 2 min, znacznik w pamięci RTC) WARMUP można skrócić do 15 s.
- Komunikat „HV” na wyświetlaczach, dopóki Ua > 50 V przy wyłączonych anodach (rozładowanie).

## 5. Pomiary

| Wielkość | Źródło | Przeliczenie | Filtr / okres |
|---|---|---|---|
| I<sub>K</sub> V5–V8 | ADS1115 0x48, zakres ±1,024 V | I = U / R; R = 10 Ω albo zmierzona wartość z NVS (kalibracja) | mediana z 5 + średnia krocząca 2 s; co ok. 50 ms na kanał |
| Szyna biasu | ADS1115 0x49 A0 | współczynnik dzielnika z płytki sterowania (kalibracja multimetrem) | średnia 1 s |
| Ua | ADS1115 0x49 A1 | U<sub>a</sub> = U × (3 MΩ + 15 kΩ) / 15 kΩ ≈ 201 × U (kalibracja) | średnia 0,5 s |
| Temperatura | DS18B20 | °C | co 2 s |
| Poziom L/P | ADC1 GPIO2/3 (2.4) | U<sub>wy</sub> = (U<sub>ADC</sub> − U<sub>śr</sub>) / k; P = U<sub>RMS</sub>² / 4 Ω | rozdz. 11 |

- ADS1115: pomiar pojedynczy na kanał, 250–475 SPS, kolejno po kanałach. Odrzucać wyniki z nasyceniem.
- Wszystkie współczynniki kalibracji w NVS, ustawiane z konsoli albo z menu serwisowego.
- „Cisza” (do korekty biasu i alarmu spoczynkowego): poziom RMS obu kanałów poniżej −50 dB względem pełnej mocy przez co najmniej 30 s **oraz** MUTE albo głośność ≥ 50 dB tłumienia. Bez sygnału VU (wariant bez 2.4) tylko: MUTE albo prądy stabilne ±0,5 mA przez 60 s.

## 6. Automatyczna korekta biasu

- Cel: 52 mA na lampę (ustawialne 45–60 mA), różnica w parze < 1 mA. Tryb UL i trioda mają **osobne** zestawy wartości DAC w NVS.
- Zakres korekty przy dzielniku z płytki Onyxa: ok. ±3 mA (±0,3 V na siatce). Potencjometry Onyxa ustawiają bias zgrubnie, automat tylko dociąga.
- Algorytm (co 1 s, tylko w PLAY i w ciszy, nie wcześniej niż 10 min od włączenia, wcześniej tylko obserwacja):
  1. dla każdej lampy błąd e = I − I<sub>cel</sub>; ignoruj |e| < 0,3 mA (strefa martwa);
  2. najpierw wyrównaj parę (lampa z większym błędem), potem obie do celu;
  3. krok DAC najwyżej 1 LSB/s (ułamek mA), łącznie najwyżej 2 mA na włączenie;
  4. wynik zapisuj do NVS najwyżej co 10 min i przy wyłączeniu (oszczędzanie flash);
  5. DAC w 10 % od końca zakresu → ostrzeżenie „Vx: przestaw potencjometr / lampa do wymiany”.
- Przy starcie DAC z NVS (MCP4728 ma też EEPROM: wpisywać tylko przy zmianie o więcej niż kilka LSB).
- Tryb ustawiania (menu serwisowe): DAC na środek (ok. 1,65 V), wyłączona korekta, wyświetlacze pokazują prądy z rozdzielczością 0,1 mA → ręczne ustawienie potencjometrami 52 mA, potem włączenie automatu.
- Licznik godzin pracy lamp (czas z K3 ON), osobno dla KT88 i 6SN7 (kasowany przy wymianie).

## 7. UL / trioda

- Zmiana tylko przy wyłączonych anodach: MUTE → kolumny do Marantza → K4, K3 OFF → czekaj na Ua < 30 V (max 90 s, wyświetlacz pokazuje odliczanie i Ua) → RLY_UL (4 przekaźniki naraz) → ANODES → STABILIZE → UNMUTE.
- Wywołanie: pilot (przytrzymanie przycisku, potwierdzenie na wyświetlaczu) albo menu. Nie z enkodera w zwykłej obsłudze (żeby przypadkiem nie wyłączyć anod).
- Tryb zapamiętany w NVS, ustawiany przy każdym włączeniu przed ANODES.

## 8. Selektor i głośność

- Wejścia 1–4 z nazwami (NVS, np. „DAC”, „Marantz”, „CD”, „AUX”), dla każdego: korekta poziomu ±6 dB i **limit najmniejszego tłumienia** (docs/09, 9.9: DAC 2 V −10 dB, Marantz 1,2 V −5 dB, 1 V −4 dB).
- Zmiana wejścia: MUTE selektora → 50 ms → wszystkie K1–K4 OFF → wybrany ON → 100 ms → MUTE OFF. Nigdy dwa wejścia naraz.
- Zmiana głośności: najpierw załącz nowe bity drabinki, 5 ms, potem wyłącz zbędne (bez chwilowego skoku głośności).
- MUTE selektora: logika odwrócona (aktywne wyjście ULN = dźwięk), patrz selektor 7.5.
- Zapamiętane w NVS: wejście, głośność na wejście (opcja) albo wspólna, stan MUTE nie (zawsze start bez MUTE, ale z limitem i narastaniem).
- Po włączeniu głośność nie większa niż „bezpieczna startowa” (np. −30 dB) albo ostatnia, jeśli mniejsza.

## 9. Kolumny i trigger

- RLY_SPK OFF = kolumny na Marantzu (także przy awarii ESP32). Lampa przejmuje kolumny tylko w UNMUTE, każde wyjście z PLAY oddaje je od razu.
- Trigger 12 V: narastające zbocze → włączenie i wybór wejścia „Marantz” (pre-out, stała głośność, ustawiana w menu), opadające → SHUTDOWN. Ręczne wyłączenie przy obecnym triggerze: zostaje do następnego narastającego zbocza.
- Ręczny przełącznik kolumn Lampa / Marantz bez wyłączania lamp: komenda z pilota (z MUTE w trakcie).

## 10. Obsługa: enkodery, przycisk, pilot

### 10.1 Front (bez dodatkowych przycisków)

| Element | Krótko | Długo (≥ 2 s) | Obrót |
|---|---|---|---|
| Przycisk | włącz / wyłącz | (w FAULT) potwierdzenie alarmu | |
| Enkoder głośności | MUTE / zdejmij MUTE | **menu ustawień** (3 s) | głośność, z przyspieszeniem: wolno 1 dB, szybko 3–4 dB |
| Enkoder selektora | zatwierdź wejście od razu | **strona punktu pracy** | wybór wejścia: lista na wyświetlaczu, przełączenie po 1 s bez ruchu; za wejściem 4 pozycja „Status” (rozdz. 13) |

Enkodery czytane sprzętowo (PCNT), bez gubienia kroków; drgania styków przycisków filtrowane programowo (20 ms).

### 10.2 Pilot IR **[DECYZJA: jaki pilot]**

- Odbiór przez RMT, protokoły NEC, RC5, RC6 (pilot Marantza ma RC5). **Nauka pilota** z menu: kolejne funkcje na wyświetlaczu, naciśnij przycisk, kod zapisany w NVS. Dzięki temu można użyć wolnych przycisków pilota Marantza albo dowolnego innego.
- Funkcje: POWER, VOL+, VOL−, MUTE, IN1–IN4 i IN±, **INFO** (punkt pracy, kolejne strony), DISPLAY (jasność / wyłączenie wyświetlaczy), SPK (kolumny Lampa / Marantz), MODE (UL / trioda, przytrzymanie + potwierdzenie), MENU.
- Powtarzanie przy przytrzymaniu VOL± (co 150 ms, po 1 s szybciej).

## 11. Wskaźniki wysterowania (VU)

- Wyświetlacz lewy = kanał L, prawy = P. Do wyboru w menu: **wskazówka VU** (klasyczna skala), **słupek** z kropką szczytu, **waty** (skala 0,1–45 W, logarytmiczna).
- Obliczenia w `audio_level` co 20 ms na kanał: RMS z bloku, wartość szczytowa, wskazówka VU (filtr 2. rzędu: 99 % wskazania w 300 ms, przerzut ok. 1,5 %), pamięć szczytu 1,5 s, wskaźnik **obcinania** (szczyt > 95 % napięcia dla 45 W przez ≥ 3 próbki, czerwona dioda na tarczy przez 1 s).
- Wysyłka do wyświetlaczy 50 razy na sekundę: 2 bajty wskazówki, 2 bajty szczytu, bit obcinania. Animację wygładza wyświetlacz.
- Kalibracja „0 VU” w menu (np. 0 VU = 10 W albo = 1 W), kalibracja wzmocnienia toru pomiarowego z konsoli (sinus 1 kHz, miernik na 4 Ω).
- W trybie Marantz i przy MUTE: wskazówka w spoczynku, napis „MARANTZ” / „MUTE”.

## 12. Wyświetlacze: ekrany i komunikacja

### 12.1 Ekrany

| Ekran | Kiedy | Co |
|---|---|---|
| Czuwanie | STANDBY | wygaszone (opcja: przyciemniony zegar z NTP, jeśli WiFi) |
| Start | MAINS…STABILIZE | kroki sekwencji, odliczanie do anod, Ua, prądy lamp rosnące do celu |
| VU | PLAY | rozdz. 11; na dole tarczy mała nazwa wejścia i tryb UL/T |
| Nakładka głośności | przy zmianie, przez 3 s | duża liczba dB (np. „−32 dB”) na obu tarczach, łuk z położeniem |
| Nakładka wejścia | przy obracaniu selektora, do 3 s po wyborze | lista / nazwa wejścia |
| Punkt pracy | długie naciśnięcie selektora, INFO z pilota, dotyk (wariant A), pozycja „Status” selektora | rozdz. 13 |
| Komunikat | ostrzeżenie / alarm | tekst, kod, co zrobić; alarm czerwony do potwierdzenia |
| Menu | długie naciśnięcie głośności, MENU z pilota | rozdz. 14 |

- Jasność: ustawiana, automatyczne przyciemnienie po 5 min bez obsługi (opcja: wyłączenie wskazówek po 30 min ciszy).

### 12.2 Łącze z wyświetlaczami (wariant A)

- UART 921600 b/s, osobny port na każdy wyświetlacz, ramki COBS + CRC16.
- Sterownik → wyświetlacz: `LEVEL` (50 Hz), `STATE` (przy zmianie: stan, wejście, głośność, tryb, MUTE, kolumny), `OPPOINT` (1 Hz, gdy otwarta strona punktu pracy), `OVERLAY` (głośność / wejście), `MESSAGE`, `CONFIG` (styl tarczy, jasność, język).
- Wyświetlacz → sterownik: `HELLO` (wersja programu), `TOUCH` (stuknięcie, przytrzymanie, przesunięcie), `ACK`, co 1 s `HEARTBEAT`.
- Brak heartbeatu przez 5 s → ostrzeżenie w konsoli, wzmacniacz działa dalej (wyświetlacze nie są potrzebne do bezpiecznej pracy).
- Aktualizacja programu wyświetlaczy przez ich USB (opcja: przez sterownik).

## 13. Punkt pracy bez dodatkowych przycisków

Propozycja: kilka równoległych dróg, żadna nie wymaga nowego przycisku.

1. **Długie naciśnięcie enkodera selektora** (≥ 2 s) otwiera punkt pracy; obrót selektora przełącza strony, krótkie naciśnięcie albo 10 s bez ruchu wraca do VU. Najwygodniejsze na co dzień.
2. **Pozycja „Status” selektora**: po wejściu 4 obrót dalej pokazuje „Status” zamiast wejścia (dźwięk zostaje na bieżącym wejściu). Wygodne dla gości: nic się nie przełącza, tylko widać dane.
3. **Pilot: INFO** (kolejne naciśnięcia = kolejne strony).
4. **Dotyk tarczy** (wariant A): stuknięcie w tarczę L/P pokazuje punkt pracy tego kanału, drugie stuknięcie wraca.
5. **Automatycznie**: przez 10 s po stabilizacji przy każdym włączeniu oraz przy każdym ostrzeżeniu dotyczącym lamp.

Strony punktu pracy (na każdej tarczy dane jej kanału):

| Strona | Zawartość |
|---|---|
| Lampy | I<sub>K</sub> obu KT88 (mA, łuk z polem 50–55 mA), różnica w parze, korekta DAC w % zakresu |
| Zasilanie | Ua, szyna biasu, temperatura pod płytką |
| Stan | tryb UL/trioda, korekta automatyczna wł./wył., czas od włączenia |
| Lampy: historia | godziny pracy KT88 i 6SN7, ostatnie ostrzeżenia |

## 14. Menu ustawień

Rzadko używane, przez długie naciśnięcie enkodera głośności albo MENU z pilota; obrót wybiera, naciśnięcie zatwierdza, 30 s bez ruchu zamyka.

- Wejścia: nazwy, korekty poziomu, limity głośności, wejście dla triggera i jego stała głośność.
- Lampy: tryb UL / trioda, korekta biasu wł./wył., prąd docelowy, tryb ustawiania biasu (6), kasowanie liczników godzin.
- Wyświetlacze: styl wskaźnika, kalibracja 0 VU, jasność, przyciemnianie.
- Pilot: nauka kodów.
- Serwis: kalibracje (rezystory pomiarowe, dzielnik Ua, dzielnik biasu, tor VU), dziennik alarmów, przywrócenie ustawień fabrycznych.

## 15. Zabezpieczenia

| Warunek | Reakcja |
|---|---|
| Szyna biasu mniej ujemna niż −65 V | natychmiast MUTE, kolumny do Marantza, K3/K4 OFF, FAULT |
| I<sub>K</sub> dowolnej lampy > 130 mA średnio przez 3 s | FAULT |
| I<sub>K</sub> > 70 mA w ciszy przez 5 s | FAULT (także przerwany przewód korekty J10) |
| I<sub>K</sub> < 20 mA przy pozostałych w normie | ostrzeżenie: brak żarzenia / lampa zużyta |
| Różnica w parze > 5 mA w ciszy po korekcie | ostrzeżenie (toroid: podmagnesowanie rdzenia) |
| Ua < 380 V lub > 520 V w PLAY | ostrzeżenie; < 300 V → FAULT |
| Ua > 50 V przy wyłączonych anodach | komunikat „HV”, blokada przełączania UL/trioda |
| Temperatura > 70 °C / > 80 °C | ostrzeżenie / FAULT |
| Brak odpowiedzi ADS1115 / MCP4728 / MCP23017 | FAULT (pomiary) albo MUTE (selektor) |
| Reset / zawieszenie ESP32 | watchdog → reset → bezpieczny stan (wszystko OFF: kolumny na Marantzu, anody wyłączone) |

- Każde przejście w FAULT zapisuje wpis w dzienniku (NVS, ostatnie 32: czas pracy, kod, wartości).
- Programowe zabezpieczenia nie zastępują bezpieczników F1–F4.

## 16. Pamięć NVS, konsola, etapy

**NVS:** wejście, głośności, nazwy i limity wejść, tryb UL/T, DAC korekty (osobno UL i T), prąd docelowy, kalibracje, kody pilota, ustawienia wyświetlaczy, liczniki godzin, dziennik alarmów.

**Konsola USB** (komendy tekstowe): `status`, `meas` (strumień pomiarów), `relay K3 on` (tylko w trybie serwisowym bez anod), `dac 0 2048`, `cal ua 465.2`, `cal ik 0 10.03`, `log`, `nvs reset`.

**Etapy:**
1. Szkielet: zadania, kolejka komend, konsola, NVS, przekaźniki na stole (diody zamiast cewek).
2. Pomiary (ADS1115, DS18B20) z napięciami z zasilacza laboratoryjnego, kalibracja.
3. Sekwencja i zabezpieczenia na płytce zasilacza bez lamp (żarówka w szeregu, Ua bez obciążenia).
4. Selektor, enkodery, pilot.
5. Pierwsze uruchomienie z lampami: ręczny bias, potem korekta automatyczna.
6. Wskaźniki VU i wyświetlacze, punkt pracy, menu.
7. Opcje: WiFi (strona WWW, OTA), zegar.

## 17. Do ustalenia **[DECYZJA]**

1. Wyświetlacze: wariant A (2 moduły ESP32-S3 + LCD 2,1" dotykowy) czy B (GC9A01 1,28" SPI)?
2. Sygnał VU: dzielnik na ADC ESP32 (2.4) czy detektor obwiedni na ADS1115?
3. Drugi enkoder: piny z prawej listwy DevKitC (dolutowane złącze) czy nowa wersja płytki sterowania?
4. Pilot: pilot Marantza (nauka kodów) czy osobny?
5. Przycisk włączania na froncie zostaje (jak w Soloiście)?
6. WiFi: potrzebne (strona WWW, aktualizacja bez otwierania obudowy)? Zasięg osłabia ekran nad płytką sterowania.
7. Skala VU: 0 VU = ile watów?
