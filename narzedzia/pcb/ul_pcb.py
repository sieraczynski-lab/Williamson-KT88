"""Przelacznik UL / trioda Williamson KT88: jedna plytka, 4 przekazniki (V5, V6 lewy kanal; V7, V8 prawy).
Uruchom:  python3 ul_pcb.py   -> ../../pcb/ul/
"""
import os, sys
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from pcbgen import Board, F
from schwired import WiredSch
from zasilacz_pcb import export

NAME = "ul_trioda_williamson"
OUT = os.path.abspath(os.path.join(D, "..", "..", "pcb", "ul"))
TUBES = (("V5", "L", "J101-1/-2"), ("V6", "L", "J101-5/-4"), ("V7", "P", "J201-1/-2"), ("V8", "P", "J201-5/-4"))
HV = {"%s_%s" % (a, t) for t, _, _ in TUBES for a in ("AN", "UL", "G2")}


def board():
    g_k, g_c, g_mh = "PRZEKAZNIKI UL/TRIODA", "ZLACZA", "OTWORY"
    comps, volt = [], {"+12V": 12, "RLY_UL": 12}
    for k, (t, ch, j) in enumerate(TUBES, 1):
        an, ul, g2 = "AN_" + t, "UL_" + t, "G2_" + t
        volt.update({an: "AC", ul: "AC", g2: "AC"})
        comps.append(("K%d" % k, "G2RL-2-DC12", "RELAY_G2RL", {"1": "+12V", "8": "RLY_UL", "3": g2, "6": g2, "2": ul, "7": ul, "4": an, "5": an},
                      g_k, "lampa %s (kanal %s): bez pradu cewki G2 <- odczep UL (NC); cewka 12 V: G2 <- anoda (NO)" % (t, ch)))
        comps.append(("D%d" % k, "1N4148", "D", {"1": "+12V", "2": "RLY_UL"}, g_k, "dioda cewki K%d" % k))
        comps.append(("J%d" % k, "LAMPA_" + t, "CONN_3", [an, ul, g2], g_c,
                      "zlacze srubowe 7,62 mm, %s: 1 anoda (toroid i %s), 2 odczep UL toroidu, 3 do %s (G2)" % (t, j.split("/")[0], j[:5] + j.split("/")[1])))
    comps.append(("J5", "CEWKI", "CONN_2", ["+12V", "RLY_UL"], g_c, "ze sterowania J11 piny 1-2 (+12 V, RLY_UL)"))
    comps += [("MH%d" % k, "M3", None, {}, g_mh, "") for k in (1, 2, 3, 4)]
    fixed = {"K1": (17, 16.5, "T", "G2RL"), "K2": (17, 40.5, "T", "G2RL"), "K3": (67, 16.5, "T", "G2RL"), "K4": (67, 40.5, "T", "G2RL"),
             "J1": (42, 16.5, "", "TB762_3V"), "J2": (42, 40.5, "", "TB762_3V"), "J3": (92, 16.5, "", "TB762_3V"), "J4": (92, 40.5, "", "TB762_3V"),
             "MH1": (4.5, 4.5, "", "MH"), "MH2": (78, 4.5, "", "MH"), "MH3": (4.5, 61.5, "", "MH"), "MH4": (95.5, 61.5, "", "MH")}
    auto = [("J5", (50, 60, "", ["TB2"])), ("D1", (20, 59, "T", ["DO35", "DO35V"])), ("D2", (32, 59, "T", ["DO35", "DO35V"])),
            ("D3", (68, 59, "T", ["DO35", "DO35V"])), ("D4", (80, 59, "T", ["DO35", "DO35V"]))]
    b = Board(NAME, "Williamson KT88 - przelacznik UL/trioda, 4x KT88 na jednej plytce", 100, 66)
    pos = dict(fixed); pos.update({r: (p[0], p[1], p[2], p[3][0]) for r, p in auto})
    for (ref, value, symbol, nets, group, note) in comps:
        x, y, side, fk = pos[ref]
        b.add(ref, value, symbol, F[fk], x, y, nets, group, note, side or "T")
    Board.VOLT = volt
    b.failed = b.autoplace([r for r, p in auto], dict(auto), list(fixed))
    b.texts = [(25, 28.5, "KANAL L", 1.2), (75, 28.5, "KANAL P", 1.2), (50, 54.5, "WILLIAMSON UL/TRIODA v1.0", 1.0)]
    return b


def schematic(b):
    S = WiredSch(b, ("A4", 11693, 8268))
    P, W, L = S.put, S.w, S.lab
    for k, (x0, y0) in enumerate(((1200, 2100), (1200, 3900), (6200, 2100), (6200, 3900)), 1):
        P("J%d" % k, "CONNR_3", x0, y0); P("K%d" % k, None, x0 + 2600, y0 + 100)
    P("J5", "CONNR_2", 1200, 6200)
    xs = (3000, 3600, 4200, 4800)
    for k, x in enumerate(xs, 1):
        P("D%d" % k, "D_V", x, 6200)
    W(("D1", 1), (3000, 5900), (4800, 5900), ("D4", 1)); W(("D1", 2), (3000, 6500), (4800, 6500), ("D4", 2))
    for k, x in ((2, 3600), (3, 4200)):
        W(("D%d" % k, 1), (x, 5900)); W(("D%d" % k, 2), (x, 6500))
    L((3900, 5900), "+12V", 1, stub=(0, -100)); L((3900, 6500), "RLY_UL", 3, stub=(0, 100))
    for x, y, t in ((800, 1000, "Przelacznik UL / trioda Williamson KT88 - jedna plytka, 4 x KT88 (V5, V6 kanal L; V7, V8 kanal P)"),
                    (800, 1120, "Cewka bez zasilania: G2 <- odczep UL (NC, tryb UL). Cewka 12 V: G2 <- anoda (NO, trioda)."),
                    (800, 1240, "PRZELACZAC TYLKO PRZY WYLACZONYCH ANODACH (ESP32: K3/K4 off, czekaj na Ua < 30 V, przelacz, start)."),
                    (800, 1360, "J1..J4: 1 anoda toroidu (i J101-1/-5 Onyxa), 2 odczep UL toroidu, 3 do J101-2/-4 Onyxa (G2 przez R125/R126)."),
                    (800, 1700, "KANAL L"), (5800, 1700, "KANAL P"),
                    (800, 7000, "J5: ze sterowania J11 piny 1-2 (+12 V, RLY_UL); piny 3-4 J11 wolne")):
        S.note(x, y, t, 60)
    S.autolabel()
    return S


if __name__ == "__main__":
    export(board(), schematic, OUT, NAME, HV, "CZYTAJ_MNIE_ul.txt", vp=(560, 370))
