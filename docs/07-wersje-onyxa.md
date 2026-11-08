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

- Topologia schematu odpowiada płytce Onyxa, ale **wartości elementów są policzone od nowa** pod 6SL7 + 6SN7 i toroid 4 kΩ.
- Przed montażem trzeba prześledzić ścieżki przy V1 i V2 i potwierdzić topologię.
- Brzmienie z odsłuchu pochodzi z Hammondów 1650HA. Z toroidem 4 kΩ wzmacniacz będzie trochę inny, z większą mocą, ale lampy będą widziały mniejszą impedancję w dołku kolumn.
