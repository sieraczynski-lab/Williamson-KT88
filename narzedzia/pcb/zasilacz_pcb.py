"""Plytka zasilacza Williamson KT88 (docs/09): schemat + PCB (KiCad 4 dla EasyEDA Standard, KiCad 5 dla EasyEDA Pro / KiCad 8).

Generator i biblioteka footprintow/symboli z projektu Soloist-KT88 (pcbgen.py, schwired.py).
Uruchom:  python3 zasilacz_pcb.py   -> ../../pcb/
"""
import os, sys, shutil, zipfile, csv
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from pcbgen import Board, F, SYM, FOOT, reg, box_cap
F["FUSEV"] = reg(box_cap("Fuseholder_5x20_Closed_P22.5", 22.5, 28.0, 10.0, 1.5, 3.0, v=True))
import netclasses
from schwired import WiredSch

NAME = "zasilacz_williamson"
LIB = "williamson"
OUT = os.path.abspath(os.path.join(D, "..", "..", "pcb", "zasilacz"))

HV = {"L_SW", "N_SW", "L_K1", "L_TR", "L_TR2", "HT_TR", "HT_F", "K3_MID", "HT_K3", "HT_IN", "HT_B", "UA", "HVS1", "HVS2", "LED_M"}
VOLT = {"L_SW": "AC", "N_SW": "AC", "L_K1": "AC", "L_TR": "AC", "L_TR2": "AC",
        "HT_TR": "AC", "HT_F": "AC", "K3_MID": "AC", "HT_K3": "AC", "HT_IN": "AC", "HT_B": "AC",
        "B_AC1": 82, "B_AC2": -82, "B_F": 82,
        "UA": 465, "HVS1": 310, "HVS2": 155, "HV_SENSE": 2, "LED_M": 232, "LED_A": 2,
        "+12V": 12, "RLY1": 12, "RLY2": 12, "RLY3": 12, "RLY4": 12, "GND": 0}


