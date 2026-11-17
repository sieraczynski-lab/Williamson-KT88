"""Przelacznik kolumn Marantz / Lampa + uklad pomiaru sygnalu do wskaznikow VU (2 kanaly), Williamson KT88.

Czesc przekaznikowa jak w Soloist-KT88 (boards.glosniki); dodany tor VU wg docs/10, 2.4.
Uruchom:  python3 glosniki_pcb.py   -> ../../pcb/glosniki/
"""
import os, sys
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from pcbgen import Board, F
from schwired import WiredSch
from zasilacz_pcb import export

NAME = "glosniki_williamson"
OUT = os.path.abspath(os.path.join(D, "..", "..", "pcb", "glosniki"))
W, H = 100, 44
HV = set()


def board():
    g_k, g_v, g_c, g_mh = "PRZEKAZNIKI GLOSNIKOW", "POMIAR VU", "ZLACZA", "OTWORY"
    comps = []
    for k, ch, ref in ((1, "L", "K1"), (2, "R", "K2")):
        comps.append((ref, "G2RL-2-DC12", "RELAY_G2RL",
                      {"1": "+12V", "8": "RLY_SPK", "3": "SPK_%sP" % ch, "6": "SPK_%sN" % ch, "2": "MAR_%sP" % ch, "7": "MAR_%sN" % ch,
                       "4": "TUBE_%sP" % ch, "5": "TUBE_%sN" % ch}, g_k,
                      "kanal %s: bez pradu cewki kolumna <- Marantz (NC), cewka zasilona: kolumna <- Lampa (NO); + i - przelaczane" % ch))
    comps += [
        ("D1", "1N4148", "D", {"1": "+12V", "2": "RLY_SPK"}, g_k, "dioda cewki K1"),
        ("D2", "1N4148", "D", {"1": "+12V", "2": "RLY_SPK"}, g_k, "dioda cewki K2"),
        ("J1", "MARANTZ_L", "CONN_2", ["MAR_LP", "MAR_LN"], g_c, "z zaciskow Marantza na tylnej sciance, kanal L: 1 +, 2 GND"),
        ("J2", "LAMPA_L", "CONN_2", ["TUBE_LP", "TUBE_LN"], g_c, "z wtornego toroidu L: 1 odczep 4 Ohm, 2 COM (masa Lampy)"),
        ("J3", "KOLUMNA_L", "CONN_2", ["SPK_LP", "SPK_LN"], g_c, "do zaciskow wyjsciowych L: 1 -> 4 Ohm, 2 -> GND (izolowany od obudowy)"),
        ("J4", "MARANTZ_R", "CONN_2", ["MAR_RP", "MAR_RN"], g_c, "z Marantza, kanal P"),
        ("J5", "LAMPA_R", "CONN_2", ["TUBE_RP", "TUBE_RN"], g_c, "z wtornego toroidu P: 1 odczep 4 Ohm, 2 COM"),
        ("J6", "KOLUMNA_R", "CONN_2", ["SPK_RP", "SPK_RN"], g_c, "do zaciskow wyjsciowych P"),
        ("J7", "CEWKI", "CONN_2", ["+12V", "RLY_SPK"], g_c, "ze sterowania J13 (+12 V, RLY_SPK)"),
    ]
    # ---- tor VU: odczep 4 Ohm (przed przekaznikiem) -> 100k / 5k1 do 1,65 V -> ADC ESP32 ----
    for i, ch, adc in ((0, "L", "GPIO2"), (1, "R", "GPIO3")):
        n = "VU_" + ch
        comps += [
            ("R%d" % (1 + i), "100k 1%", "R", ["TUBE_%sP" % ch, n], g_v, "metalizowany 1 %% 0,6 W; dzielnik VU kanal %s (odczep 4 Ohm)" % ch),
            ("R%d" % (3 + i), "5k1 1%", "R", [n, "VMID"], g_v, "metalizowany 1 %; k = 5,1 / 105,1 = 0,0485"),
            ("C%d" % (1 + i), "1n C0G", "C", [n, "VMID"], g_v, "C0G/NP0 50 V raster 5 mm; filtr ok. 31 kHz"),
            ("D%d" % (3 + 2 * i), "BAT85", "D", {"1": "3V3", "2": n}, g_v, "Schottky: ogranicznik do 3,3 V"),
            ("D%d" % (4 + 2 * i), "BAT85", "D", {"1": n, "2": "GND"}, g_v, "Schottky: ogranicznik do masy"),
        ]
    comps += [
        ("R5", "1k", "R", ["3V3", "VMID"], g_v, "punkt srodkowy 1,65 V"),
        ("R6", "1k", "R", ["VMID", "GND"], g_v, "punkt srodkowy 1,65 V"),
        ("C3", "10u 16V", "CP", ["VMID", "GND"], g_v, "elektrolit 10 uF, + do VMID"),
        ("J8", "VU", "CONN_4", ["3V3", "GND", "VU_L", "VU_R"], g_c,
         "goldpin 4: 1 3V3, 2 GND (masa sterowania), 3 VU_L -> ESP32 GPIO2, 4 VU_R -> ESP32 GPIO3; przewod ekranowany 4-zylowy, ekran do masy tylko od strony sterowania"),
    ]
    comps += [("MH%d" % k, "M3", None, {}, g_mh, "") for k in (1, 2, 3)]
    fixed = {"K1": (30, 28, "T", "G2RL"), "K2": (72, 28, "T", "G2RL"),
             "J1": (12, 5, "", "TB2"), "J2": (27, 5, "", "TB2"), "J3": (42, 5, "", "TB2"),
             "J4": (58, 5, "", "TB2"), "J5": (73, 5, "", "TB2"), "J6": (88, 5, "", "TB2"),
             "MH1": (4.5, 39.5, "", "MH"), "MH2": (51, 17.5, "", "MH"), "MH3": (95.5, 39.5, "", "MH")}
    auto = [("J7", (95.5, 22, "T", ["H2", "H2H"])),
            ("D1", (8, 15, "T", ["DO35", "DO35V"])), ("D2", (93, 15, "T", ["DO35", "DO35V"])),
            ("J8", (51, 41.5, "T", ["H4", "H4H"])),
            ("R1", (17, 40.5, "T", ["R05", "R05V"])), ("R3", (32, 40.5, "T", ["R05", "R05V"])), ("C1", (44, 38, "T", ["C5"])),
            ("D3", (46, 28, "T", ["DO35V", "DO35"])), ("D4", (49, 28, "T", ["DO35V", "DO35"])),
            ("R2", (84, 40.5, "T", ["R05", "R05V"])), ("R4", (69, 40.5, "T", ["R05", "R05V"])), ("C2", (58, 38, "T", ["C5"])),
            ("D5", (56, 28, "T", ["DO35V", "DO35"])), ("D6", (53, 28, "T", ["DO35V", "DO35"])),
            ("R5", (5, 24, "T", ["R05V", "R05"])), ("R6", (9, 24, "T", ["R05V", "R05"])), ("C3", (89, 30, "T", ["CP6"]))]
    volt = {"+12V": 12, "RLY_SPK": 12, "3V3": 3, "VU_L": 2, "VU_R": 2, "VMID": 2, "GND": 0}
    b = Board(NAME, "Williamson KT88 - przelacznik kolumn Marantz/Lampa + pomiar VU", W, H)
    pos = dict(fixed); pos.update({r: (p[0], p[1], p[2], p[3][0]) for r, p in auto})
    for (ref, value, symbol, nets, group, note) in comps:
        x, y, side, fk = pos[ref]
        b.add(ref, value, symbol, F[fk], x, y, nets, group, note, side or "T")
    Board.VOLT = volt
    b.failed = b.autoplace([r for r, p in auto], dict(auto), list(fixed))
    b.texts = [(51, 12, "WILLIAMSON GLOSNIKI + VU v1.0", 1.0)]
    return b


