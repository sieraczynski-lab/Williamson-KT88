# Uruchomienie krok po kroku

> ⚠️ Do 545 V DC. Pracuj jedną ręką, przed dotknięciem układu mierz napięcie na kondensatorach. R301 rozładowuje filtr w ok. minutę.

## Punkty pracy docelowe

| Stopień | Lampa | Ua | Ia | Ug | Uwagi |
|---|---|---|---|---|---|
| Wejście | ½ 6N2P (V1a) | ≈ 120 V | 1,5 mA | −0,5 V | katoda bez kondensatora, tu wchodzi NFB |
| Inwerter | ½ 6N2P (V1b) | ≈ 240 V | 1,5 mA | ≈ −1 V | katodyna, katoda ok. +120 V |
| Driver | 6N6P (V2a, V2b) | ≈ 200 V | 2× 12 mA | −8,5 V | P100 wyrównuje połówki |
| Końcówka | 2× KT88 UL | ≈ 445 V | 50 mA | −45…−55 V | 0,50 V na R125/R126 (10 Ω) |

## Kolejność

1. Sam zasilacz, bez lamp, przez **żarówkę w szereg** z siecią (albo autotransformator). Sprawdzić −90 V. Ustawić P201 i P202 w obu kanałach na maksimum ujemnego napięcia (ok. −64 V na suwaku).
2. Włożyć lampy. Zamiast głośnika **rezystor 8 Ω** (przy kolumnach 4 Ω: 4 Ω na odczepie 4 Ω). Sprzężenie zwrotne na razie odłączone (R127 rozpięty).
3. Po nagrzaniu sprawdzić napięcia z tabeli. Podnosić prąd KT88 potencjometrami P201 (V3) i P202 (V4) do **0,50 V na TP-A i TP-B**, z różnicą najwyżej ok. 10 mV (1 mA). To ważne przy toroidzie.
4. Podłączyć R127. Jeśli wzmocnienie wzrośnie zamiast spaść albo pojawi się wzbudzenie, zamienić końce uzwojenia wtórnego (gorący odczep z COM).
5. Generator 1 kHz: ustawić P100 na minimum zniekształceń albo na równe amplitudy na anodach V2a i V2b.
6. Prostokąt 1 kHz i 10 kHz na obciążeniu rezystancyjnym, potem z dołożonym kondensatorem 0,1–0,47 µF równolegle. Dobrać C100 tak, żeby nie było dzwonienia. Sprawdzić też zachowanie przy włączaniu i wyłączaniu (pompowanie membran = problem na dole pasma).
7. Po kilku godzinach grania i po pierwszych tygodniach ponownie wyrównać bias, bo nowe lampy się „układają”.

## Lista elementów zmienionych i nowych (na kanał)

| Ozn. | Wartość | Funkcja |
|---|---|---|
| V3, V4 | KT88, para dobrana | lampy mocy w UL |
| TR-OUT | toroidy.pl TTG-KT88PP | 4 kΩ, UL 43%, 80 W, wyjścia 4 i 8 Ω |
| R119, R120 | 220 kΩ 0,6 W | upływowe siatek KT88 (max dla stałego biasu) |
| R123, R124 | 1 kΩ 0,6 W | antyoscylacyjne g1, przy podstawce |
| R128, R129 | 220 Ω 1 W | antyoscylacyjne g2, przy podstawce |
| R125, R126 | 10 Ω 1% 1 W | pomiar prądu katody |
| C105, C106 | 330 nF / 630 V foliowy | sprzęgające driver → KT88 |
| P201, P202 | 10 kΩ cermet wieloobrotowy | regulacja biasu V3 i V4, ok. −39…−64 V |
| R130, R132 | 10 kΩ 0,6 W | górna część dzielnika biasu (od −90 V) |
| R131, R133 | 15 kΩ 0,6 W | dolna część dzielnika biasu (do masy) |
| C107, C108 | 10 µF / 100 V | odsprzęganie biasu, plus do masy |
| R201 / R202 | 1,8 kΩ 3 W / 13 kΩ 1 W | spadek 450 → 400 → 360 V (osobno w każdym kanale) |
| R127, C100 | 68 kΩ, 250 pF (start); przy odczepie 4 Ω R127 ≈ 47 kΩ | sieć sprzężenia zwrotnego |
| C102 | 47 µF / 550 V | odsprzęganie wejścia (w oryginale 450 V) |

## Zasilacz

- TR1 ok. 300 VA: 350 V/0,5 A, 70 V/0,1 A, 6,3 V/7 A (KT88), 6,3 V/3 A (lampy sterujące)
- mostek UF4007, filtr CLC: C1 100 µF, L1 5 H / 400 mA, C2 220 µF, wszystkie na 550 V
- bias: D5 1N4007, C5–R203–C6 (100 µF / 160 V, plus do masy), ok. −90 V
- żarzenie lamp sterujących podniesione do ok. +67 V (dzielnik 470 k / 82 k z +450 V), bo katoda katodyny jest na +120 V
- soft-start: NTC 10 Ω / 5 A, bezpiecznik T 2 A

Uzwojenie 350 V AC jest dobrane pod ok. 260 mA spoczynkowego poboru z obu kanałów. Na zimno węzły anodowe dochodzą do ok. 495 V, przy +10% w sieci do ok. 545 V. Stąd 550 V na elektrolitach (2× 400 V szeregowo z rezystorami wyrównującymi 220 k).
