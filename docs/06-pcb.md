# Zamawianie płytek PCB

Płytki pochodzą z projektu Onyxa (wersja KT88). Uwagi do zamówienia u producenta PCB:

- **Miedź 2 oz (70 µm)** zamiast standardowej 1 oz, zwłaszcza jeśli na płytce jest żarzenie albo zasilacz (4× KT88 to 6,4 A samego żarzenia).
- **Laminat FR4 1,6 mm lub grubszy (2 mm).** Lepiej znosi ciężkie podstawki oktalowe i wielokrotne wkładanie lamp. Jeśli lampy siedzą na PCB, zapytać o laminat o podwyższonym Tg (np. Tg170).
- **Wykończenie HASL** w zupełności wystarcza dla elementów przewlekanych. ENIG nie daje tu realnej przewagi.
- **Przed zamówieniem przejrzeć Gerbery:** odstępy między ścieżkami wysokiego napięcia (anody, B+ 400–450 V), średnice otworów pod podstawki, potencjometry biasu i nóżki elektrolitów.
- **Zamówić z zapasem.** 5 i 10 sztuk kosztuje u chińskich producentów prawie tyle samo.

Do sprawdzenia na płytce Onyxa:
- czy jest **osobna regulacja biasu dla każdej KT88** (przy toroidzie konieczna),
- skąd brane jest sprzężenie zwrotne (przy kolumnach 4 Ω: z odczepu 4 Ω),
- czy przewidziane są rezystory antyoscylacyjne na g1 i g2 przy podstawkach,
- napięcia znamionowe kondensatorów w torze anodowym (550 V).
