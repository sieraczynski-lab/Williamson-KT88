# Transformatory wyjściowe

W Williamsonie globalna pętla sprzężenia zwrotnego obejmuje transformator wyjściowy, więc jego pasmo i indukcyjność rozproszenia decydują o stabilności całego wzmacniacza. Porównane były trzy kandydatury.

## Porównanie

| | Hammond 1650HA | toroidy.pl TTG-KT88PP | Ogonowski LO PP80-1 |
|---|---|---|---|
| Rdzeń | EI | toroid | EI96/59, blachy wyżarzane 0,3 mm |
| Raa | 6,6 kΩ | **4 kΩ** | **4 kΩ** |
| Moc | 40 W | 80 W | 80 W |
| Prąd max | 200 mA na stronę | 300 mA | 250 mA |
| Odczep UL | jest | 43% | 43% |
| Wyjścia | 4, 8, 16 Ω | 4, 8 Ω | 4, 8 Ω |
| Pasmo | 30 Hz–30 kHz (pełna moc, ±1 dB) | 12 Hz–56 kHz (−3 dB) | 8 Hz–65 kHz (−3 dB), 15 Hz–45 kHz (±1 dB) |
| Lp / Ls | brak danych | 427 H / 4,58 mH | 50 H (przy 120 Hz) / brak danych |
| Lampy wg producenta | 6L6GC, 807, 5881, EL34 | KT88, 300B, 6550 | KT88, 6550 |
| Cena (para) | ok. 800 zł używane z OLX (nowe ok. 162 € / szt.) | ok. 1054 zł (527 zł / szt., wersja AUDIO) | ok. 1430 zł, z deklami do ok. 1670 zł |

TTG-KT88PP i LO PP80-1 mają niemal identyczne przekładnie (31,6:1 i 22,3:1), czyli są policzone pod ten sam typowy punkt pracy KT88 w UL.

## Uwagi

**Hammond 1650HA.** 6,6 kΩ to impedancja typowa raczej dla EL34. KT88 przy 6,6 kΩ dadzą mniej mocy, za to pracują liniowo i lżej. Rozsądny wybór, gdy schemat jest liczony pod tę impedancję albo liczy się budżet. Używane sprawdzić: ciągłość i rezystancja uzwojeń, izolacja (najlepiej miernikiem izolacji).

**toroidy.pl TTG-KT88PP.** Stosunek Lp/Ls ≈ 93 000:1 to bardzo dobry wynik dla stabilności pętli. Największa wada toroidu: rdzeń bez szczeliny jest **wrażliwy na niezrównoważenie prądu stałego** między połówkami uzwojenia. Kilka mA różnicy między lampami podmagnesowuje rdzeń, rosną zniekształcenia na basie. Dlatego potrzebny jest osobny bias dla każdej lampy i okresowa kontrola prądów. Producent robi wersje pod konkretne lampy, więc można dopytać o odczep 2 Ω.

**Ogonowski LO PP80-1.** Rdzeń EI dużo lepiej toleruje niezrównoważenie DC, a pasmo jest najszersze. Onyx używał transformatorów Ogonowskiego w wersji 6S33S (LO PP80-3). Najdroższy.

## Co miał Onyx

Na zdjęciu wzmacniacza Onyxa w wersji KT88 widać na transformatorach wyjściowych etykiety Hammonda z oznaczeniem, które wygląda na **1650HA**, a pośrodku toroidalny transformator sieciowy. Brzmienie, które było punktem odniesienia przy wyborze tego projektu, pochodzi więc z Hammondów 6,6 kΩ, a nie z toroidu 4 kΩ.

Przy kolumnach 4 Ω z dołkiem 2,5 Ω Hammond 6,6 kΩ na odczepie 4 Ω byłby wygodniejszy dla lamp: ok. 4,1 kΩ w dołku zamiast ok. 2,5 kΩ, kosztem mocy (ok. 30–35 W).

## Decyzja

Wybrany: **toroidy.pl TTG-KT88PP**. Używana para Hammondów 1650HA z OLX (800 zł) się sprzedała, a nowe są wyraźnie droższe. Toroid jest dedykowany do KT88 w UL, nowy, z gwarancją i ze znanymi parametrami. Warunek: osobna regulacja biasu dla każdej KT88 (jest na schemacie: P201, P202) i dobrze dobrane lampy. Punkt pracy i sprzężenie zwrotne są w szkicu policzone pod 4 kΩ, a nie przepisane od Onyxa, więc trzeba je zweryfikować przy uruchomieniu.

## Montaż toroidu

- Śruba mocująca przez środek toroidu **nie może tworzyć zwoju zwartego**: mocować ją tylko z jednej strony do obudowy albo przez podkładki izolacyjne.
- Transformatory wyjściowe ustawić z dala od sieciowego i obrócić tak, żeby jak najmniej się sprzęgały.
- Przy zamówieniu podać punkt pracy (Ua ≈ 445 V, 50 mA na lampę, UL) i zapytać o tolerancję na niezrównoważenie DC oraz o odczep 2 Ω.
