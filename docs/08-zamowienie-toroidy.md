# Specyfikacja do zamówienia w toroidy.pl

toroidy.pl wykonują transformatory na zamówienie, więc wszystkie trzy elementy indukcyjne można zamówić w jednym miejscu. Poniższe parametry wynikają ze szkicu 2. Przed zamówieniem warto je potwierdzić z producentem i podać mu punkt pracy.

## 1. Transformator głośnikowy: 2 szt.

Baza: **TTG-KT88PP** (4 kΩ, UL 43%, 80 W).

| Parametr | Wartość |
|---|---|
| Lampy | 2× KT88 push-pull, ultralinear |
| Raa | 4 kΩ z odczepem środkowym |
| Odczepy UL | 43% |
| Prąd spoczynkowy | ok. 2× 50–55 mA (anoda + siatka druga) |
| Napięcie anodowe | ok. 450 V |
| Moc | 80 W |
| Uzwojenie wtórne | **2, 4 i 8 Ω** (prośba o dodatkowy odczep 2 Ω) |

Pytania do producenta:
- ile mA niezrównoważenia DC rdzeń znosi bez wyraźnego wzrostu zniekształceń na basie,
- czy dodatkowy odczep 2 Ω zmienia pasmo lub indukcyjność rozproszenia.

Odczep 2 Ω jest do porównania na słuch z kolumnami 4 Ω. Lampy widzą wtedy ok. 8 kΩ nominalnie i ok. 5 kΩ w dołku przy 160 Hz, kosztem mocy (ok. 25–30 W). Sprzężenie zwrotne zawsze z odczepu, do którego podłączone są kolumny. Przy odczepie 2 Ω R127 trzeba zmniejszyć ok. √2 razy, do ok. 15 k.

## 2. Transformator sieciowy: 1 szt.

Płytka Onyxa ma zasilacz anodowy osobno dla każdego kanału (mostek, filtr, dławik) i własny prostownik biasu, a oba mostki zasila się z jednego uzwojenia. Płytka zasilacza ([09](09-integracja-soloist.md)) podaje na nie tylko napięcia przemienne. Pobór: ok. 145 mA na kanał (2× KT88 po 50–55 mA, siatki drugie, front end ok. 18 mA, dzielniki), razem ok. 290 mA.

| Uzwojenie | Napięcie (pod obciążeniem) | Prąd | Zastosowanie |
|---|---|---|---|
| Pierwotne | 230 V | – | ekran elektrostatyczny do PE |
| S1 anodowe | **360 V, odczepy 345 V i 375 V** | 0,65 A | J103 i J203 → Ua ok. 450–470 V |
| S4 bias | **58 V** | 100 mA | J106 i J206 → ok. −80 V (dzielniki z płytki biorą ok. 15 mA DC) |
| S2 żarzenie KT88 | 6,3 V | 8 A | J105 i J205, 4× KT88 = 6,4 A |
| S3 żarzenie 6SN7 | 6,3 V | 3 A | J104 i J204, 4× 6SN7 = 2,4 A |

Moc **400 VA**. Prąd 0,65 A na S1 wynika z prostownika z filtrem pojemnościowym (prąd skuteczny ok. 1,8–2× prąd stały).

Porównanie z transformatorem Onyxa (TSTA-0300/001: 400 V / 0,3 A, 2× 70 V, 3× 6,3 V / 6,6 A): jego 400 V dawało Ua ok. 530–550 V, dobre dla Hammonda 6,6 kΩ. Toroid 4 kΩ potrzebuje ok. 465 V, stąd 360 V. 0,3 A na S1 to za mało na cztery KT88 przy 50–55 mA, a jedno 6,3 V / 6,6 A nie wystarczy na 4× KT88 i 4× 6SN7 (8,8 A).

Uwagi do zamówienia:
- zmierz napięcie sieci u siebie i podaj je producentowi (każde +5 V sieci to ok. +10 V Ua);
- poproś o napięcia bez obciążenia; S1 bez obciążenia ok. 380–390 V, czyli ok. 540 V szczytowo na kondensatorach przed wlutowaniem lamp (C119–C122 Onyxa: 2× 400 V szeregowo, zapas jest);
- obniżona indukcja (cichszy rdzeń, mniejsze pole rozproszenia);
- odczepy S1 wyprowadzone osobnymi przewodami, izolacja 1,5 kV między S1 a resztą.

## 3. Dławiki filtru anodowego: 2 szt.

Na płytce są dwa złącza dławików, L106 i L206, **po jednym na kanał**. Osobne dławiki dają lepszą separację kanałów, a każdy jest mniejszy niż jeden wspólny.

| Parametr | Wartość |
|---|---|
| Indukcyjność | 10 H (wg Onyxa) |
| Prąd DC | min. 200 mA (pobór ok. 145 mA na kanał; Onyx dał 400 mA) |
| Rezystancja DC | możliwie mała, najlepiej poniżej ok. 100 Ω (każde 10 Ω to ok. 1,5 V mniej Ua) |
| Izolacja | min. 1,5 kV do rdzenia |
| Rdzeń | EI ze szczeliną (płynie prąd stały), nie toroid bez szczeliny |

## Opcja na przyszłość: łagodniejsze obciążenie w dołku kolumn

Jeśli po odsłuchu dołek 2,5 Ω przy 160 Hz okaże się problemem, można zamówić transformator głośnikowy o wyższej impedancji, np. 5–6,6 kΩ. Taki miał Onyx: Hammond 1650HA, 6,6 kΩ. Wtedy trzeba przeliczyć punkt pracy KT88 i sprzężenie zwrotne.
