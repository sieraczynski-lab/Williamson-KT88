# Wersje Onyxa: co widać na zdjęciach

Onyx nie opublikował schematu wersji KT88. Poniższe wnioski pochodzą ze zdjęć: jego wpisów na blogu oraz zdjęć wzmacniacza zrobionych, gdy był wypożyczony do odsłuchu. Tam, gdzie to wniosek, a nie odczyt, jest to zaznaczone.

## Wersja 6S33S (2020): prototyp montowany przewlekanie

- Montaż „na drutach”: punkty lutownicze i płyty ceramiczne pod podstawkami 6S33S, przewody silikonowe. Bez płytki drukowanej.
- Obudowa z aluminium, dwie komory: na górze tor sygnałowy, na dole zasilacz (4× EPCOS 1000 µF / 300 V, przekaźniki, prawdopodobnie zwłoka anodowego, mała płytka pośrodku).
- **4 transformatory** Ogonowskiego: 2× wyjściowy **LO PP80-3** (etykieta: Raa = 1,2k, wyjścia 4 i 8 Ω) i 2× sieciowy (LO TS100-…). Dwa sieciowe, bo samo żarzenie 6S33S to ponad 26 A na cztery lampy.
- **Dwa potencjometry biasu na kanał**, czyli osobna regulacja każdej lampy.
- Front end na lampach nowalowych 6N2P (wejście + katodyna) i 6N6P (driver), według opublikowanego schematu.

## Wersja KT88 (2023): płytka VA1523-V1.0

- Jedna stereofoniczna płytka „Williamson By Onyx”, oba kanały lustrzanie (oznaczenia 1xx i 2xx).
- **Wszystkie podstawki oktalowe.** Na kanał: V1 przy wejściu i złączu sprzężenia zwrotnego, V2 jako driver, V5 i V6 przy potencjometrach biasu (KT88). Lamp 6N2P i 6N6P nie da się tu użyć.
- **Osobny bias dla każdej KT88** (P101, P102 i P201, P202).
- Na płytce jest część zasilacza: rząd diod prostowniczych, pole elektrolitów 120 µF / 400 V (przy ok. 450 V muszą być łączone szeregowo), duże kondensatory foliowe MKP w filtrach, dwa rezystory 47 Ω / 5 W.
- Złącza: wejście (We-L/P), sprzężenie zwrotne (FB-L/P), żarzenie (FF), listwy do transformatorów i zasilania.
- Sprzęgające do KT88: Miflex MKP-14 0,22 µF / 400 V.

### Wzmacniacz zmontowany (zdjęcie z odsłuchu)

- **Transformatory wyjściowe Hammond**, etykieta odczytana jako **1650HA** (6,6 kΩ, 40 W). Pośrodku duży toroidalny transformator sieciowy.
- **KT88 Psvane** (widoczny fragment napisu), z ręcznymi oznaczeniami na szczytach, pewnie numery doboru.
- Lampy sterujące: oktalowe, rurkowa bańka i czarny bakelitowy cokół, wygląd typowy dla radzieckich **6N8S / 6N9S**. Oznaczeń nie da się odczytać.
- Na lewym driverze naklejka z wartościami, odczytanymi jako **6,37 mA / 7,74 mA**. To najpewniej prądy obu triod. Taki prąd pasuje do 6SN7 (6N8S), a nie do 6SL7 (1–2 mA). Wniosek: **driver to prawie na pewno 6N8S**. Na wejściu mogła być 6N8S albo 6N9S.

## Różnice między wersjami, poza punktem pracy

| | 6S33S | KT88 |
|---|---|---|
| Montaż | przewlekany, prototyp | płytka drukowana, oba kanały |
| Lampy sterujące | 6N2P + 6N6P (nowal) | oktalowe, driver najpewniej 6N8S |
| Końcówka | trioda, ok. 160 V / 200 mA | KT88, ok. 450 V / ok. 50 mA (szacunek) |
| Transformator wyjściowy | Ogonowski LO PP80-3, 1,2 kΩ | Hammond 1650HA, 6,6 kΩ |
| Transformatory sieciowe | 2× EI Ogonowskiego | 1× toroid |
| Siatki drugie | brak (trioda) | zasilane, prawdopodobnie z odczepów UL |
| Zasilacz | osobna komora, montaż przewlekany | częściowo na płytce |

## Wnioski dla tego repozytorium

