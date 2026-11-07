# Williamson KT88

Lampowy wzmacniacz push-pull w klasycznej topologii Williamsona, z końcówką na parze KT88 w układzie ultralinearnym (UL). Projekt bazuje na wzmacniaczu **onyx1944**:

- wersja na KT88 (zdjęcia, PCB): https://onyx1944.wordpress.com/2023/11/21/williamson-kt88/
- wersja na 6S33S (schemat i zasilacz): https://onyx1944.wordpress.com/2020/03/16/6s33s-williamson-amplifier/

Autor nie opublikował schematu wersji KT88. Schemat w tym repozytorium powstał więc tak: front end (wejście, katodyna, driver) przepisany z wersji 6S33S, a końcówkę mocy i zasilacz przeliczono od nowa pod KT88.

> **Status: szkic 1, niesprawdzony w praktyce.** Wartości są policzone na papierze z danych katalogowych. Nikt tego układu jeszcze nie zbudował ani nie zmierzył. Przed zamówieniem transformatora sieciowego i dławika warto dać schemat do przejrzenia komuś doświadczonemu (Onyx, elektroda, audiostereo).

> ⚠️ **Wysokie napięcie.** We wzmacniaczu jest do ok. 545 V DC (na zimno), które utrzymuje się na kondensatorach po wyłączeniu. Przed dotknięciem układu zawsze zmierz napięcie.

## Schematy

| Plik | Zawartość |
|---|---|
| [`schematy/kanal.svg`](schematy/kanal.svg) | Jeden kanał: 6N2P → katodyna → 6N6P → 2× KT88 UL, z regulacją biasu każdej lampy |
| [`schematy/zasilacz.svg`](schematy/zasilacz.svg) | Zasilacz wspólny: anodowe 450/400/360 V, bias −90 V, dwa uzwojenia żarzenia |
| [`schematy/williamson-kt88.html`](schematy/williamson-kt88.html) | Oba schematy z punktami pracy, listą elementów i procedurą uruchomienia (otwórz w przeglądarce) |

Kolorem pomarańczowym oznaczone są elementy zmienione albo nowe względem wersji 6S33S.

![Schemat kanału](schematy/kanal.svg)

![Zasilacz](schematy/zasilacz.svg)

## Najważniejsze założenia

| | Wartość |
|---|---|
| Lampy | 6N2P (wejście + katodyna), 6N6P (driver), 2× KT88 na kanał |
| Tryb końcówki | ultralinear, odczep 43% |
| Punkt pracy KT88 | Ua ≈ 445 V, Ik = 50 mA (0,50 V na 10 Ω), Ug1 ≈ −45…−55 V, ok. 21 W na lampę |
| Moc | ok. 40 W na kanał |
| Transformator wyjściowy | toroidy.pl **TTG-KT88PP**: Raa 4 kΩ, UL 43%, 80 W, 300 mA, 12 Hz–56 kHz, wyjścia 4 i 8 Ω |
| Bias | stały, osobny potencjometr dla każdej KT88 (P201, P202), zakres ok. −39…−64 V |
| Sprzężenie zwrotne | globalne, R127/C100 do dobrania (start: 68 k / 250 pF z odczepu 8 Ω) |
| Transformator sieciowy | ok. 300 VA: 350 V/0,5 A, 70 V/0,1 A, 6,3 V/7 A, 6,3 V/3 A |

## Decyzje i otwarte sprawy

- **Kolumny 4 Ω** (patrz [docs/04-kolumny.md](docs/04-kolumny.md)): podłączać do odczepu **4 Ω**, a sprzężenie zwrotne brać też z 4 Ω, z R127 ≈ 47 k na start. Schemat v1 pokazuje jeszcze wariant z odczepem 8 Ω.
- Przy zamówieniu toroidów zapytać toroidy.pl o wersję z dodatkowym odczepem **2 Ω** (do porównania na słuch).
- Z toroidem trzeba pilnować **balansu prądów stałych** obu KT88 (różnica najwyżej ok. 1 mA).
- Wszystkie elektrolity w torze anodowym na **550 V** (w praktyce 2× 400 V szeregowo z rezystorami wyrównującymi).
- Jeśli pojawi się schemat KT88 od Onyxa, porównać z nim zwłaszcza R127/C100 i napięcia zasilania.

## Notatki

1. [Lampy KT88 Psvane: serie i różnice](docs/01-lampy-kt88.md)
2. [Transformatory wyjściowe: Hammond, toroidy.pl, Ogonowski](docs/02-transformatory-wyjsciowe.md)
3. [Topologia: Williamson, Mullard 5-20, 6S33S, 6SN7](docs/03-topologia.md)
4. [Kolumny: impedancja, zwrotnica 2,5-drożna, spadek bafla](docs/04-kolumny.md)
5. [Uruchomienie krok po kroku](docs/05-uruchomienie.md)
6. [Zamawianie płytek PCB](docs/06-pcb.md)

## Generowanie schematów

Schematy są rysowane skryptem (Python 3, bez dodatkowych bibliotek):

```bash
python3 narzedzia/build.py
```

Skrypt [`narzedzia/gen_schemat.py`](narzedzia/gen_schemat.py) zawiera geometrię i wartości elementów. Po zmianie wartości wystarczy uruchomić `build.py` ponownie, a SVG i strona HTML w `schematy/` zostaną odświeżone.
