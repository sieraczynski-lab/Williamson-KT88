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

| Uzwojenie | Napięcie | Prąd | Zastosowanie |
|---|---|---|---|
| Pierwotne | 230 V / 50 Hz | – | sieć |
| Anodowe | 350 V AC | 0,5 A | mostek + CLC → ok. 450 V przy ok. 245 mA |
| Bias | 70 V AC | 0,1 A | jednopołówkowo → ok. −90 V |
| Żarzenie KT88 | 6,3 V AC | 7 A | 4× KT88 = 6,4 A |
| Żarzenie lamp sterujących | 6,3 V AC | 3 A | 2× 6SL7 + 2× 6SN7 = 1,8 A, podniesione do +67 V |

- Moc ok. **300 VA** (obciążenie realne ok. 245 VA).
- **Ekran elektrostatyczny** między pierwotnym a wtórnymi.
- Izolacja uzwojenia anodowego na co najmniej 1,5 kV. Napięcie szczytowe na kondensatorach to ok. 495 V, a przy +10% w sieci ok. 545 V.
- Duży toroid ma wysoki prąd załączenia: w zasilaczu jest NTC 10 Ω / 5 A i bezpiecznik zwłoczny T 2 A. Zapytać producenta o zalecany bezpiecznik.
- Toroid sieciowy może buczeć przy składowej stałej w sieci. Jeśli wystąpi, pomaga prosty filtr DC (DC blocker) na pierwotnym.

## 3. Dławik filtru anodowego: 1 szt.

| Parametr | Wartość |
|---|---|
| Indukcyjność | 5 H |
| Prąd DC | 300 mA (pobór ok. 245 mA) |
| Rezystancja DC | możliwie mała, najlepiej poniżej ok. 80 Ω (każde 10 Ω to ok. 2,5 V mniej na B+) |
| Izolacja | min. 1,5 kV do rdzenia |

Dławik może być na rdzeniu EI ze szczeliną, bo płynie przez niego prąd stały. Toroid bez szczeliny się tu nie nadaje, chyba że producent zaproponuje rdzeń z przerwą.

## Opcja na przyszłość: łagodniejsze obciążenie w dołku kolumn

Jeśli po odsłuchu dołek 2,5 Ω przy 160 Hz okaże się problemem, można zamówić transformator głośnikowy o wyższej impedancji, np. 5–6,6 kΩ. Taki miał Onyx: Hammond 1650HA, 6,6 kΩ. Wtedy trzeba przeliczyć punkt pracy KT88 i sprzężenie zwrotne.