- Wcześniejsze szkice (1 i 2) zakładały własne wartości. Od wersji 3 schemat jest przerysowany z płytki Onyxa (patrz niżej).
- Brzmienie z odsłuchu pochodzi z Hammondów 1650HA. Z toroidem 4 kΩ wzmacniacz będzie trochę inny, z większą mocą, ale lampy będą widziały mniejszą impedancję w dołku kolumn.

## Schemat i płytka VA1523 (12.11.2026)

Onyx przesłał schematy obu kanałów i rysunki płytki (bez wartości elementów). Wnioski:

- **Wszystkie lampy sterujące to 6SN7:** V1B wejście, V1A katodyna (22k / 22k), V2 driver ze wspólnym R110 390 Ω, **bez potencjometru balansu**.
- Sprzężenie zwrotne: R129 22k (∥ C123) ze złącza J102 na R105 470 Ω w katodzie V1B. R104 47 Ω jest zbocznikowany przez C102 47 µF.
- Front end zasilany z Ua przez **R128 4k7 3 W** (Uaa), z odsprzęganiem C116/C117.
- KT88: g1 przez 1k, g2 przez 100 Ω, katody przez 10 Ω 3 W do masy, środek transformatora odsprzęgnięty C118 100 nF.
- Bias: mostek UF5408, filtr C125–R141–R142–C126 w gałęzi masy; dla każdej KT88 dzielnik P101 47k + R139 47k, z R119 470k od szyny do suwaka.
- Zasilacz anodowy na płytce, **osobno w każdym kanale:** mostek UF5408, R134 10 Ω, C119/C120, zewnętrzny dławik 10 H / 400 mA (L106, L206), C121/C122. Zworki B103/B104 pozwalają zasilić oba mostki z jednego uzwojenia.
- Żarzenie lamp sterujących podniesione do ok. 10% Ua (R136/R137) przez sztuczny środek R130/R131 330 Ω. Przy Ua 465 V katoda katodyny jest ok. 49 V nad żarzeniem, więc mieści się w ±100 V lampy Psvane AIR 6SN7.

### Różnice płytka / schemat (sprawdzone na płytce)

| Element | Schemat | Płytka |
|---|---|---|
| R117 / R217 | 220k / 1k | 100k / 100k |
| R124 / R224 | 10 Ω / 470k | 10 Ω / 10 Ω |
| C123 / C223 | 56 pF | brak |

Według Onyxa część elementów różni się, bo miał inny transformator sieciowy i Hammondy jako wyjściowe. Lista elementów do dobrania pod toroid jest w [05-uruchomienie.md](05-uruchomienie.md#elementy-do-sprawdzenia-lub-zmiany).

## Odpowiedzi Onyxa (12.11.2026)

- **Transformator sieciowy:** toroidy.pl **TSTA-0300/001** (300 VA). Onyx sugeruje większy, żeby w pełni wykorzystać KT88. Planowany TR1 400 VA (360 V + 345 V / 0,65 A) to spełnia. Dokładnych uzwojeń TSTA-0300/001 nie udało się znaleźć; pokrewny TSTA-0250/001 ma anodowe 275/330 V, bias 50 V i trzy uzwojenia 6,3 V.
- **Metoda:** „najpierw obrać punkt pracy i do niego dobrać napięcia; jak już są trafa wyjściowe, zacząć od Raa”. Przy Raa 4 kΩ dane GEC dla pary KT88 UL to ok. 460 V i 2× 50 mA (ok. 70 W przy 2% THD), co odpowiada przyjętemu Ua ok. 465 V i 50–55 mA.
- **Sprzężenie zwrotne:** u niego z odczepu **8 Ω** Hammonda. Tu też z 8 Ω (toroidu).
- **C123:** żeby nie było wzbudzenia na wysokich częstotliwościach. Podobnie **R102/C101** (i R202/C201) w anodzie pierwszego stopnia; 100 nF na schemacie to błąd. U niego obyło się bez tej sieci RC, ale radzi sprawdzić odpowiedź na prostokąt.
- **Rezystory katodowe KT88:** przy stałym biasie mogłoby ich nie być, są tylko do pomiaru prądu; wystarczyłby 1 Ω. Tu zostaje **10 Ω 1 %**, bo pod tę wartość jest liczony pomiar w sterowniku Soloista (55 mA = 0,55 V).
- **Pomyłki na schemacie** (R217, R224) potwierdzone.
