# Williamson KT88

Lampowy wzmacniacz push-pull w klasycznej topologii Williamsona, z końcówką na parze KT88 w układzie ultralinearnym (UL). Projekt bazuje na wzmacniaczu **onyx1944**:

- wersja na KT88 (zdjęcia, PCB): https://onyx1944.wordpress.com/2023/11/21/williamson-kt88/
- wersja na 6S33S (schemat i zasilacz): https://onyx1944.wordpress.com/2020/03/16/6s33s-williamson-amplifier/

Autor nie opublikował schematu wersji KT88. Schemat w tym repozytorium zachowuje jego topologię (wejście sprzężone bezpośrednio z katodyną, różnicowy driver, para KT88), ale wszystkie wartości są policzone od nowa: front end pod lampy oktalowe 6SL7 + 6SN7, jak na płytce Onyxa VA1523, a końcówka i zasilacz pod KT88 w UL z toroidem 4 kΩ. Co wiadomo o wersjach Onyxa ze zdjęć: [docs/07-wersje-onyxa.md](docs/07-wersje-onyxa.md).

> **Status: szkic 2, niesprawdzony w praktyce.** Wartości są policzone na papierze z danych katalogowych. Nikt tego układu jeszcze nie zbudował ani nie zmierzył. Przed zamówieniem transformatora sieciowego i dławika warto dać schemat do przejrzenia komuś doświadczonemu (Onyx, elektroda, audiostereo).

> ⚠️ **Wysokie napięcie.** We wzmacniaczu jest do ok. 545 V DC (na zimno), które utrzymuje się na kondensatorach po wyłączeniu. Przed dotknięciem układu zawsze zmierz napięcie.

## Schematy

| Plik | Zawartość |
|---|---|
| [`schematy/kanal.svg`](schematy/kanal.svg) | Jeden kanał: 6SL7 (wejście + katodyna) → 6SN7 (driver) → 2× KT88 UL, z regulacją biasu każdej lampy |
| [`schematy/zasilacz.svg`](schematy/zasilacz.svg) | Zasilacz wspólny: anodowe 450/410/400 V, bias −90 V, dwa uzwojenia żarzenia |
| [`schematy/williamson-kt88.html`](schematy/williamson-kt88.html) | Oba schematy z punktami pracy, listą elementów i procedurą uruchomienia (otwórz w przeglądarce) |

Kolorem pomarańczowym oznaczone są elementy zmienione albo nowe względem schematu wersji 6S33S Onyxa.

![Schemat kanału](schematy/kanal.svg)

![Zasilacz](schematy/zasilacz.svg)

## Najważniejsze założenia

| | Wartość |
|---|---|
| Lampy | 6SL7 / 6N9S (wejście + katodyna), 6SN7 / 6N8S (driver), 2× KT88 na kanał |
| Tryb końcówki | ultralinear, odczep 43% |
| Punkt pracy KT88 | Ua ≈ 445 V, Ik = 50 mA (0,50 V na 10 Ω), Ug1 ≈ −45…−55 V, ok. 21 W na lampę |
| Moc | ok. 40 W na kanał (kolumny 4 Ω na odczepie 4 Ω) |
| Wzmocnienie | ok. 47 dB bez pętli, ok. 21 dB sprzężenia zwrotnego, czułość ok. 0,6 V na pełną moc |
| Transformator wyjściowy | toroidy.pl **TTG-KT88PP**: Raa 4 kΩ, UL 43%, 80 W, 300 mA, 12 Hz–56 kHz, wyjścia 4 i 8 Ω |
| Bias | stały, osobny potencjometr dla każdej KT88 (P201, P202), zakres ok. −39…−64 V |
| Sprzężenie zwrotne | globalne z odczepu 4 Ω, R127/C100 do dobrania (start: 22 k / 180 pF) |
| Transformator sieciowy | ok. 300 VA: 350 V/0,5 A, 70 V/0,1 A, 6,3 V/7 A (KT88), 6,3 V/3 A (lampy sterujące, pobór 1,8 A) |

## Decyzje i otwarte sprawy

- **Transformatory wyjściowe: toroidy.pl TTG-KT88PP.** Onyx w swojej wersji KT88 używał Hammondów 1650HA (6,6 kΩ), ale używana para z OLX się sprzedała. Szczegóły w [docs/02-transformatory-wyjsciowe.md](docs/02-transformatory-wyjsciowe.md).
- **Lampy sterujące oktalowe**, bo płytka Onyxa ma podstawki oktalowe: 6SL7 na wejściu (więcej wzmocnienia, czyli głębsze NFB i lepsza czułość), 6SN7 w driverze. Uzasadnienie w [docs/03-topologia.md](docs/03-topologia.md).
- **Kolumny 4 Ω** (patrz [docs/04-kolumny.md](docs/04-kolumny.md)): podłączone do odczepu **4 Ω**, sprzężenie zwrotne też z 4 Ω (R127 = 22 k).
- Wszystkie transformatory (2× głośnikowy z odczepem 2/4/8 Ω, sieciowy, dławik) zamówić w toroidy.pl, które robią wykonania nietypowe. Gotowa specyfikacja: [docs/08-zamowienie-toroidy.md](docs/08-zamowienie-toroidy.md).
- Z toroidem trzeba pilnować **balansu prądów stałych** obu KT88 (różnica najwyżej ok. 1 mA).
- Wszystkie elektrolity w torze anodowym na **550 V** (w praktyce 2× 400 V szeregowo z rezystorami wyrównującymi).
- Po otrzymaniu płytek Onyxa sprawdzić, czy topologia przy V1 i V2 zgadza się ze schematem (katodyna sprzężona bezpośrednio, driver ze wspólną katodą). Wartości elementów będą inne niż u Onyxa.
- Jeśli pojawi się schemat KT88 od Onyxa, porównać z nim zwłaszcza R127/C100 i napięcia zasilania.

## Notatki

1. [Lampy KT88 Psvane: serie i różnice](docs/01-lampy-kt88.md)
2. [Transformatory wyjściowe: Hammond, toroidy.pl, Ogonowski](docs/02-transformatory-wyjsciowe.md)
3. [Topologia: Williamson, Mullard 5-20, 6S33S, 6SN7](docs/03-topologia.md)
4. [Kolumny: impedancja, zwrotnica 2,5-drożna, spadek bafla](docs/04-kolumny.md)
5. [Uruchomienie krok po kroku](docs/05-uruchomienie.md)
6. [Zamawianie płytek PCB](docs/06-pcb.md)
7. [Wersje Onyxa: co widać na zdjęciach](docs/07-wersje-onyxa.md)
8. [Specyfikacja do zamówienia w toroidy.pl](docs/08-zamowienie-toroidy.md)

## Generowanie schematów

Schematy są rysowane skryptem (Python 3, bez dodatkowych bibliotek):

```bash
python3 narzedzia/build.py
```

Skrypt [`narzedzia/gen_schemat.py`](narzedzia/gen_schemat.py) zawiera geometrię i wartości elementów. Po zmianie wartości wystarczy uruchomić `build.py` ponownie, a SVG i strona HTML w `schematy/` zostaną odświeżone.
