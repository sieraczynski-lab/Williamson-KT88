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

## Wybór lamp sterujących dla tego projektu

Płytka Onyxa w wersji KT88 (VA1523) ma **wyłącznie podstawki oktalowe**: V1 (wejście + katodyna w jednej lampie), V2 (driver) i dwie KT88 na kanał. 6N2P i 6N6P odpadają, więc front end jest przeliczony na oktale.

**Wybór: V1 = 6SL7 (6N9S), V2 = 6SN7 (6N8S).** Obie lampy mają ten sam układ nóżek (8BD), ale różne punkty pracy, więc zamiana wymaga zmiany rezystorów.

| V1 (wejście + katodyna) | Wzmocnienie wejścia | Wzmocnienie bez NFB | Czułość przy ~20 dB NFB |
|---|---|---|---|
| **6SL7 (6N9S)** | ok. 45× | ok. 47 dB | **ok. 0,6 V** |
| 6SN7 (6N8S) | ok. 10× | ok. 34 dB | ok. 2,5 V (za mało czuły) |

- **6SL7 na wejściu** daje zapas wzmocnienia na ok. 21 dB sprzężenia zwrotnego. To obniża impedancję wyjściową, co ma znaczenie przy kolumnach z dołkiem 2,5 Ω.
- **6SN7 w driverze** przy 8 mA potrzebuje tylko ok. 3,4 V szczytowo na siatce, żeby dać 50 V na siatkę KT88. To połowa jego biasu (−7,5 V), więc zapas jest dwukrotny.
- Na zdjęciu wzmacniacza Onyxa naklejka na driverze podaje ok. 6,4 i 7,7 mA na triodę. To potwierdza 6SN7 (6N8S) w driverze. Co miał na wejściu, nie wiadomo, bo 6N8S i 6N9S wyglądają z zewnątrz tak samo.
- Mocniejszy driver na później: 6BX7 lub 6BL7 (niższe Ri), ale 1,5 A żarzenia na lampę i inne punkty pracy.

Punkty pracy (model 3/2 dopasowany do danych katalogowych, do weryfikacji pomiarem):

| | Lampa | Zasilanie | Ua | Ia | Ug | Rk / Ra |
|---|---|---|---|---|---|---|
| Wejście V1a | ½ 6SL7 | 400 V | 133 V | 1,0 mA | −1,0 V | Rk 1 k, Ra 47 k + 220 k |
| Katodyna V1b | ½ 6SL7 | 400 V | 266 V (Uk 134 V) | 1,2 mA | −0,9 V | 110 k / 110 k |
| Driver V2 | 6SN7 | 410 V | 234 V | 2× 8 mA | −7,5 V | Ra 22 k, Rk wspólny 390 Ω + P100 |

Bieguny na dole pasma są celowo rozsunięte: katodyna → driver 470 nF / 470 kΩ (0,7 Hz), driver → KT88 100 nF / 220 kΩ (7 Hz), toroid poniżej 1 Hz. W Williamsonie z globalną pętlą zmniejsza to ryzyko pompowania (motorboatingu).

Żarzenie lamp sterujących jest podniesione do ok. +67 V, bo katoda katodyny jest na +134 V, a 6SL7 dopuszcza ok. 90 V między żarzeniem a katodą.

### Konkretne lampy

| Typ | Tanio i dobrze (NOS) | Nowa produkcja |
|---|---|---|
| 6SL7 | **6N9S** (radzieckie) | Tung-Sol 6SL7GT, Electro-Harmonix 6SL7EH |
| 6SN7 | **6N8S** (radzieckie), 5692 (wojskowa, droga) | Tung-Sol 6SN7GTB, EH 6SN7EH, Psvane 6SN7 / CV181 |

Na pierwsze uruchomienie: radzieckie 6N9S i 6N8S. Droższe wersje porównywać na dostrojonym wzmacniaczu. Driver warto dobrać tak, żeby obie triody miały zbliżony prąd; resztę wyrównuje P100.
