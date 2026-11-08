# Uruchomienie krok po kroku

> ⚠️ Do 545 V DC. Pracuj jedną ręką, przed dotknięciem układu mierz napięcie na kondensatorach. R301 rozładowuje filtr w ok. minutę.

## Punkty pracy docelowe

| Stopień | Lampa | Ua | Ia | Ug | Uwagi |
|---|---|---|---|---|---|
| Wejście | ½ 6SL7 / 6N9S (V1a) | ≈ 133 V | 1,0 mA | −1,0 V | katoda bez kondensatora, tu wchodzi NFB |
| Inwerter | ½ 6SL7 / 6N9S (V1b) | ≈ 266 V | 1,2 mA | ≈ −0,9 V | katodyna, katoda ok. +134 V |
| Driver | 6SN7 / 6N8S (V2a, V2b) | ≈ 234 V | 2× 8 mA | −7,5 V | P100 wyrównuje połówki |
| Końcówka | 2× KT88 UL | ≈ 445 V | 50 mA | −45…−55 V | 0,50 V na R125/R126 (10 Ω) |

## Kolejność

1. Sam zasilacz, bez lamp, przez **żarówkę w szereg** z siecią (albo autotransformator). Sprawdzić −90 V. Ustawić P201 i P202 w obu kanałach na maksimum ujemnego napięcia (ok. −64 V na suwaku).
2. Włożyć lampy. Zamiast głośnika **rezystor 4 Ω na odczepie 4 Ω**. Sprzężenie zwrotne na razie odłączone (R127 rozpięty).
3. Po nagrzaniu sprawdzić napięcia z tabeli. Podnosić prąd KT88 potencjometrami P201 (V3) i P202 (V4) do **0,50 V na TP-A i TP-B**, z różnicą najwyżej ok. 10 mV (1 mA). To ważne przy toroidzie.
4. Podłączyć R127. Jeśli wzmocnienie wzrośnie zamiast spaść albo pojawi się wzbudzenie, zamienić końce uzwojenia wtórnego (gorący odczep z COM).
5. Generator 1 kHz: ustawić P100 na minimum zniekształceń albo na równe amplitudy na anodach V2a i V2b.
6. Prostokąt 1 kHz i 10 kHz na obciążeniu rezystancyjnym, potem z dołożonym kondensatorem 0,1–0,47 µF równolegle. Dobrać C100 tak, żeby nie było dzwonienia. Sprawdzić też zachowanie przy włączaniu i wyłączaniu (pompowanie membran = problem na dole pasma).
7. Po kilku godzinach grania i po pierwszych tygodniach ponownie wyrównać bias, bo nowe lampy się „układają”.

## Lista elementów zmienionych i nowych (na kanał)

| Ozn. | Wartość | Funkcja |
|---|---|---|
| V1 | 6SL7GT / 6N9S | wejście i katodyna |
| V2 | 6SN7GT / 6N8S | driver różnicowy |
| V3, V4 | KT88, para dobrana | lampy mocy w UL |
| R103 | 1 kΩ 0,6 W | katoda V1a, wejście NFB |
| R105 / R102 | 47 kΩ 1 W / 220 kΩ 1 W | odsprzęganie i obciążenie anody V1a |
| R104, R106 | 110 kΩ 1 W | obciążenia katodyny |
| C103, C104 | 470 nF / 630 V foliowy | sprzęgające katodyna → driver |
| R107, R108 | 470 kΩ 0,6 W | upływowe siatek drivera |
| R113, R114 | 22 kΩ 3 W | obciążenia anod drivera |
| R112, P100 | 390 Ω 1 W, 100 Ω | wspólna katoda drivera, balans AC |
| TR-OUT | toroidy.pl TTG-KT88PP | 4 kΩ, UL 43%, 80 W, wyjścia 4 i 8 Ω |
| R119, R120 | 220 kΩ 0,6 W | upływowe siatek KT88 (max dla stałego biasu) |
| R123, R124 | 1 kΩ 0,6 W | antyoscylacyjne g1, przy podstawce |
| R128, R129 | 220 Ω 1 W | antyoscylacyjne g2, przy podstawce |
| R125, R126 | 10 Ω 1% 1 W | pomiar prądu katody |
| C105, C106 | 100 nF / 630 V foliowy | sprzęgające driver → KT88 (biegun ok. 7 Hz) |
| P201, P202 | 10 kΩ cermet wieloobrotowy | regulacja biasu V3 i V4, ok. −39…−64 V |
| R130, R132 | 10 kΩ 0,6 W | górna część dzielnika biasu (od −90 V) |
| R131, R133 | 15 kΩ 0,6 W | dolna część dzielnika biasu (do masy) |
| C107, C108 | 10 µF / 100 V | odsprzęganie biasu, plus do masy |
| R201 / R202 | 2,2 kΩ 2 W / 4,7 kΩ 1 W | spadek 450 → 410 → 400 V (osobno w każdym kanale) |
| R127, C100 | 22 kΩ, 180 pF (start) | sprzężenie zwrotne z odczepu 4 Ω |
| C102 | 47 µF / 550 V | odsprzęganie wejścia (w oryginale 450 V) |

## Zasilacz

- TR1 ok. 300 VA: 350 V/0,5 A, 70 V/0,1 A, 6,3 V/7 A (KT88), 6,3 V/3 A (lampy sterujące)
- mostek UF4007, filtr CLC: C1 100 µF, L1 5 H / 400 mA, C2 220 µF, wszystkie na 550 V
- bias: D5 1N4007, C5–R203–C6 (100 µF / 160 V, plus do masy), ok. −90 V
- żarzenie lamp sterujących (6SL7 + 6SN7, 1,8 A) podniesione do ok. +67 V (dzielnik 470 k / 82 k z +450 V), bo katoda katodyny jest na +134 V
- soft-start: NTC 10 Ω / 5 A, bezpiecznik T 2 A

Uzwojenie 350 V AC jest dobrane pod ok. 260 mA spoczynkowego poboru z obu kanałów. Na zimno węzły anodowe dochodzą do ok. 495 V, przy +10% w sieci do ok. 545 V. Stąd 550 V na elektrolitach (2× 400 V szeregowo z rezystorami wyrównującymi 220 k).