def board():
    g_m, g_ht, g_b, g_s, g_l, g_r, g_c, g_mh = ("SIEC 230 V", "ANODY (AC)", "BIAS (AC)", "POMIAR Ua", "LED HV",
                                               "CEWKI K1-K4", "ZLACZA", "OTWORY")
    comps = [
        # ---- siec ----
        ("J1", "SIEC", "CONN_2", ["L_SW", "N_SW"], g_m, "zlacze srubowe: 1 L (po F1 w gniezdzie IEC i wylaczniku), 2 N"),
        ("F2", "T500mA 250V", "FUSE", ["L_TR2", "L_SW"], g_m, "bezpiecznik PS1 (IRM-15-12)"),
        ("J3", "PS1", "CONN_2", ["L_TR2", "N_SW"], g_m, "zlacze srubowe: 230 V czuwania do PS1 IRM-15-12 (sterowanie J1)"),
        ("K1", "G2RL-2-DC12", "RELAY_G2RL", {"1": "+12V", "8": "RLY1", "3": "L_SW", "6": "L_SW", "4": "L_K1", "5": "L_K1", "2": None, "7": None}, g_m,
         "siec przez R_SS; Omron G2RL-2 12 V, 2 styki rownolegle (LCSC C61458)"),
        ("K2", "G2RL-2-DC12", "RELAY_G2RL", {"1": "+12V", "8": "RLY2", "3": "L_K1", "6": "L_K1", "4": "L_TR", "5": "L_TR", "2": None, "7": None}, g_m,
         "bocznik R_SS (+1,5 s); 2 styki rownolegle"),
        ("R1", "47R 10W", "R", ["L_K1", "L_TR"], g_m, "R_SS, rezystor cementowy"),
        ("J5", "TR1_PRI", "CONN_2", ["L_TR", "N_SW"], g_m, "zlacze srubowe: pierwotne TR1, 1 L, 2 N"),
        # ---- anody ----
        ("J7", "S1_IN", "CONN_2", ["HT_TR", "HT_B"], g_ht, "zlacze srubowe 7,62 mm: S1 360 V z TR1 (1 przez F3, 2 drugi koniec)"),
        ("F3", "T1A 500V", "FUSE", ["HT_TR", "HT_F"], g_ht, "bezpiecznik anodowy 5x20, napiecie znamionowe >= 400 V AC (np. Schurter SPT 5x20 500 V)"),
        ("K3", "G2RL-2-DC12", "RELAY_G2RL", {"1": "+12V", "8": "RLY3", "3": "HT_F", "2": None, "4": "K3_MID",
                                       "6": "K3_MID", "7": None, "5": "HT_K3"}, g_ht, "anody (+45 s); dwa styki szeregowo"),
        ("R2", "100R 10W", "R", ["HT_K3", "HT_IN"], g_ht, "R_IN: udar ladowania kondensatorow Onyxa ok. 5 A"),
        ("K4", "G2RL-2-DC12", "RELAY_G2RL", {"1": "+12V", "8": "RLY4", "3": "HT_K3", "6": "HT_K3", "4": "HT_IN", "5": "HT_IN", "2": None, "7": None}, g_ht,
         "bocznik R_IN (+1,5 s); 2 styki rownolegle"),
        ("J8", "HT_L", "CONN_2", ["HT_IN", "HT_B"], g_ht, "zlacze srubowe 7,62 mm: do Onyx J103 (1 -> pin 1, 2 -> pin 2)"),
        ("J9", "HT_R", "CONN_2", ["HT_IN", "HT_B"], g_ht, "zlacze srubowe 7,62 mm: do Onyx J203"),
        # ---- bias ----
        ("J10", "S4_IN", "CONN_2", ["B_AC1", "B_AC2"], g_b, "zlacze srubowe: S4 58 V z TR1"),
        ("F4", "T100mA 250V", "FUSE", ["B_AC1", "B_F"], g_b, "bezpiecznik uzwojenia biasu"),
        ("J11", "BIAS_L", "CONN_2", ["B_F", "B_AC2"], g_b, "zlacze srubowe: do Onyx J106"),
        ("J12", "BIAS_R", "CONN_2", ["B_F", "B_AC2"], g_b, "zlacze srubowe: do Onyx J206"),
        # ---- pomiar Ua ----
        ("J13", "UA_IN", "PAD", ["UA"], g_s, "z Ua-L na plytce Onyxa (plus C121); przewod w izolacji 1 kV"),
        ("R3", "1M 1600V", "R", ["UA", "HVS1"], g_s, "np. Vishay VR37"),
        ("R4", "1M 1600V", "R", ["HVS1", "HVS2"], g_s, ""),
        ("R5", "1M 1600V", "R", ["HVS2", "HV_SENSE"], g_s, ""),
        ("R6", "15k", "R", ["HV_SENSE", "GND"], g_s, "ok. 2,3 V przy 465 V"),
        ("J14", "HV_SENSE", "PAD", ["HV_SENSE"], g_s, "do sterowania J5 pin 2"),
        ("J15", "GND_ONYX", "PAD", ["GND"], g_c, "masa: do gwiazdy na plytce Onyxa (minus C120)"),
        ("J18", "GND_STER", "PAD", ["GND"], g_c, "masa pomiaru: do sterowania J5"),
        # ---- LED HV ----
        ("R7", "220k 1W", "R", ["UA", "LED_M"], g_l, "LED HV ok. 1 mA"),
        ("R8", "220k 1W", "R", ["LED_M", "LED_A"], g_l, ""),
        ("D1", "LED HV czerwona", "D", {"1": "GND", "2": "LED_A"}, g_l, "swieci, dopoki na plytce Onyxa jest napiecie; NIE ZASTEPUJE MIERNIKA"),
        # ---- cewki ----
        ("J16", "RELAY_A", "CONN_3", ["+12V", "RLY1", "RLY2"], g_r, "ze sterowania J2 piny 1,2,3"),
        ("J17", "RELAY_B", "CONN_3", ["+12V", "RLY3", "RLY4"], g_r, "ze sterowania J2 piny 1,4,5"),
        ("D2", "1N4148", "D", {"1": "+12V", "2": "RLY1"}, g_r, ""),
        ("D3", "1N4148", "D", {"1": "+12V", "2": "RLY2"}, g_r, ""),
        ("D4", "1N4148", "D", {"1": "+12V", "2": "RLY3"}, g_r, ""),
        ("D5", "1N4148", "D", {"1": "+12V", "2": "RLY4"}, g_r, ""),
    ] + [("MH%d" % k, "M3", None, {}, g_mh, "") for k in (1, 2, 3, 4)]

    fixed = {"K1": (25, 12, "T", "G2RL"), "K2": (25, 30, "T", "G2RL"),
             "K3": (25, 54, "T", "G2RL"), "K4": (25, 72, "T", "G2RL"),
             "R1": (46, 32, "T", "R10V"), "R2": (58, 50, "T", "R10V"),
             "MH1": (4.5, 4.5, "", "MH"), "MH2": (95.5, 4.5, "", "MH"), "MH3": (4.5, 95.5, "", "MH"), "MH4": (95.5, 95.5, "", "MH")}
    auto = [
        ("J1", (5, 13, "", ["TB2V"])), ("J3", (5, 30, "", ["TB2V"])),
        ("F2", (77, 12, "T", ["FUSE"])), ("J5", (95, 22, "", ["TB2V"])),
        ("J7", (5, 54, "", ["TB762_2V"])), ("F3", (70, 38, "T", ["FUSEV"])),
        ("J8", (95, 42, "", ["TB762_2V"])), ("J9", (95, 60, "", ["TB762_2V"])),
        ("J16", (46, 66, "T", ["H3"])), ("J17", (46, 78, "T", ["H3"])),
        ("D2", (50, 66, "T", ["DO35V"])), ("D3", (50, 77, "T", ["DO35V"])),
        ("D4", (42, 86, "T", ["DO35V"])), ("D5", (46, 86, "T", ["DO35V"])),
        ("J10", (5, 84, "", ["TB2V"])), ("F4", (24, 92, "T", ["FUSE"])),
        ("J11", (46, 95, "", ["TB2"])), ("J12", (57, 95, "", ["TB2"])),
        ("J13", (70, 75, "", ["PADL"])),
        ("R7", (66, 88, "T", ["R1V"])), ("R8", (71, 88, "T", ["R1V"])), ("D1", (68, 98, "T", ["LED3"])),
        ("R3", (77, 88, "T", ["R1V"])), ("R4", (82, 88, "T", ["R1V"])), ("R5", (87, 88, "T", ["R1V"])),
        ("R6", (92, 84, "T", ["R05V"])), ("J14", (97, 76, "", ["PAD"])), ("J18", (97, 82, "", ["PAD"])),
        ("J15", (97, 88, "", ["PADL"])),
    ]
    b = Board(NAME, "Williamson KT88 - plytka zasilacza (siec, opoznienie anod, bias AC, pomiar Ua)", 100, 100)
    pos = dict(fixed)
    pos.update({r: (p[0], p[1], p[2], p[3][0]) for r, p in auto})
    for (ref, value, symbol, nets, group, note) in comps:
        x, y, side, fk = pos[ref]
        b.add(ref, value, symbol, F[fk], x, y, nets, group, note, side or "T")
    Board.VOLT = VOLT
    b.failed = b.autoplace([r for r, p in auto], dict(auto), list(fixed))
    b.texts = [(77, 67.5, "WILLIAMSON KT88", 1.1), (77, 70, "ZASILACZ v1.0", 1.1)]
    return b


