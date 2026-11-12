"""Eksport obudowy Williamsona: STEP, DXF, lista czesci, widoki -> ../../obudowa/
Uzycie: python3 narzedzia/obudowa/export.py (z katalogu glownego repozytorium albo z tego folderu)."""
import sys, os, shutil, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
import stepw
orig = stepw.prism
REC = {}
def rec(name, color, outer, holes, w0, w1, frame="XY", ref=False, offset=(0, 0, 0)):
    REC[name] = (outer, holes, abs(w1 - w0))
    return orig(name, color, outer, holes, w0, w1, frame, ref, offset)
stepw.prism = rec
import model
from zrender import render
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "obudowa"))
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(os.path.join(OUT, "DXF"))

def dxf(path, loops, ox, oy):
    L = ["0", "SECTION", "2", "ENTITIES"]
    for lp in loops:
        if getattr(lp, "circ", None):
            cx, cy, r = lp.circ
            L += ["0", "CIRCLE", "8", "0", "10", "%.4f" % (cx - ox), "20", "%.4f" % (cy - oy), "40", "%.4f" % r]
            continue
        if getattr(lp, "segs", None):
            L += ["0", "POLYLINE", "8", "0", "66", "1", "70", "1"]
            for sg in lp.segs:
                st = stepw.seg_start(sg)
                bulge = math.tan((sg[4] - sg[3]) / 4) if sg[0] == "A" else 0.0
                L += ["0", "VERTEX", "8", "0", "10", "%.4f" % (st[0] - ox), "20", "%.4f" % (st[1] - oy), "42", "%.6f" % bulge]
            L += ["0", "SEQEND"]
            continue
        L += ["0", "POLYLINE", "8", "0", "66", "1", "70", "1"]
        for (x, y) in lp:
            L += ["0", "VERTEX", "8", "0", "10", "%.4f" % (x - ox), "20", "%.4f" % (y - oy)]
        L += ["0", "SEQEND"]
    L += ["0", "ENDSEC", "0", "EOF"]
    open(path, "w").write("\n".join(L) + "\n")

def mat(n):
    if n.startswith("SS_klatka"): return "stal nierdzewna perforowana (np. Rv 5-8), gieta"
    if n.startswith("AL_"): return "aluminium 5754"
    if n.startswith("ST_"): return "profil stalowy 20x20x1,5 ocynk/czarny - dlugosc"
    return "MDF + fornir"
rows = []
for S in model.parts:
    outer, holes, th = REC[S.name]
    xs = [p[0] for p in outer]; ys = [p[1] for p in outer]
    rows.append((S.name, mat(S.name), th, max(xs) - min(xs), max(ys) - min(ys), len(holes)))
    if not S.name.startswith("ST_"):
        dxf(os.path.join(OUT, "DXF", S.name + ".dxf"), [outer] + list(holes), min(xs), min(ys))
with open(os.path.join(OUT, "lista_czesci.csv"), "w", encoding="utf-8-sig") as fh:
    fh.write("Czesc;Material;Grubosc [mm];Wymiar A [mm];Wymiar B [mm];Otwory/gniazda;Szt.\n")
    for r in rows:
        fh.write("%s;%s;%.1f;%.1f;%.1f;%d;1\n" % r)
stepw.write_step(os.path.join(OUT, "Williamson_obudowa.step"), model.parts, "Williamson_obudowa")
stepw.write_step(os.path.join(OUT, "Williamson_obudowa_z_elementami.step"), model.parts + model.ref, "Williamson_obudowa_z_elementami")
allp = model.parts + model.ref
render(allp, os.path.join(OUT, "widok_przod.png"), azim=-62, elev=24, title="Williamson KT88 w obudowie Soloist - widok z przodu")
render(allp, os.path.join(OUT, "widok_tyl.png"), azim=118, elev=26, title="Widok z tylu")
render(allp, os.path.join(OUT, "widok_bez_klatki.png"), azim=-58, elev=34, title="Bez klatki: plytka Onyxa jako gorny poklad",
       skip=("SS_klatka",))
render(allp, os.path.join(OUT, "widok_wnetrze.png"), azim=-58, elev=40, title="Wnetrze (bez pokrywy, plytki Onyxa, klatki, drewna i dachu trafo)",
       skip=("AL_pokrywa", "DREWNO", "AL_trafo_dach", "SS_", "REF_plytka_Onyx", "REF_KT88", "REF_V", "REF_podstawka", "REF_kondensatory", "REF_potencjometr", "REF_galka", "REF_przycisk", "REF_LED", "REF_wyswietl"))
print(OUT, len(rows))
