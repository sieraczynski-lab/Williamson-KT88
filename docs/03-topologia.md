# Topologia: Williamson, Mullard 5-20, 6S33S, 6SN7

## Williamson a Mullard 5-20

Williamson (D.T.N. Williamson, „Wireless World”, 1947) pokazał, że lampowiec może mieć zniekształcenia ok. 0,1%. Mullard 5-20 (broszura Mullarda, połowa lat 50.) to jego uproszczony następca, zaprojektowany tak, by dało się go zbudować taniej i pewniej.

| | Williamson | Mullard 5-20 |
|---|---|---|
| Liczba stopni | 4 (wejście, inwerter, driver, końcówka) | 3 (wejście, inwerter, końcówka) |
| Stopień wejściowy | trioda (6SN7, tu 6N2P) | pentoda EF86 |
| Inwerter fazy | katodyna, bez wzmocnienia | long-tail pair na ECC83, ze wzmocnieniem |
| Driver | osobny stopień różnicowy (6SN7, tu 6N6P) | brak, inwerter steruje końcówką |
| Końcówka (oryginał) | KT66 triodowo, ok. 15 W | EL34 UL, ok. 20 W |
| Sprzężenie zwrotne | ok. 20 dB | ok. 30 dB |

Najważniejsze różnice:

- **Stabilność.** W Williamsonie pętla obejmuje cztery stopnie i transformator, więc ma więcej biegunów. Jest bardziej wrażliwy na transformator, skłonny do oscylacji i „motorboatingu”. Mullard łatwiej ustabilizować.
- **Sterowanie końcówką.** Osobny driver Williamsona daje duży zapas amplitudy, co przydaje się przy KT88 (ok. 50 V szczytowo na siatce). W Mullardzie przy KT88 inwerter na ECC83 bywa na granicy.
- **Wejście.** EF86 daje dużo wzmocnienia, ale szumi i mikrofonuje. Trioda jest cicha i bezproblemowa.

## 6S33S a KT88

Obie wersje Onyxa mają ten sam front end. Różnią się końcówką i to ona decyduje o charakterze.

| | 6S33S (wersja 2020) | KT88 UL (wersja 2023) |
|---|---|---|
| Typ | trioda o bardzo niskim Ri | tetroda strumieniowa w UL |
| Punkt pracy | ok. 160 V, 200 mA na lampę | ok. 445 V, 50 mA na lampę |
| Transformator | 1 kΩ (LO PP80-3) | 4 kΩ |
| Żarzenie | 6,6 A na lampę | 1,6 A na lampę |
| Mocne strony | bardzo niska impedancja wyjściowa, kontrola głośnika, liniowość, bliżej oryginału (triody) | więcej mocy, wyższa sprawność, mniej ciepła, łatwo dostępne lampy |
| Słabe strony | ciepło, niska sprawność, lampy tylko z zapasów (wojskowe) | wyższa impedancja wyjściowa, wyższe napięcia, przy toroidzie konieczny balans DC |

To nie jest wersja „ulepszona”, tylko inna: KT88 to praktyczniejszy wzmacniacz na co dzień, a 6S33S lepiej radzi sobie z trudną impedancją kolumn.

## 6SN7 a 6N2P / 6N6P

W oryginalnym Williamsonie wszystkie stopnie sterujące były na 6SN7. Onyx zastąpił je lampami nowalowymi.

| | 6SN7 | 6N2P | 6N6P |
|---|---|---|---|
| Cokół | oktal | nowal | nowal |
| μ | ok. 20 | ok. 97 | ok. 20 |
| Ri | ok. 7,7 kΩ | ok. 50 kΩ | ok. 1,8 kΩ |
| Nachylenie | ok. 2,6 mA/V | ok. 2 mA/V | ok. 11 mA/V |
| Moc anody (na triodę) | 3,5–5 W | 1 W | 4,8 W |
| Żarzenie 6,3 V | 0,6 A | 0,34 A | 0,75 A |
| Odpowiednik | 6N8S, w przybliżeniu ECC82 | ECC83 / 12AX7 | najbliżej 5687 |

- **Wejście:** 6N2P wzmacnia ok. 50×, 6SN7 ok. 15×. Więcej wzmocnienia to głębsze sprzężenie zwrotne i lepsza czułość.
- **Driver:** 6N6P ma ok. 4× mniejsze Ri i pracuje przy 12 mA, więc łatwiej wysterowuje pojemność wejściową KT88 i ma większy zapas amplitudy.
- 6SN7 **nie da się wstawić bezpośrednio** (inny cokół, piny i punkty pracy). Jeśli już, to sensownie tylko w driverze (ok. 7–8 mA, przeliczone rezystory), z wejściem pozostawionym na 6N2P.
