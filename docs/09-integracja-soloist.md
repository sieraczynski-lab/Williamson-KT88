# 9. Zasilacz, sterowanie, dodatki i obudowa z Soloista

Płytka Onyxa VA1523 dostaje całą infrastrukturę z projektu [Soloist-KT88](https://github.com/sieraczynski-lab/Soloist-KT88):

- miękki start i opóźnione anody,
- sterownik ESP32 z pomiarem prądów i automatyczną korektą biasu,
- przełącznik UL / trioda,
- przełącznik kolumn z triggerem,
- selektor wejść z drabinką głośności,
- obudowę.

Płytki Soloista zostają bez zmian w PCB, zmienia się tylko to, co się na nich montuje. Na płytce Onyxa nic się nie przecina: przewody lutuje się do istniejących złączy albo nóżek elementów.

Oznaczenia elementów i złączy Soloista według jego wersji 0.23 (płytki) i 0.4 (obudowa). Oznaczenia Onyxa: lewy kanał 1xx, prawy 2xx.

## 9.1 Schemat blokowy

```
230 V ─ IEC/F1 ─ zasilacz_siec: K1 (R_SS) → K2 ─ TR1
                                                 │
   S1 360 V ── zasilacz_siec F3 ── zasilacz_hv: K3/K4, R_IN, mostek, C1 ─ L1 12 H ─ C2 = B+3 ≈ 470 V
                                                                                     │
                                       ┌─────────────────────────────────────────────┴───────┐
                                  Onyx J103 (L)                                         Onyx J203 (P)
                                  mostek Onyxa przepuszcza DC → R134 → C119/120 → [L106 zwora] → C121/122 = Ua ≈ 467 V
   S4 65 V ── zasilacz_siec: mostek, C141–R142–C142 = −80 V ── Onyx J106 / J206 (DC) → szyna Bias-L ≈ −79 V
   S2 6,3 V/8 A ─────────────────────────────────────────── Onyx J105 / J205 (KT88)
   S3 6,3 V/3 A ── zasilacz_siec J26 → J28 / J30 ────────── Onyx J104 / J204 (6SN7, podniesienie z płytki Onyxa)

sterowanie (ESP32): J2 → K1–K4 · J4 ← prądy 4× KT88 · J5 ← −80 V, B+3 · J10 → korekta biasu 4× KT88
                    J11 → płytki UL · J13 → przełącznik kolumn · J12 ← TRIGGER · I²C → selektor
```

## 9.2 Zasilanie anodowe

Najprostsze i najbezpieczniejsze rozwiązanie: **zasilacz HV Soloista pracuje w całości bez zmian**, a jego wyjście B+3 (napięcie stałe) podaje się na wejścia „AC” mostków na płytce Onyxa. Mostek Onyxa po prostu przepuszcza napięcie stałe przez jedną diodę. Dzięki temu bez żadnych zmian działają:

- opóźnienie anod K3/K4 i ograniczenie udaru R_IN,
- pomiar B+ dla sterownika (J18 HV_SENSE) i dioda HV,
- rezystory upływowe R3–R6.

| Skąd (Soloist) | Dokąd (Onyx) | Uwagi |
|---|---|---|
| zasilacz_hv J13 B+3_KAN_L | **J103 pin 1** | drugi pin J103 zostaje wolny |
| zasilacz_hv J14 B+3_KAN_R | **J203 pin 1** | drugi pin J203 zostaje wolny |
| zasilacz_hv J16 GND_KAN_L | masa płytki Onyxa (minus C120) | przewód 1 mm² do gwiazdy J15 |
| – | **L106 i L206: zwora** | filtruje dławik L1 Soloista (12 H) |

Bilans: B+3 ok. 470 V przy ok. 290 mA (cztery KT88 po 55 mA, siatki drugie, front end ok. 36 mA, dzielniki). Po diodzie mostka i R134 Ua wychodzi ok. **467 V**, a Uaa za R128 ok. 383 V, czyli tyle, ile zakładają punkty pracy.

**Dławik:** wystarczy jeden, L1 Soloista (12 H / 400 mA), już przewidziany w obudowie pod TR1. Na płytce Onyxa złącza L106 i L206 zwiera się przewodem. Alternatywa to dwa dławiki 10 H na płytce Onyxa i zwora zamiast L1 (zasilacz_hv J9–J10); Ua wyjdzie wtedy ok. 470 V. Filtr jest w obu wariantach dwustopniowy, więc tętnienia są pomijalne.

**Masa:** sprawdź omomierzem, czy masy lewego i prawego kanału są połączone na płytce Onyxa. Jeśli tak, prowadź **jeden** przewód masy do gwiazdy (J16), a J17 zostaw wolne. Dwa przewody zrobiłyby pętlę masy.

**Rozładowanie:** po wyłączeniu dioda mostka Onyxa odcina płytkę od zasilacza HV, więc dioda HV na zasilaczu nie pokazuje napięcia na kondensatorach Onyxa. Płytkę rozładowują jej własne R136/R137 (110k) i rezystory wyrównujące. Stała czasowa wynosi ok. 11 s, więc poniżej 50 V jest po ok. 25 s. Przed dotknięciem płytki i tak zawsze mierz napięcie.

## 9.3 Bias

Jedna szyna biasu dla wszystkiego: **−80 V z zasilacza sieciowego Soloista** (S4 65 V, C141–R142 1k–C142). Z niej korzysta też pomiar w sterowniku i przesuwniki korekty.

| Skąd | Dokąd | Uwagi |
|---|---|---|
| zasilacz_siec J21 pin 1 | Onyx **J106 pin 1** | podaje DC; mostek Onyxa przepuszcza, Bias-L ≈ −79 V |
| zasilacz_siec J21 pin 2 | Onyx **J206 pin 1** | |
| zasilacz_siec J21 pin 3 | sterowanie J5 pin 1 | jak w Soloiście |

- Zakres potencjometrów P101/P102: suwak daje od 0,5 do 1,0 napięcia szyny, czyli ok. **−40…−79 V**. Na maksimum ujemnego napięcia lampa jest bezpiecznie zatkana.
- Obciążenie szyny: 4 dzielniki Onyxa (47k + 47k) ok. 3,4 mA, korekta ok. 3,6 mA, pomiar ok. 0,2 mA, razem **ok. 7,2 mA**. To tyle, ile zakłada Soloist (7,3 mA), więc −80 V się utrzymuje.

## 9.4 Pomiar prądów i automatyczna korekta biasu

| sterowanie | Kanał | Lampa Onyxa | Punkt lutowania na płytce Onyxa |
|---|---|---|---|
| J4 pin 1 IK_L1 | lewy | V5 | koniec R123 przy katodzie (nóżka 8 V5) |
| J4 pin 2 IK_L2 | lewy | V6 | koniec R124 przy katodzie (nóżka 8 V6) |
| J4 pin 3 IK_R1 | prawy | V7 | koniec R223 przy katodzie |
| J4 pin 4 IK_R2 | prawy | V8 | koniec R224 przy katodzie |
| J4 pin 5 GND | – | – | masa płytki Onyxa |
| J10 pin 1 BI_L1 | lewy | V5 | koniec **R117** od strony biasu (suwak P101, R119) |
| J10 pin 2 BI_L2 | lewy | V6 | koniec **R118** od strony biasu (suwak P102, R120) |
| J10 pin 3 BI_R1 | prawy | V7 | koniec R217 od strony biasu |
| J10 pin 4 BI_R2 | prawy | V8 | koniec R218 od strony biasu |

Kolejność w J4 i J10 musi być ta sama. Przewody J10 skręcone z masą, z dala od anod. Lutowanie od spodu, na nóżce elementu albo polu, z koszulką termokurczliwą.

**R123, R124, R223, R224:** na płytce Onyxa są to rezystory 10 Ω 3 W o zwykłej tolerancji. Wymień je na **10 Ω 1 % 3 W** albo zmierz każdy i wpisz rzeczywistą wartość do programu.

**Zakres korekty** (przesuwnik Soloista 68k/33k + 1k, źródło ok. −53,9…−50,6 V, opór ok. 23 kΩ; węzeł suwaka Onyxa ma przy −50 V ok. 21 kΩ):

| | Wartość |
|---|---|
| Udział korekty w węźle | ok. 0,47 |
| Zakres korekty na siatce | **ok. ±0,78 V, czyli ok. ±7 mA** (Soloist: ±0,7 V) |
| Przerwany przewód J10 | bias wraca do wartości z samego potencjometru: ok. 2 V cieplej, czyli ok. +15–20 mA |
| Brak 12 V / awaria ESP32 | jak w Soloiście: najwyżej ok. 0,85 V, D9–D12 trzymają wyjście |

Przy przerwanym przewodzie prąd może dojść do ok. 70–75 mA, czyli na granicę alarmu Soloista (75 mA). Dla Williamsona **próg alarmu w ciszy obniżamy do 70 mA**.

**Uruchomienie korekty:** jak w Soloiście. DAC w połowie zakresu (ok. 1,65 V na wyjściu MCP4728), z podłączonym J10 ustaw potencjometrami Onyxa 50–55 mA, dopiero potem włącz automat.

## 9.5 Żarzenie

| Uzwojenie | Droga | Odniesienie |
|---|---|---|
| S3 6,3 V / 3 A (4× 6SN7 = 2,4 A) | zasilacz_siec J26 → J28 → Onyx **J104**, J30 → Onyx **J204** | sztuczny środek Onyxa R130/R131 do UaFF ≈ 42 V |
| S2 6,3 V / 8 A (4× KT88 = 6,4 A) | bezpośrednio do Onyx **J105** i **J205**, przewody 1–1,5 mm² skręcone | patrz niżej |

Na płytkach Soloista **nie montujesz**:
- R13, R14 na zasilacz_siec (sztuczny środek S3; robi to płytka Onyxa),
- R140A, R140B, R141, C140 na zasilacz_hv (podniesienie żarzenia; robi to płytka Onyxa); J34 i J36 zostają wolne.

**Żarzenie KT88: do sprawdzenia przed pierwszym włączeniem.** Na schemacie Onyxa sztuczny środek R132/R133 idzie do sieci **UaFF-L2**, której nie ma nigdzie indziej na schemacie. Zmierz omomierzem, dokąd idzie środek R132/R133 (J105) na płytce:

- **nigdzie (pływa):** zamontuj R11/R12 na zasilacz_siec i połącz J24 z S2. Żarzenie KT88 dostaje odniesienie do masy, jak w Soloiście;
- **do UaFF (ok. 42 V):** **nie montuj R11/R12**. Inaczej między masą a UaFF popłynie prąd przez oba sztuczne środki i rezystory się spalą.

## 9.6 Przekaźniki i sekwencja

K1–K4, ich płytki i sekwencja są bez zmian: K1 (sieć przez R_SS) → K2 (+1,5 s) → kontrola biasu → nagrzewanie 45 s → K3 (anody przez R_IN) → K4 → stabilizacja prądów → zdjęcie MUTE → kolumny na lampę. Wyłączanie: MUTE → kolumny do Marantza → K3/K4 → 3 s → K1/K2.

## 9.7 Przełącznik UL / trioda

Płytka `ul` Soloista (po jednej na kanał) wpina się między płytkę Onyxa a transformator. Na płytce Onyxa nic się nie zmienia:

| Płytka UL kanału L | Połączenie |
|---|---|
| J1 pin 3 G2_A | Onyx **J101 pin 2** (siatka druga V5 przez R125) |
| J1 pin 2 UL_A | odczep UL A toroidu (zamiast do J101-2) |
| J1 pin 1 AN_A | anoda A toroidu, ten sam punkt co Onyx J101 pin 1 |
| J2 pin 3 G2_B | Onyx **J101 pin 4** |
| J2 pin 2 UL_B | odczep UL B toroidu |
| J2 pin 1 AN_B | anoda B toroidu, ten sam punkt co Onyx J101 pin 5 |
| J3 | sterowanie J11 piny 1–2 (prawy kanał: J11 piny 3–4) |

Środek toroidu idzie dalej do J101 pin 3. Bez prądu w cewkach jest tryb UL. Przełączanie tylko przy wyłączonym B+, jak w Soloiście. Po przełączeniu na triodę sprawdź prostokątem stabilność, bo zmienia się wzmocnienie pętli. R125/R126 Onyxa mają 100 Ω / 1 W, a Soloist ma w tym miejscu 270 Ω / 2 W. W trybie triodowym siatka druga dostaje pełne napięcie anody i większy prąd, więc warto wymienić je na **270 Ω 2 W** (lepiej chronią siatkę i tłumią oscylacje).

## 9.8 Przełącznik kolumn i trigger

Płytka `glosniki` i wejście TRIGGER bez zmian:

- odczep **4 Ω** i COM toroidu → glosniki J2 (LAMPA_L), prawy kanał J5;
- **sprzężenie zwrotne z odczepu 8 Ω prosto z toroidu** do Onyx J102, przed przekaźnikiem;
- RL 100 Ω / 2 W zostaje na wtórnym toroidu, więc lampa nigdy nie gra bez obciążenia;
- Marantz → glosniki J1/J4, kolumny → J3/J6, cewki → sterowanie J13.

## 9.9 Selektor i głośność

Płytka selektora Soloista (TubeSel) w puszce aluminiowej (np. Hammond 1590, ok. 112 × 60 × 31 mm) na dnie, z przodu z lewej, pod pełną częścią pokrywy:

- wyjście selektora (J5) → przewód ekranowany → Onyx **J100** i **J200** (We-L, We-P), ekran podłączony tylko po stronie płytki;
- wejście Onyxa nie ma kondensatora sprzęgającego (J100 → R100 → siatka, R101 1M do masy). Na wszelki wypadek, żeby odciąć składową stałą ze źródeł, dodaj **22 nF folia** szeregowo: z 1 MΩ daje to filtr ok. 7 Hz;
- terminator 10 kΩ selektora równolegle z 1 MΩ Onyxa nie zmienia tłumienia drabinki. Impedancja wyjściowa drabinki ≤ 3,2 kΩ z pojemnością wejściową V1B (ok. 60 pF, Miller) daje pasmo powyżej 600 kHz;
- MUTE: K11 selektora przez sterowanie J3, jak w Soloiście.

**Limity głośności** (czułość Williamsona ok. 0,5 V na pełną moc, przy Soloiście 160 mV):

| Źródło | Najmniejsze tłumienie (limit) |
|---|---|
| DAC / CD 2 V | ok. −12 dB |
| pre-out Marantza 1,2 V | ok. −8 dB |
| 1 V | ok. −6 dB |
| 0,3–0,5 V | bez limitu |

Mniejszy nadmiar wzmocnienia niż w Soloiście oznacza też niższy szum w ciszy.

## 9.10 Zmiany w programie ESP32 (względem Soloista)

| | Soloist | Williamson |
|---|---|---|
| Lampy w J4 / J10 | V103, V104, V203, V204 | V5, V6, V7, V8 Onyxa |
| Rezystory pomiarowe | 10 Ω 1 % | 10 Ω (wymienić na 1 % albo wpisać zmierzone) |
| Prąd docelowy | 55 mA | 50–55 mA |
| Alarm w ciszy | > 75 mA | **> 70 mA** |
| Zakres korekty | ±0,7 V (±6 mA) | ±0,78 V (±7 mA) |
| Szyna biasu (kontrola) | −68…−92 V | bez zmian |
| B+ (HV_SENSE) | B+3 | bez zmian (B+3, przed mostkami Onyxa) |
| Limity głośności | czułość 160 mV | czułość ok. 0,5 V (tabela wyżej) |
| Czujnik DS18B20 | – | pod płytką Onyxa, przy rzędzie KT88 |

Reszta (sekwencja, UL/trioda, kolumny, trigger, selektor, IR, wyświetlacze) bez zmian.

## 9.11 Obudowa

Wariant obudowy Soloista z płytką Onyxa jako górnym pokładem: [`obudowa/`](../obudowa/), opis w [`obudowa/CZYTAJ_MNIE.txt`](../obudowa/CZYTAJ_MNIE.txt).

- Płytka Onyxa (360 × 160 mm) leży w oknie pokrywy, wierzch płytki równo z wierzchem pokrywy (Z 106), na 10 tulejach M3 ok. 101 mm od dna.
- Nad płytką **klatka z perforowanej stali nierdzewnej** (379 × 177 × 169 mm), przykręcana do pokrywy 12 śrubami M4. Na wierzchu płytki jest wysokie napięcie, więc klatkę zdejmuje się tylko narzędziem i tylko przy wyłączonym wzmacniaczu.
- Pod płytką na dnie bez zmian: sterowanie, zasilacz sieciowy, zasilacz HV (z kondensatorami C1/C2). Do tego dwie płytki UL pod rzędem KT88 i puszka selektora z przodu.
- Obudowa transformatorów, tył, front i drewno jak w Soloiście 0.4.

## 9.12 Lista „nie montować / zmienić”

| Płytka | Element | Zmiana |
|---|---|---|
| zasilacz_siec | R13, R14 | nie montować |
| zasilacz_siec | R11, R12 | zależnie od UaFF-L2 (9.5) |
| zasilacz_hv | R140A, R140B, R141, C140 | nie montować |
| Onyx | L106, L206 | zwora (filtruje L1 Soloista) |
| Onyx | R123, R124, R223, R224 | 10 Ω 1 % 3 W (albo zmierzyć) |
| Onyx | R125, R126, R225, R226 | 270 Ω 2 W (zalecane przy UL/trioda) |
| Onyx | wejście J100 / J200 | opcjonalnie 22 nF szeregowo |
| sterowanie | program | progi z 9.10 |
