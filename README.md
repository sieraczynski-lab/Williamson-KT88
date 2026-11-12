# Williamson KT88

Lampowy wzmacniacz push-pull w klasycznej topologii Williamsona (wszystkie lampy sterujące na 6SN7), z końcówką na parze KT88 w układzie ultralinearnym (UL). Projekt to wzmacniacz **onyx1944** na jego płytce VA1523:

- wersja na KT88 (zdjęcia, PCB): https://onyx1944.wordpress.com/2023/11/21/williamson-kt88/
- wersja na 6S33S (schemat i zasilacz): https://onyx1944.wordpress.com/2020/03/16/6s33s-williamson-amplifier/

Płytka **VA1523-V1.0** jest kupiona od Onyxa (bez lamp i transformatorów), a Onyx udostępnił schematy. Schemat w tym repozytorium jest przerysowany z jego schematu i **poprawiony według wartości faktycznie wlutowanych na płytce**. Pomarańczowe elementy to te, które trzeba sprawdzić albo dobrać pod toroid TTG-KT88PP i własny transformator sieciowy. Oryginalnych plików Onyxa tu nie ma, to jego praca.

> **Status: płytka w ręku, przed uruchomieniem.** Punkty pracy są szacunkowe (model lampy, Ua ≈ 465 V), do potwierdzenia pomiarem.

> ⚠️ **Wysokie napięcie.** Ua ok. 465 V, a na zimno i przy wysokim napięciu sieci więcej. Kondensatory filtrów rozładowują się przez rezystory 680 k przez kilka minut. Przed dotknięciem płytki zawsze zmierz napięcie.

## Schematy

| Plik | Zawartość |
|---|---|
| [`schematy/kanal.svg`](schematy/kanal.svg) | Jeden kanał wg VA1523: 6SN7 (wejście + katodyna) → 6SN7 (driver) → 2× KT88 UL, bias osobno dla każdej lampy |
| [`schematy/zasilacz.svg`](schematy/zasilacz.svg) | Zasilacz z płytki (osobno w każdym kanale): mostek, CLC z dławikiem 10 H, Uaa przez R128, bias, podniesienie żarzenia |
| [`schematy/williamson-kt88.html`](schematy/williamson-kt88.html) | Oba schematy z punktami pracy, różnicami płytka/schemat, listą zmian i uruchomieniem (otwórz w przeglądarce) |

![Schemat kanału](schematy/kanal.svg)

![Zasilacz](schematy/zasilacz.svg)

## Najważniejsze dane

| | Wartość |
|---|---|
| Lampy | V1, V2: 6SN7 (6N8S); V5, V6: KT88 (lewy kanał; prawy V3, V4, V7, V8) |
| Front end | wejście ok. 3,7 mA / 89 V, katodyna 22k/22k ok. 4,2 mA, driver ok. 5 mA na triodę (bez balansu AC) |
| Końcówka | KT88 UL, Ua ≈ 465 V, 50–55 mA (0,50–0,55 V na 10 Ω), Ug1 ≈ −45…−55 V |
| Transformator wyjściowy | toroidy.pl **TTG-KT88PP** (u Onyxa Hammond 1650HA 6,6 kΩ) |
| Sprzężenie zwrotne | R129 22k z **odczepu 8 Ω** (ok. 10 dB), C123 niemontowany |
| Czułość / moc | ok. 0,5 V / ok. 40 W na kanał, kolumny na odczepie 4 Ω |
| Transformator sieciowy | 400 VA: 360 V (+345 V)/0,65 A, 65 V/50 mA, 6,3 V/8 A, 6,3 V/3 A (ta sama specyfikacja co w Soloiście) |
| Dławiki | z zasilaczem Soloista: jeden L1 12 H (L106/L206 zwarte); samodzielnie: 2× 10 H (L106, L206), min. 200 mA |

## Płytka a schemat Onyxa

| Element | Na schemacie | Na płytce |
|---|---|---|
| R117 / R217 | 220k / 1k | **100k / 100k** |
| R124 / R224 | 10 Ω / 470k | **10 Ω / 10 Ω** |
| C123 / C223 | 56 pF | **brak** |

## Zasilacz, sterowanie, dodatki i obudowa z Soloista

Płytka Onyxa dostaje całą infrastrukturę z [Soloist-KT88](https://github.com/sieraczynski-lab/Soloist-KT88): miękki start i opóźnione anody, sterownik ESP32 z automatyczną korektą biasu, przełącznik UL / trioda, przełącznik kolumn z triggerem, selektor z drabinką głośności i obudowę. Płytki Soloista bez zmian w PCB, płytka Onyxa bez cięcia ścieżek. Szczegóły: [docs/09-integracja-soloist.md](docs/09-integracja-soloist.md), obudowa: [`obudowa/`](obudowa/).

![Płytka Onyxa jako górny pokład](obudowa/widok_bez_klatki.png)

## Decyzje i otwarte sprawy

- **Toroid TTG-KT88PP** zamiast Hammonda: sprzężenie zwrotne z odczepu 8 Ω (zbliżona głębokość pętli jak u Onyxa), kolumny na 4 Ω. Kompensację C123 dobrać na oscyloskopie, jeśli prostokąt dzwoni.
- **R128 / R228** (4k7) dobrać do własnego Ua, żeby Uaa wyszło ok. 380–420 V.
- **Driver bez balansu AC:** do V2 dawać 6SN7 o zbliżonych prądach obu triod.
- **Dodatek:** rezystor 100 Ω / 2 W między 4 Ω a COM (wzmacniacz nie pracuje bez obciążenia).
- **Do potwierdzenia u Onyxa:** Ua i Uaa, napięcie AC biasu, odczep sprzężenia zwrotnego w Hammondzie, prąd KT88, dokąd idzie sieć UaFF-L2.
- Projekt równoległy: [Soloist-KT88](https://github.com/sieraczynski-lab/Soloist-KT88) (Mullard: EF86 + E88CC LTP + KT88), z tym samym transformatorem sieciowym i toroidami.

## Notatki

1. [Lampy KT88 Psvane: serie i różnice](docs/01-lampy-kt88.md)
2. [Transformatory wyjściowe: Hammond, toroidy.pl, Ogonowski](docs/02-transformatory-wyjsciowe.md)
3. [Topologia: Williamson, Mullard 5-20, 6S33S, 6SN7](docs/03-topologia.md)
4. [Kolumny: impedancja, zwrotnica 2,5-drożna, spadek bafla](docs/04-kolumny.md)
5. [Uruchomienie krok po kroku](docs/05-uruchomienie.md)
6. [Zamawianie płytek PCB](docs/06-pcb.md)
7. [Wersje Onyxa: zdjęcia, schemat i płytka VA1523](docs/07-wersje-onyxa.md)
8. [Specyfikacja do zamówienia w toroidy.pl](docs/08-zamowienie-toroidy.md)
9. [Zasilacz, sterowanie, dodatki i obudowa z Soloista](docs/09-integracja-soloist.md)

## Generowanie schematów

Schematy są rysowane skryptem (Python 3, bez dodatkowych bibliotek):

```bash
python3 narzedzia/build.py
```

Obudowa (STEP, DXF, widoki) powstaje z `python3 narzedzia/obudowa/export.py` (wymaga `numpy` i `matplotlib`).

Skrypt [`narzedzia/gen_schemat.py`](narzedzia/gen_schemat.py) zawiera geometrię i wartości elementów. Po zmianie wartości wystarczy uruchomić `build.py` ponownie, a SVG i strona HTML w `schematy/` zostaną odświeżone.