def schematic(b):
    S = WiredSch(b, ("A3", 16535, 11693))
    P, W, L = S.put, S.w, S.lab
    # ---------------- 230 V ----------------
    P("J1", "CONNR_2", 900, 2050); P("J3", "CONNR_2", 900, 3050); P("F2", "FUSE_H", 1600, 3000)
    W(("J3", 1), ("F2", 1)); W(("F2", 2), (2000, 3000), (2000, 2000))
    P("K1", "RELAY_G2RL", 2900, 2300)
    W(("J1", 1), (2000, 2000), (2000, 1800), (3500, 1800), (3500, 2000), ("K1", 3))
    P("R1", "RH", 3900, 2200); W(("K1", 4), ("R1", 1))
    P("J5", "CONN_2", 5400, 2250); W(("R1", 2), ("J5", 1))
    P("K2", "RELAY_G2RL", 4300, 3000)
    W((3600, 2200), (3600, 2550), (4900, 2550), (4900, 2700), ("K2", 3))
    W(("K2", 4), (4950, 2900), (4950, 2200))
    for k, c, n in (("K1", "L_SW", "L_K1"), ("K2", "L_K1", "L_TR")):
        L((k, 3), c, 0); L((k, 4), n, 0)
    # ---------------- anody ----------------
    P("J7", "CONNR_2", 900, 4550); P("F3", "FUSE_H", 1600, 4500); W(("J7", 1), ("F3", 1))
    P("K3", "RELAY_G2RL", 2700, 4800)
    W(("F3", 2), (2000, 4500), (2000, 4300), (3300, 4300), (3300, 4500), ("K3", 3))
    W(("K3", 4), (3300, 4700), (3300, 4900), ("K3", 6))
    P("R2", "RH", 3900, 5100); W(("K3", 5), ("R2", 1))
    P("K4", "RELAY_G2RL", 4300, 5900)
    W((3500, 5100), (3500, 5450), (4900, 5450), (4900, 5600), ("K4", 3))
    W(("K4", 4), (5000, 5800), (5000, 5100))
    L(("K4", 3), "HT_K3", 0); L(("K4", 4), "HT_IN", 0)
    P("J8", "CONN_2", 5700, 5150); W(("R2", 2), ("J8", 1))
    P("J9", "CONN_2", 5700, 5550); W((5200, 5100), (5200, 5500), ("J9", 1))
    # ---------------- bias ----------------
    P("J10", "CONNR_2", 900, 7050); P("F4", "FUSE_H", 1600, 7000); W(("J10", 1), ("F4", 1))
    P("J11", "CONN_2", 2600, 7050); W(("F4", 2), ("J11", 1))
    P("J12", "CONN_2", 2600, 7450); W((2050, 7000), (2050, 7400), ("J12", 1))
    # ---------------- pomiar Ua, LED ----------------
    P("J13", "PAD_L", 7500, 2000)
    P("R3", "R", 8200, 2250); P("R4", "R", 8200, 2550); P("R5", "R", 8200, 2850); P("R6", "R", 8200, 3150)
    W(("J13", 1), (8200, 2000), ("R3", 1)); W(("R3", 2), ("R4", 1)); W(("R4", 2), ("R5", 1)); W(("R5", 2), ("R6", 1))
    P("J14", "PAD", 8800, 3000); W(("R5", 2), ("J14", 1))
    P("R7", "R", 9200, 2250); P("R8", "R", 9200, 2550); P("D1", "D", 9200, 2850)
    W((8200, 2000), (9200, 2000), ("R7", 1)); W(("R7", 2), ("R8", 1)); W(("R8", 2), ("D1", 2))
    L(("R6", 2), "GND", 3, stub=(0, 100)); L(("D1", 1), "GND", 3, stub=(0, 100))
    P("J15", "PAD", 8800, 3800); P("J18", "PAD", 8800, 4100)
    W(("J15", 1), (8500, 3800), (8500, 4100), ("J18", 1)); L((8500, 4100), "GND", 3, stub=(0, 100))
    # ---------------- cewki ----------------
    P("J16", "CONN_3", 2600, 9050); P("J17", "CONN_3", 2600, 9650)
    for k, (ref, x) in enumerate((("D2", 3400), ("D3", 3800), ("D4", 4200), ("D5", 4600))):
        P(ref, "D_V", x, 9300)
    for x, y, t in ((800, 1500, "230 V: F1 T2,5A w gniezdzie IEC i wylacznik poza plytka -> J1"),
                    (800, 1620, "K1 wlacza TR1 przez R_SS 47R, po 1,5 s K2 zwiera R_SS"),
                    (5750, 2300, "J5: pierwotne TR1"), (300, 3350, "J3: PS1 IRM-15-12 (czuwanie)"),
                    (800, 4000, "Anody: S1 360 V (odczepy 345/375 V) -> F3 -> K3 (2 styki szeregowo, +45 s) -> R_IN -> K4 (+1,5 s)"),
                    (800, 4120, "-> AC na mostki Onyxa J103 / J203. Prostowniki, filtry i dlawiki 10 H sa na plytce Onyxa."),
                    (5900, 5000, "J8 -> Onyx J103"), (5900, 5400, "J9 -> Onyx J203"),
                    (800, 6600, "Bias: S4 58 V -> F4 -> AC na mostki biasu Onyxa J106 / J206 (ok. -80 V)"),
                    (2900, 7000, "J11 -> Onyx J106"), (2900, 7400, "J12 -> Onyx J206"),
                    (7300, 1600, "Pomiar Ua i LED HV z Ua-L plytki Onyxa (plus C121)"),
                    (9100, 3300, "J14 HV_SENSE -> sterowanie J5-2 (ok. 2,3 V przy 465 V)"),
                    (8900, 3700, "J15 masa do plytki Onyxa, J18 masa do sterowania"),
                    (9700, 2950, "LED HV: NIE ZASTEPUJE MIERNIKA"),
                    (800, 8600, "Cewki K1-K4 ze sterowania J2: J16 = piny 1,2,3; J17 = piny 1,4,5"),
                    (800, 10400, "Zarzenie (S2 6,3 V/8 A, S3 6,3 V/3 A) idzie z TR1 wprost na Onyx J105/J205 i J104/J204, poza ta plytka."),
                    (800, 10520, "Zarzenie KT88 ma odniesienie do masy na plytce Onyxa (UaFF-L2), R11/R12 niepotrzebne.")):
        S.note(x, y, t, 60)
    S.autolabel()
    return S