def schematic(b):
    S = WiredSch(b, ("A4", 11693, 8268))
    P, Wr, L = S.put, S.w, S.lab
    for k, (ch, K, y) in enumerate((("L", "K1", 2600), ("R", "K2", 5300))):
        P(K, None, 4000, y)
        j0 = 1 + 3 * k
        P("J%d" % j0, "CONNR_2", 1300, y - 450); P("J%d" % (j0 + 1), "CONNR_2", 1300, y + 450); P("J%d" % (j0 + 2), "CONN_2", 6300, y - 50)
    P("J7", "CONNR_2", 1300, 7200); P("D1", "D_V", 2800, 7200); P("D2", "D_V", 3400, 7200)
    Wr(("D1", 1), (2800, 6900), (3400, 6900), ("D2", 1)); Wr(("D1", 2), (2800, 7500), (3400, 7500), ("D2", 2))
    L((3100, 6900), "+12V", 1, stub=(0, -100)); L((3100, 7500), "RLY_SPK", 3, stub=(0, 100))
    # tor VU: R1 pionowo (gora TUBE_xP), wezel VU_x, R3 i C1 w dol do VMID, diody w gore do 3V3 / w dol do GND
    for i, (ch, y) in enumerate((("L", 2700), ("R", 5000))):
        r_in, r_lo, c, d_up, d_dn = "R%d" % (1 + i), "R%d" % (3 + i), "C%d" % (1 + i), "D%d" % (3 + 2 * i), "D%d" % (4 + 2 * i)
        P(r_in, None, 8000, y - 300)
        P(r_lo, None, 8600, y + 300); P(c, None, 9100, y + 300)
        P(d_up, "D_V", 9700, y - 300); P(d_dn, "D_V", 10300, y + 300)
        node = (8000, y)
        Wr((r_in, 2), node, (8600, y), (9100, y), (9700, y), (10300, y))
        Wr((r_lo, 1), (8600, y)); Wr((c, 1), (9100, y)); Wr((d_up, 2), (9700, y)); Wr((d_dn, 1), (10300, y))
        Wr((r_lo, 2), (8600, y + 600), (8850, y + 600), (9100, y + 600), (c, 2))
        L((10300, y), "VU_" + ch, 0, stub=(500, 0))
        L((8850, y + 600), "VMID", 3, stub=(0, 100))
    P("R5", None, 8000, 6700); P("R6", None, 8000, 7300); P("C3", None, 8600, 7300)
    Wr(("R5", 2), (8000, 7000), ("R6", 1)); Wr((8000, 7000), (8600, 7000), ("C3", 1))
    Wr(("R6", 2), (8000, 7600), (8300, 7600), (8600, 7600), ("C3", 2))
    L((8300, 7600), "GND", 3, stub=(0, 100))
    L((8600, 7000), "VMID", 0, stub=(300, 0))
    P("J8", "CONN_4", 10200, 7000)
    for x, y, t in ((800, 1000, "Przelacznik kolumn Marantz / Lampa + pomiar sygnalu do wskaznikow VU - Williamson KT88"),
                    (800, 1120, "Cewki bez pradu: kolumny <- Marantz (NC). Lampa gotowa (ESP32): kolumny <- Lampa (NO). Oba bieguny przelaczane."),
                    (800, 1240, "ESP32 przelacza tylko przy MUTE. RL 100R 2W zostaje na wtornym kazdego toroidu (odczep 4 Ohm - COM)."),
                    (7300, 1600, "POMIAR VU: odczep 4 Ohm PRZED przekaznikiem -> 100k / 5k1 do 1,65 V"),
                    (7300, 1720, "45 W / 4 Ohm = 19 V szczyt -> +-0,92 V na ADC. GND toru VU = masa sterowania,"),
                    (7300, 1840, "NIE laczyc z TUBE_xN na plytce (COM toroidu jest uziemiony na plytce Onyxa)."),
                    (7300, 7900, "J8 -> sterowanie: 3V3, GND, GPIO2 (L), GPIO3 (P)"),
                    (800, 7900, "J7: z plytki sterowania J13 (+12 V, RLY_SPK)")):
        S.note(x, y, t, 60)
    S.autolabel()
    return S


if __name__ == "__main__":
    export(board(), schematic, OUT, NAME, HV, "CZYTAJ_MNIE_glosniki.txt", vp=(560, 300))
