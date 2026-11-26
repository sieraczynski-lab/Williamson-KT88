"""Tylna scianka widziana Z TYLU (jak przy podlaczaniu kabli), z przegrodami i polkami (przerywane) -> obudowa/detal_tylna_scianka.png"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
import model as m
OUT = os.path.join(HERE, "..", "..", "obudowa", "detal_tylna_scianka.png")
u = lambda x: m.W - x                  # widok od tylu: lustro X
fig, ax = plt.subplots(figsize=(14, 6.2), dpi=140)
ax.add_patch(Rectangle((m.T + m.RP_CL, m.T + m.RP_CL), m.W - 2 * m.T - 2 * m.RP_CL, m.Z_LID - m.T - 2 * m.RP_CL, fc="#d9dcdf", ec="#333", lw=1))
for xp in (m.X_P1, m.X_P2):
    ax.axvspan(u(xp + m.T), u(xp), color="#999", alpha=0.25, lw=0)
for nm, (xa, xb) in m.SHELF_X.items():
    z = m.SHELF_Z[nm]
    ax.add_patch(Rectangle((u(xb), z), xb - xa, m.T, fc="none", ec="#555", ls="--", lw=0.8))
    x, y, dd, h = m.TRAFO_POS[nm]; z0 = m.trafo_z0(nm)
    ax.add_patch(Rectangle((u(x + dd / 2), z0), dd, h, fc="#555", alpha=0.12, ec="#555", ls=":", lw=0.8))
    ax.text(u(x), z0 + h / 2, {"OT_L": "TG L", "OT_R": "TG P", "TR1": "TR1"}[nm] + "\n(za scianka, na polce)", ha="center", va="center", fontsize=8, color="#444")
def hole(x, z, d, c="#fff", lab=None, fs=6.5):
    ax.add_patch(Circle((u(x), z), d / 2, fc=c, ec="#222", lw=0.6))
    if lab: ax.text(u(x), z - d / 2 - 1.5, lab, ha="center", va="top", fontsize=fs)
for k, (x, z) in enumerate(m.SPK_OUT):
    hole(x, z, 14, "#c33" if k % 3 != 2 else "#222", ["8 Ω", "4 Ω", "GND"][k % 3])
for k, (x, z) in enumerate(m.SPK_MAR):
    hole(x, z, 12, "#c33" if k % 2 == 0 else "#222", ["M +", "M GND"][k % 2])
for i, (x, z) in enumerate(m.RCA):
    hole(x, z, 11, "#d8b24a")
for j, x in enumerate(sorted({x for (x, z) in m.RCA})):
    ax.text(u(x), 52, "WE %d" % (j + 1), ha="center", fontsize=7)
ax.text(u(m.RCA[0][0]) + 14, 40, "L", fontsize=7, va="center"); ax.text(u(m.RCA[0][0]) + 14, 18, "P", fontsize=7, va="center")
cx, cz = m.IEC
ax.add_patch(Rectangle((u(cx) - m.IEC_FLANGE[0] / 2, cz - m.IEC_FLANGE[1] / 2), *m.IEC_FLANGE, fc="#222", ec="#000"))
ax.add_patch(Rectangle((u(cx) - m.IEC_CUT[0] / 2, cz - m.IEC_CUT[1] / 2), *m.IEC_CUT, fc="#444", ec="#aaa", lw=0.5))
ax.text(u(cx), cz, "230 V\nIEC C14 + bezp. + wyl.", ha="center", va="center", color="w", fontsize=6.5)
hole(*m.TRIG_JACK, 6, "#222", "TRIGGER"); hole(*m.PE_STUD, 10, "#c9a54a", "PE")
for z in m.BR_SIDE_Z:
    hole(m.T + m.BR_SCR, z, 4.5); hole(m.W - m.T - m.BR_SCR, z, 4.5)
for x in m.BR_FLOOR_X: hole(x, m.T + m.BR_SCR, 4.5)
for x in m.BR_LID_X: hole(x, m.Z_LID - m.BR_SCR, 4.5)
for z in (108.0, 120.0, 132.0, 144.0):
    for i in range(33):
        x = 14.0 + i * 12
        if x > 386 or abs(x - (m.X_P1 + m.T / 2)) < 9 or abs(x - (m.X_P2 + m.T / 2)) < 9: continue
        if (x < m.T + m.BR_FL + 6 or x > m.W - m.T - m.BR_FL - 6) and 100 < z < 141: continue
        if any(abs(x - bx) < m.BR_LEN / 2 + 5 for bx in m.BR_LID_X) and z > m.Z_LID - m.BR_FL - 8: continue
        ax.add_patch(Circle((u(x), z), 4, fc="#fff", ec="#888", lw=0.4))
for (x0, lab) in ((m.X_P2 + m.T, "komora TG P"), (m.X_P1 + m.T, "komora TR1: wejscia + siec"), (m.T, "komora TG L")):
    pass
ax.text(u(335), 148, "komora TG kanalu P", ha="center", fontsize=8, weight="bold")
ax.text(u(200), 148, "komora TR1", ha="center", fontsize=8, weight="bold")
ax.text(u(65), 148, "komora TG kanalu L", ha="center", fontsize=8, weight="bold")
ax.text(u(m.CH_X0 + 10), 6, "kanal wejsc\n(za scianka)", ha="center", fontsize=6, color="#444")
ax.set_xlim(-5, m.W + 5); ax.set_ylim(-4, m.Z_LID + 8); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Tylna scianka widziana od tylu (393 x 149 mm); przerywane: polki transformatorow, kropkowane: obrys transformatorow za scianka", fontsize=9)
fig.tight_layout(); fig.savefig(OUT); print(OUT)
