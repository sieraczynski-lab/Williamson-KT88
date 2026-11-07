# Kolumny: dopasowanie do wzmacniacza

## Obecne kolumny

- 3-drożne, głośniki Dayton, układ **WMTMW** (woofer, średni, tweeter, średni, woofer)
- impedancja nominalna **4 Ω**, woofery 8 Ω
- skuteczność ok. **90 dB**, obciążalność ok. 160 W
- **dołek impedancji ok. 2,5 Ω przy 160 Hz**

## Moc

Przy 90 dB/W/m ok. 40 W z KT88 daje szczytowo ok. 106 dB z metra, więc mocy jest z dużym zapasem. 160 W to obciążalność kolumny, a nie moc, której ona potrzebuje.

## Problem: dołek 2,5 Ω przy 160 Hz

1. **Obciążenie lamp.** Transformator przenosi impedancję proporcjonalnie. Na wyjściu 8 Ω lampy przy 160 Hz widziałyby ok. 1,25 kΩ zamiast 4 kΩ. Na wyjściu 4 Ω widzą ok. 2,5 kΩ, co jest do przyjęcia.
2. **Charakterystyka częstotliwościowa.** Impedancja wyjściowa wzmacniacza (ok. 1 Ω) tworzy dzielnik z impedancją kolumny. W dołku spada głośność, przy 2,5 Ω wobec 8 Ω w innych zakresach różnica może sięgnąć ok. 2 dB, słyszalna jako odchudzony wyższy bas i niższa średnica.

Dołek 2,5 Ω przy kolumnie 4 Ω jest trochę głębszy, niż przewiduje norma (ok. 3,2 Ω), ale przy 3-drożnej zwrotnicy to nic niezwykłego.

## Wnioski dla wzmacniacza

- Kolumny podłączyć do **odczepu 4 Ω**.
- Sprzężenie zwrotne brać z **odczepu 4 Ω**, R127 zmniejszyć ok. √2 razy: z 68 k do **ok. 47 k** (ta sama głębokość pętli).
- Opcja: zamówić TTG-KT88PP z dodatkowym **odczepem 2 Ω**. Kolumna 4 Ω na odczepie 2 Ω daje lampom 8 kΩ nominalnie i ok. 5 kΩ w dołku. Impedancja wyjściowa spada mniej więcej o połowę, lampy pracują lżej, moc spada do ok. 25–30 W (nadal ok. 104–105 dB z metra). Porównać na słuch z odczepem 4 Ω. Sprzężenie zwrotne zawsze z odczepu, do którego podłączone są kolumny.
- Zwrotnice 3-drożne bywają przy wysokich częstotliwościach obciążeniem pojemnościowym, więc test stabilności z kondensatorem na wyjściu jest tu szczególnie ważny.

Ciekawostka: wersja 6S33S, dzięki triodowej końcówce o bardzo niskiej impedancji wyjściowej, reagowałaby na ten dołek dużo słabiej.

## Planowana przeróbka zwrotnicy: 2,5-drożna (w praktyce „3,5-drożna”)

- **Górny woofer:** filtr LCL jak obecnie, gra aż do przejścia na średniotonowe.
- **Dolny woofer:** sama cewka, gra tylko najniższy zakres i kompensuje spadek bafla.

Dlaczego cewka na **dolnym** wooferze:
- podłoga wzmacnia najniższy bas, a wyżej dolny woofer jest już wyciszony,
- znika dołek interferencyjny od odbicia od podłogi, który przy niskim głośniku wypada wysoko w paśmie,
- przy 300–400 Hz fala ma ok. 1 m, więc asymetria wooferów nie psuje promieniowania w pionie.

Jeśli przejście wooferów na średniotonowe jest nisko (200–300 Hz) i wypada blisko spadku bafla, różnica między wooferem z cewką a wooferem z LCL będzie mała. Wtedy prościej dać oba woofery na ten sam filtr i stłumić średnie i wysokie tony. Rozstrzygną pomiary.

### Impedancja po przeróbce

Dwa woofery 8 Ω równolegle dają na basie ok. 4 Ω. Minimum pojedynczego głośnika leży blisko Re (ok. 5,5–6,5 Ω), więc w najgłębszym punkcie wyjdzie ok. 3 Ω, a rezystancja cewek trochę to podniesie. Dla odczepu 4 Ω to akceptowalne. Cel: **minimum impedancji całej kolumny nie niżej niż ok. 3 Ω.**

Przeróbka może sama złagodzić dołek przy 160 Hz, bo tam cewka dolnego woofera ma już wyraźną reaktancję i gra głównie górny woofer.

Przy dolnym wooferze można użyć cewki o wyższej rezystancji (tańsza, rdzeniowa), co dodatkowo podnosi minimum impedancji.

## Spadek bafla (baffle step)

Przy wysokich częstotliwościach fala jest krótsza niż szerokość przedniej ścianki i cała energia idzie do przodu (półprzestrzeń). Przy niskich fala opływa obudowę i rozchodzi się we wszystkich kierunkach, więc przed kolumną jest ciszej, teoretycznie o 6 dB. W pokoju strata jest mniejsza, w praktyce kompensuje się 3–4 dB (mniej, gdy kolumna stoi blisko ściany).

Częstotliwość przejścia w przybliżeniu:

```
f ≈ 115 / szerokość ścianki [m]
25 cm → ok. 460 Hz
30 cm → ok. 380 Hz
```

Metody kompensacji: większa cewka przed wooferem, stłumienie średnich i wysokich tonów albo właśnie konstrukcja 2,5-drożna. Odcięcie dolnego woofera dobiera się w okolicy tej częstotliwości.

## Pomiary i symulacja

- **Impedancja i parametry T/S:** Dayton DATS (v3). Każdy woofer osobno w obudowie, potem oba przez docelowe filtry, na koniec cała kolumna ze zwrotnicą. Ostatnią krzywą zachować do strojenia sprzężenia zwrotnego wzmacniacza.
- **Charakterystyka:** REW + mikrofon pomiarowy (np. UMIK-1). Bas w polu bliskim (kilka mm od membrany), reszta w polu dalekim z bramkowaniem. Połączyć w VituixCAD z uwzględnieniem symulacji bafla, inaczej bas wyjdzie zawyżony.
- **Symulacja pod lampowca:** w symulacji zwrotnicy dodać na wejściu rezystor szeregowy **1 Ω** (na odczepie 2 Ω ok. **0,5 Ω**), żeby zobaczyć charakterystykę z tym wzmacniaczem, a nie z idealnym tranzystorowym.
