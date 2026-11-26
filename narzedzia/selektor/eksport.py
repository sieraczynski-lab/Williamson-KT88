#!/usr/bin/env python3
"""Pliki selektora w tym samym ukladzie co pozostale plytki Williamsona (pcb/selektor/):
BOM, BOM JLCPCB, pozycje elementow (CPL), netlista, klasy sieci, wydruk 1:1, BOM LCSC (xlsx), paczki do importu.
Zrodlo: projekt KiCad w pcb/selektor/kicad (po trasowaniu sciezek to on jest zrodlem prawdy).
Uzycie: python3 narzedzia/selektor/eksport.py   (po verify.py i render.py)"""
import csv, json, math, os, re, sys, zipfile
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.join(REPO, "pcb", "selektor")
K8 = os.path.join(ROOT, "kicad")
K5 = os.path.join(ROOT, "kicad5-easyeda")
NAME = "selektor"


def sexp(txt):
    toks = re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+', txt)
    st = [[]]
    for t in toks:
        if t == "(":
            st.append([])
        elif t == ")":
            x = st.pop(); st[-1].append(x)
        else:
            st[-1].append(t[1:-1] if t.startswith('"') else t)
    return st[0][0]


kids = lambda n, k: [x for x in n if isinstance(x, list) and x and x[0] == k]
def kid(n, k):
    r = kids(n, k); return r[0] if r else None
def rot(x, y, a):
    r = math.radians(a)
    return x * math.cos(r) + y * math.sin(r), -x * math.sin(r) + y * math.cos(r)


pcb = sexp(open(os.path.join(K8, "tube_selector.kicad_pcb"), encoding="utf-8").read())
# obrys plytki
ex, ey = [], []
for g in kids(pcb, "gr_line") + kids(pcb, "gr_arc"):
    if kid(g, "layer")[1] == "Edge.Cuts":
        for k in ("start", "mid", "end"):
            p = kid(g, k)
            if p: ex.append(float(p[1])); ey.append(float(p[2]))
X0, Y0, X1, Y1 = min(ex), min(ey), max(ex), max(ey)

# BOM z projektu (wartosci, LCSC, uwagi)
bom_info = {}
with open(os.path.join(K8, "BOM.csv"), encoding="utf-8-sig") as fh:
    for r in csv.DictReader(fh, delimiter=";"):
        for ref in [x.strip() for x in r["Referencje"].split(",")]:
            bom_info[ref] = r

fps, nets = [], {}
for fp in kids(pcb, "footprint"):
    props = {p[1]: p[2] for p in kids(fp, "property")}
    ref = props.get("Reference", "")
    at = kid(fp, "at"); X, Y = float(at[1]), float(at[2]); A = float(at[3]) if len(at) > 3 else 0.0
    layer = kid(fp, "layer")[1]
    fps.append((ref, props.get("Value", ""), fp[1].split(":")[-1], layer, X, Y, A, fp))
    for p in kids(fp, "pad"):
        n = kid(p, "net")
        if n and p[1]:
            nets.setdefault(n[2].lstrip("/"), []).append("%s-%s" % (ref, p[1]))

def key(r):
    m = re.match(r"([A-Z]+)(\d+)", r); return (m.group(1), int(m.group(2))) if m else (r, 0)