PRO = """update=
version=1
last_client=eeschema
[eeschema]
version=1
LibDir=
[eeschema/libraries]
LibName1={lib}
[pcbnew]
version=1
"""



def write_lib(path, names, prefix=""):
    o = ["EESchema-LIBRARY Version 2.4" if prefix else "EESchema-LIBRARY Version 2.3", "#encoding utf-8"]
    for u in names:
        t = SYM[u].lib_text()
        if prefix:
            t = t.replace("# %s\n" % u, "# %s%s\n" % (prefix, u), 1).replace("DEF %s " % u, "DEF %s%s " % (prefix, u), 1).replace('F1 "%s"' % u, 'F1 "%s%s"' % (prefix, u), 1)
        o.append(t)
    o += ["#", "#End Library", ""]
    open(path, "w").write("\n".join(o))


def main():
    b = board()
    assert not b.failed, ("autoplace failed", b.failed)
    msgs = b.check()
    if msgs:
        print("\n".join(msgs))
    S = schematic(b)
    errs = S.verify()
    assert not errs, errs
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    k4 = os.path.join(OUT, "KiCad4_dla_EasyEDA_Standard"); os.makedirs(k4)
    k5 = os.path.join(OUT, "KiCad5_dla_EasyEDA_Pro_i_KiCad8"); os.makedirs(k5)
    # KiCad 4
    S.write(os.path.join(k4, NAME + ".sch"), LIB, v5=False)
    write_lib(os.path.join(k4, LIB + ".lib"), S.used_symbols())
    shutil.copy(os.path.join(k4, LIB + ".lib"), os.path.join(k4, NAME + "-cache.lib"))
    b.write_pcb(os.path.join(k4, NAME + ".kicad_pcb"), LIB)
    open(os.path.join(k4, NAME + ".pro"), "w").write(PRO.format(lib=LIB))
    # KiCad 5
    S = schematic(b)
    S.write(os.path.join(k5, NAME + ".sch"), LIB, v5=True)
    write_lib(os.path.join(k5, LIB + ".lib"), S.used_symbols())
    write_lib(os.path.join(k5, NAME + "-cache.lib"), S.used_symbols(), prefix=LIB + "_")
    b.write_pcb(os.path.join(k5, NAME + ".kicad_pcb"), LIB, v5=True)
    open(os.path.join(k5, NAME + ".pro"), "w").write(PRO.format(lib=LIB))
    open(os.path.join(k5, "sym-lib-table"), "w").write(
        '(sym_lib_table\n  (lib (name %s)(type Legacy)(uri ${KIPRJMOD}/%s.lib)(options "")(descr "Williamson KT88"))\n)\n' % (LIB, LIB))
    open(os.path.join(k5, "fp-lib-table"), "w").write("(fp_lib_table\n)\n")
    # zips for import
    imp = os.path.join(OUT, "import_EasyEDA"); os.makedirs(imp)
    with zipfile.ZipFile(os.path.join(imp, NAME + "_Standard_schemat.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in (NAME + ".sch", LIB + ".lib", NAME + "-cache.lib", NAME + ".pro"):
            z.write(os.path.join(k4, f), f)
    with zipfile.ZipFile(os.path.join(imp, NAME + "_Standard_pcb.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(k4, NAME + ".kicad_pcb"), NAME + ".kicad_pcb")
    with zipfile.ZipFile(os.path.join(imp, NAME + "_EasyEDA_Pro_KiCad8.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(k5)):
            z.write(os.path.join(k5, f), f)
    # BOM, net classes, placement drawing
    b.write_csv(OUT)
    netclasses.write_csv(b, OUT)
    svg = b.svg(hv_nets=HV)
    open(os.path.join(OUT, NAME + "_rozmieszczenie.svg"), "w").write(svg)
    shutil.copy(os.path.join(D, "CZYTAJ_MNIE_pcb.txt"), os.path.join(OUT, "CZYTAJ_MNIE.txt"))
    from playwright.sync_api import sync_playwright
    css = (".board{fill:#f4f7f2;stroke:#1d2a1f;stroke-width:.35}.body{fill:rgba(255,255,255,.55);stroke:#3a4a3c;stroke-width:.3}"
           ".body.bot{fill:none;stroke:#2f62b8;stroke-width:.3;stroke-dasharray:1.2 .8}.pad{fill:#c9a24a;stroke:#7a5c17;stroke-width:.12}"
           ".pad.hv{fill:#d9573f;stroke:#7c2414}.hole{fill:#fff;stroke:#1d2a1f;stroke-width:.25}.ref{font-size:2.2px;fill:#1d2a1f;font-weight:600}"
           ".lab{font-size:1.9px;fill:#36503a}.title{font-size:3px;fill:#1d2a1f;font-weight:700}.zone{fill:none}.zl{display:none}")
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={"width": 560, "height": 480}, device_scale_factor=2)
        pg.set_content("<style>body{margin:0;background:#fff}%s</style>%s" % (css, svg))
        pg.screenshot(path=os.path.join(OUT, NAME + "_rozmieszczenie.png")); br.close()
    import schview2
    schview2.render(os.path.join(k5, NAME + ".sch"), os.path.join(k5, LIB + ".lib"), os.path.join(OUT, NAME + "_schemat.png"), scale=6)
    print("OK", OUT, len(b.comps), "elementow,", len(b.nets()), "sieci")
    return b


if __name__ == "__main__":
    main()
