# Uruchomienie krok po kroku (płytka Onyxa VA1523 + toroid)

> ⚠️ Ua ok. 465 V, a na zimno i przy wysokim napięciu sieci więcej. Filtry rozładowują się przez rezystory 680 k kilka minut. Pracuj jedną ręką, przed dotknięciem płytki mierz napięcie.

Oznaczenia dla lewego kanału (1xx). Prawy kanał: to samo z 2xx.

## Punkty pracy (szacunek, Ua ≈ 465 V)

| Stopień | Lampa | Ua | Ia | Uk | Uwagi |
|---|---|---|---|---|---|
| Wejście | ½ 6SN7 (V1B) | ≈ 89 V | 3,7 mA | 1,9 V | NFB na R105 470 Ω, R104 47 Ω zbocznikowany C102 |
| Katodyna | ½ 6SN7 (V1A) | ≈ 198 V | 4,2 mA | ≈ 92 V | R107 / R108 22k |
| Driver | 6SN7 (V2A, V2B) | ≈ 144 V | 2× 5 mA | 3,9 V | wspólny R110 390 Ω, bez balansu AC |
| Końcówka | 2× KT88 UL | ≈ 465 V | 50–55 mA | – | 0,50–0,55 V na R123/R124 (10 Ω), Ug1 ok. −45…−55 V |
| Uaa | – | ≈ 381 V | ok. 18 mA | – | za R128 4k7 |
| Podniesienie żarzenia | – | ≈ 42 V | – | – | R136/R137 |

## Przed pierwszym włączeniem

1. Obejrzyj płytkę: luty, elektrolity (wybrzuszenia, wycieki), przebarwienia przy rezystorach mocy. Wyczyść kurz, wysusz (płytka leżała na strychu).
2. Ustaw zworki B101–B104 pod własne uzwojenia. Sprawdź, dokąd idzie sieć UaFF-L2 (żarzenie KT88).
3. Wlut dodatkowy RL 100 Ω / 2 W między odczep 4 Ω a COM (przy złączach albo przy transformatorze).
4. P101/P102 (i P201/P202) ustaw tak, żeby suwak dawał **maksimum ujemnego napięcia**.

## Kolejność

1. **Sam zasilacz, bez lamp,** przez żarówkę w szereg z siecią albo autotransformator. Podnoś napięcie powoli, żeby uformować elektrolity, które długo nie pracowały. Sprawdź Bias-L (ok. −80 V) i zakres na suwakach.
2. **Tanie lampy,** rezystor 4 Ω / 50 W na odczepie 4 Ω, **J102 odłączone** (bez sprzężenia zwrotnego).
3. Po nagrzaniu zmierz Ua, Uaa i napięcia z tabeli. Podnoś prąd KT88 potencjometrami do 0,50–0,55 V na R123/R124, różnica w parze najwyżej ok. 10 mV (1 mA). Przy toroidzie to ważne.
4. Zmierz prądy obu triod V2 (spadki na R115/R116). Do drivera daj lampę, której połówki mają najbliższe prądy.
5. Jeśli Uaa wyraźnie odbiega od ok. 380–420 V, skoryguj R128/R228.
6. **Podłącz J102 do odczepu 8 Ω.** Jeśli wzmocnienie wzrośnie zamiast spaść albo pojawi się wzbudzenie, wyłącz i zamień końce uzwojenia wtórnego.
7. Prostokąt 1 kHz i 10 kHz na 4 Ω, potem z dołożonym 0,1–0,47 µF równolegle. Jeśli zbocza dzwonią, wlutuj C123/C223 i dobierz od ok. 33 pF w górę (do ok. 150 pF).
8. Obserwuj membrany przy włączaniu i wyłączaniu. Powolne pompowanie: zwiększ C105/C106 z 220 nF do 470 nF (biegun z ok. 6 Hz na ok. 3 Hz, dalej od bieguna C103/C104 ok. 7 Hz).
9. Po kilku godzinach grania i po pierwszych tygodniach ponownie wyrównaj bias.

## Elementy do sprawdzenia lub zmiany

| Element | Wartość Onyxa | Od czego zależy | Co zrobić |
|---|---|---|---|
| R129 / R229 | 22k | przekładnia TR-OUT i odczep | start 22k z odczepu 8 Ω (ok. 10 dB); z 4 Ω byłoby ok. 8 dB |
| C123 / C223 | n.m. | TR-OUT na wysokich częstotliwościach | dobrać na oscyloskopie, 33–150 pF, jeśli potrzeba |
| R102 / C101 (R202 / C201) | n.m. | stabilność na w.cz. | tylko gdy C123 nie wystarczy: start 1k2 + 680 pF, dobór prostokątem (100 nF ze schematu to pomyłka) |
| R128 / R228 | 4k7 3 W | Ua z własnego zasilacza | Uaa ok. 380–420 V |
| odczep S1 TR1 | – | Ua | 345 / 360 / 375 V, cel Ua ok. 465 V |
| P101/P102, R139/R140, R119/R120 | 47k / 47k / 470k | napięcie uzwojenia biasu | suwak 0,5–1,0 × Bias-L; przy −80 V zakres −40…−80 V |
| L106 / L206 | 10 H / 400 mA | – | po jednym dławiku na kanał, min. 200 mA |
| R134 / R234 | 10 Ω 3 W | uzwojenie anodowe | zostawić |
| R136 / R137 | 100k / 10k | Ua | zostawić (ok. 10% Ua) |
| RL (dodatek) | – | – | 100 Ω / 2 W między 4 Ω a COM |