# 1. BOM (jak pozostale plytki: wiersz na element)
with open(os.path.join(ROOT, NAME + "_BOM.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["Oznaczenie", "Wartosc", "Footprint", "Strona", "X [mm]", "Y [mm]", "LCSC", "Uwagi"])
    for ref, val, fpn, layer, X, Y, A, _ in sorted(fps, key=lambda f: key(f[0])):
        if ref.startswith("H") and not bom_info.get(ref): continue
        bi = bom_info.get(ref, {})
        w.writerow([ref, bi.get("Wartość", val), fpn, "GORA" if layer.startswith("F") else "DOL",
                    "%.2f" % (X - X0), "%.2f" % (Y - Y0), bi.get("LCSC", ""), bi.get("Uwagi", "")])

# 2. BOM JLCPCB (montaz SMD) - kopia + 3. pozycje elementow (CPL) do montazu
with open(os.path.join(K8, "JLCPCB_BOM.csv"), encoding="utf-8") as src, \
        open(os.path.join(ROOT, NAME + "_BOM_JLCPCB.csv"), "w", encoding="utf-8") as dst:
    dst.write(src.read())
jlc_refs = set()
with open(os.path.join(K8, "JLCPCB_BOM.csv"), encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        jlc_refs |= {x.strip() for x in r["Designator"].split(",")}
with open(os.path.join(ROOT, NAME + "_CPL_JLCPCB.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
    for ref, val, fpn, layer, X, Y, A, _ in sorted(fps, key=lambda f: key(f[0])):
        if ref in jlc_refs:
            w.writerow([ref, "%.3fmm" % (X - X0), "%.3fmm" % (Y1 - Y), "Top" if layer.startswith("F") else "Bottom", "%g" % A])

# 4. netlista
with open(os.path.join(ROOT, NAME + "_netlista.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["Siec", "Polaczenia (element-pin)"])
    for n in sorted(nets, key=lambda s: (s != "GND", s)):
        if n.startswith("unconnected"): continue
        w.writerow([n, " ".join(sorted(nets[n], key=lambda s: key(s.split("-")[0])))])

# 5. klasy sieci (z .kicad_pro; w pliku KiCad sa juz zapisane)
pro = json.load(open(os.path.join(K8, "tube_selector.kicad_pro"), encoding="utf-8"))
ns = pro["net_settings"]
pat = {}
for a in ns.get("netclass_patterns", []):
    pat.setdefault(a["netclass"], []).append(a["pattern"].lstrip("/"))
UW = {"Default": "logika, I2C, zasilanie 12 V i 3,3 V, masa", "Audio": "sygnal audio: drabinka, wejscia, wyjscie",
      "Coil": "cewki przekaznikow i +12 V"}
with open(os.path.join(ROOT, NAME + "_klasy_sieci.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["Klasa", "Szerokosc sciezki [mm]", "Odstep [mm]", "Odstep specjalny", "Sieci", "Uwagi"])
    for c in ns["classes"]:
        w.writerow([c["name"], c.get("track_width"), c.get("clearance"), "", " ".join(pat.get(c["name"], ["(pozostale)"])), UW.get(c["name"], "")])

# 6. wydruk 1:1 (A4, skala 100 %)
MM = 1 / 25.4
fig = plt.figure(figsize=(210 * MM, 297 * MM))
bw, bh = X1 - X0, Y1 - Y0
ox, oy = (210 - bw) / 2, 297 - 40 - bh
ax = fig.add_axes([ox / 210, oy / 297, bw / 210, bh / 297])
ax.set_xlim(X0, X1); ax.set_ylim(Y1, Y0); ax.axis("off")
ax.add_patch(Rectangle((X0, Y0), bw, bh, fill=False, ec="black", lw=0.8))
for ref, val, fpn, layer, X, Y, A, fp in fps:
    for g in kids(fp, "fp_line"):
        if kid(g, "layer")[1] not in ("F.SilkS", "F.Fab"): continue
        s, e = kid(g, "start"), kid(g, "end")
        x1, y1 = rot(float(s[1]), float(s[2]), A); x2, y2 = rot(float(e[1]), float(e[2]), A)
        ax.plot([X + x1, X + x2], [Y + y1, Y + y2], color="#555", lw=0.4)
    for p in kids(fp, "pad"):
        pat_ = kid(p, "at"); sz = kid(p, "size")
        px, py = rot(float(pat_[1]), float(pat_[2]), A)
        wd, ht = float(sz[1]), float(sz[2])
        if round(float(pat_[3]) if len(pat_) > 3 else 0) % 180 == 90: wd, ht = ht, wd
        if p[2] in ("thru_hole", "np_thru_hole") and p[3] == "circle":
            ax.add_patch(Circle((X + px, Y + py), wd / 2, fc="#999", ec="black", lw=0.2))
        else:
            ax.add_patch(Rectangle((X + px - wd / 2, Y + py - ht / 2), wd, ht, fc="#bbb", ec="black", lw=0.2))
        if kid(p, "drill"):
            ax.add_patch(Circle((X + px, Y + py), float(kid(p, "drill")[1]) / 2, fc="white", ec="none"))
    if not ref.startswith("H"):
        ax.text(X, Y, ref, fontsize=3.2 if ref[0] in "RC" else 5, ha="center", va="center", color="black", weight="bold")
fig.text(0.5, 1 - 15 / 297, "Selektor wejsc + drabinka glosnosci (TubeSel v0.5) - rozmieszczenie, skala 1:1 (%.0f x %.0f mm)" % (bw, bh),
         ha="center", fontsize=9)
fig.text(0.5, 1 - 22 / 297, "Drukuj w skali 100 % (bez dopasowania do strony); sprawdz linijka wymiar plytki.", ha="center", fontsize=7)
fig.savefig(os.path.join(ROOT, NAME + "_rozmieszczenie_1do1.pdf"))
plt.close(fig)

# 7. BOM LCSC (xlsx) dla 1 plytki
try:
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "BOM"
    ws.append(["Williamson KT88 - selektor (1 plytka): czesci z LCSC. SMD moze zmontowac JLCPCB (selektor_BOM_JLCPCB.csv + selektor_CPL_JLCPCB.csv)."])
    ws["A1"].font = Font(bold=True)
    ws.append(["LCSC", "Producent / MPN", "Opis", "Oznaczenia", "Ilosc na plytke", "Do zamowienia (z zapasem)"])
    for c in ws[2]: c.font = Font(bold=True)
    with open(os.path.join(K8, "LCSC_zamowienie.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            q = int(r["Qty per board"]) if r["Qty per board"].isdigit() else r["Qty per board"]
            z = (q + (1 if q < 5 else 2)) if isinstance(q, int) else r["Quantity"]
            ws.append([r["LCSC Part Number"], r["Manufacturer Part Number"], r["Description"], r["Designator"], q, z])
    ws.append(["", "mini DC-DC step-down 3,3 V (4 piny, 14,17 x 8,24 mm)", "poza LCSC: Allegro / AliExpress", "U4", 1, 1])
    for col, wdt in zip("ABCDEF", (12, 26, 40, 34, 14, 22)): ws.column_dimensions[col].width = wdt
    wb.save(os.path.join(ROOT, NAME + "_BOM_LCSC.xlsx"))
except ImportError:
    print("brak openpyxl - pomijam xlsx")

# 8. paczki do importu
os.makedirs(os.path.join(ROOT, "import_EasyEDA"), exist_ok=True)
def zipdir(src, dst, arc):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for d, _, fs in os.walk(src):
            for f in sorted(fs):
                p = os.path.join(d, f); z.write(p, os.path.join(arc, os.path.relpath(p, src)))
zipdir(K5, os.path.join(ROOT, "import_EasyEDA", NAME + "_EasyEDA_Pro_KiCad5.zip"), NAME)
zipdir(K8, os.path.join(ROOT, "import_EasyEDA", NAME + "_KiCad8.zip"), NAME)
print("plytka %.1f x %.1f mm, elementow %d, sieci %d" % (bw, bh, len(fps), len(nets)))
