"""Przekroj mocowania okraglego LCD 2,1" GC9B72 we froncie (pionowy, przez srodek ekranu) -> obudowa/detal_wyswietlacz_przekroj.png"""
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "obudowa", "detal_wyswietlacz_przekroj.png")
fig, ax = plt.subplots(figsize=(10, 7), dpi=150)
W, P, V, REC = 5.0, 57.0, 54.0, 2.5           # lico, frez, okno, glebokosc okna
def r(x0, z0, x1, z1, c, **k): ax.add_patch(Rectangle((x0, z0), x1 - x0, z1 - z0, fc=c, ec="#333", lw=0.6, **k))
# y: 0 = czolo frontu, w glab dodatnio. z: 0 = srodek ekranu
for s in (1, -1):
    r(0, s * V / 2, REC, s * 45, "#b8875a")                     # lico, warstwa z oknem fi 54
    r(REC, s * P / 2, W, s * 45, "#c99a6a")                     # lico, frez fi 57 od tylu
r(W, 30.6, W + 15, 45, "#9c6b3e"); r(W, -45, W + 15, -39.0, "#9c6b3e")   # rama 15 mm (przelot na plytke)
r(W + 15, 26 - 55 + 55, W + 18, 45, "#b0b4b8"); r(W + 15, -45, W + 18, -39, "#b0b4b8")  # sciana Al 3 mm
r(W + 15, -26, W + 18, 26, "#b0b4b8")
r(W - 2.31, -55.92 / 2, W, 55.92 / 2, "#111")                   # szklo LCM 2,01 + tasma 0,3
r(W, -37.9, W + 1.2, 29.6, "#2a56a0")                           # plytka 1,2
r(W + 1.2, -37, W + 3.7, -33, "#222")                           # listwa goldpin
r(W + 1.2, -20, W + 14.5, 20, "#e8d9a0", alpha=0.8)             # pianka dociskowa
ax.annotate("okno fi 54 (pole aktywne fi 52,9)", (0.2, 20), (-34, 30), arrowprops=dict(arrowstyle="->"), fontsize=8)
ax.annotate("frez od tylu fi 57 x 2,5 mm\n(szklo fi 55,9)", (3.8, 28), (-30, 52), arrowprops=dict(arrowstyle="->"), fontsize=8)
ax.annotate("ekran cofniety ok. 2,7 mm\n(2,5 + 0,2 luzu w frezie)", (2.69, 0), (-32, -8), arrowprops=dict(arrowstyle="->"), fontsize=8)
ax.annotate("rama 15 mm: przelot fi 61,2\n+ jezyk 32 mm (plytka 59,2 x 67,5)", (12, 38), (22, 54), arrowprops=dict(arrowstyle="->"), fontsize=8)
ax.annotate("pianka EPDM / neopren ok. 14 mm\ndociska plytke do lica", (14, 5), (30, 15), arrowprops=dict(arrowstyle="->"), fontsize=8)
ax.annotate("sciana Al 3 mm: przepust 34 x 13 mm\nna goldpiny i przewody", (19.5, -33), (30, -30), arrowprops=dict(arrowstyle="->"), fontsize=8)
ax.annotate("goldpiny 10-pin (do S3 mini)", (6.5, -35), (-32, -52), arrowprops=dict(arrowstyle="->"), fontsize=8)
ax.text(2.5, -58, "lico\n5 mm", ha="center", va="top", fontsize=7); ax.text(12.5, -58, "rama\n15 mm", ha="center", va="top", fontsize=7); ax.text(20.5, -58, "Al\n3 mm", ha="center", va="top", fontsize=7)
ax.set_xlim(-38, 60); ax.set_ylim(-64, 62); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Mocowanie okraglego LCD 2,1\" (GC9B72) we froncie - przekroj pionowy przez srodek ekranu (mm)", fontsize=10)
fig.tight_layout(); fig.savefig(OUT); print(OUT)
