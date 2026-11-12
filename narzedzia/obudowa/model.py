"""Williamson KT88 (plytka Onyxa VA1523) w obudowie Soloist 88 - wariant W1. Wymiary w mm.
Na bazie modelu obudowy Soloist 88 v0.4 (src/case/model.py w repozytorium Soloist-KT88).
Uklad osi: X w prawo (patrzac od przodu), Y do tylu, Z w gore. 0,0,0 = lewy przedni dolny rog dna aluminiowego."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stepw import *

# ================================================================ parametry
T = 3.0          # aluminium
TS = 2.5         # stal nierdzewna oslony lamp
WOOD = 20.0      # MDF + fornir (boki), przod = 5 lico + 15 rama
W, D = 400.0, 460.0          # dno aluminiowe
H_CH = 100.0                 # wysokosc wnetrza czesci lampowej (dno->pokrywa)
Z_COV = T + H_CH             # 103 - spod pokrywy
Y_BOX = 310.0                # przednia scianka obudowy trafo (y 310..313)
Y_STEP = 307.0               # od tego miejsca boczne scianki sa wysokie
Z_LID = 153.0                # spod dachu obudowy trafo
TAB = 15.0                   # dlugosc wypustu
CL = 0.1                     # luz gniazda (na strone)
X_P1, X_P2 = 127.0, 270.0    # przegrody w obudowie trafo

ALU = (0.78, 0.80, 0.83); ALU2 = (0.70, 0.72, 0.76); SS = (0.86, 0.87, 0.88)
WOODC = (0.55, 0.36, 0.20); WOODF = (0.62, 0.43, 0.26)
REFC = (0.25, 0.45, 0.75); GLASS = (0.85, 0.75, 0.55); BLACK = (0.12, 0.12, 0.12); PCB = (0.10, 0.45, 0.20)
TRAFO = (0.30, 0.30, 0.32)

def tabs(centers, d):
    return [(c - TAB / 2, c + TAB / 2, d) for c in centers]
def slot(cu, cv, lu, lv):
    return rect(cu - lu / 2 - CL, cv - lv / 2 - CL, cu + lu / 2 + CL, cv + lv / 2 + CL)

# ---------------- plytka Onyxa VA1523 (360 x 160 mm) jako gorny poklad
# uklad plytki z rysunku mechanicznego Onyxa: x od lewej, y od tylnej krawedzi (strona KT88)
OB_W, OB_D = 360.0, 160.0
OB_X0, OB_Y1 = 20.0, 272.0            # lewa krawedz plytki, tylna krawedz plytki (Y); przod = Y 112
OB_ZTOP = Z_COV + T                   # wierzch plytki rowno z wierzchem pokrywy (Z 106)
def ob(x, y):                          # wspolrzedne z rysunku Onyxa -> obudowa
    return (OB_X0 + x, OB_Y1 - y)
KT = [ob(x, 40.0) for x in (30.0, 130.0, 230.0, 330.0)]          # KT88 (rzad tylny)
SMALL = [ob(x, 130.0) + (n,) for x, n in ((30.0, "V1_L 6SN7"), (130.0, "V2_L 6SN7"), (230.0, "V2_R 6SN7"), (330.0, "V1_R 6SN7"))]
POTS = [ob(x, 40.0) for x in (65.0, 95.0, 265.0, 295.0)]          # osie P101/P102, P201/P202
OB_MH = [ob(x, y) for (x, y) in ((4, 4), (356, 4), (4, 76), (356, 76), (4, 104), (356, 104), (4, 156), (80, 156), (280, 156), (356, 156))]
WIN = (15.0, OB_Y1 - OB_D - 5.0, 385.0, OB_Y1 + 5.0)              # okno w pokrywie, 5 mm odstepu od plytki
# klatka z blachy perforowanej nad plytka
CG_X0, CG_X1, CG_Y0, CG_Y1 = 10.5, 389.5, WIN[1] - 3.5, WIN[3] + 3.5
CG_T = 1.5; CG_Z1 = 275.0; CG_FL = 8.0
# plytki na dnie (x0, y0) - jak w Soloist 88
BOARDS_DNO = {"sterowanie": (150.0, 5.0), "zasilacz_siec": (150.0, 107.0), "zasilacz_hv": (150.0, 209.0)}
MH = {"sterowanie": [(4.5, 4.5), (95.5, 4.5), (4.5, 95.5), (95.5, 95.5)],
      "zasilacz_siec": [(4.5, 4.5), (95.5, 4.5), (4.5, 95.5), (95.5, 95.5)],
      "zasilacz_hv": [(4.5, 4.5), (95.5, 4.5), (67.0, 95.5), (95.5, 95.5)],
      "glosniki": [(4.5, 37.5), (51.0, 37.5), (95.5, 22.0)],
      "ul": [(4.5, 4.5), (4.5, 43.5), (48.0, 24.0)]}
UL_POS = {"L": (40.0, 186.0), "R": (286.0, 186.0)}                # plytki UL 74 x 48 na dnie, pod KT88 kanalu
SEL_BOX = (20.0, 12.0, 132.0, 72.0)                                 # selektor w puszce aluminiowej ok. 112 x 60 x 31 (Hammond 1590)
SEL_MH = [(26.0, 18.0), (126.0, 18.0), (26.0, 66.0), (126.0, 66.0)]
TRAFO_POS = {"OT_L": (65.0, 385.0, 120.0, 65.0), "TR1": (200.0, 385.0, 130.0, 65.0), "OT_R": (335.0, 385.0, 120.0, 65.0)}
OT_RAISE = 35.0
PROF = 20.0; PROF_T = 1.5; PROF_Y0 = 300.0
PROF_X = [T, W - T - PROF]
RCA = [(T + PROF / 2, T + PROF / 2), (W - T - PROF / 2, T + PROF / 2)]
CORNER_POSTS = [(12.0, 12.0), (388.0, 12.0), (12.0, 295.0), (388.0, 295.0)]
FEET = [(35.0, 25.0), (365.0, 25.0), (45.0, 440.0), (355.0, 440.0)]
GL_X0, GL_Y0 = 82.0, 340.0
SPK_MAR = [(35, 100), (60, 100), (340, 100), (365, 100)]
SPK_OUT = [(35, 70), (60, 70), (340, 70), (365, 70)]
TRIG_JACK = (245.0, 45.0)
# sruby klatki M4 w pokrywie (na kolnierzu klatki)
CAGE_SCREWS = [(6.5, y) for y in (125.0, 205.0, 285.0)] + [(393.5, y) for y in (125.0, 205.0, 285.0)] + \
              [(x, CG_Y0 - CG_FL / 2) for x in (60.0, 200.0, 340.0)] + [(x, CG_Y1 + CG_FL / 2) for x in (60.0, 200.0, 340.0)]

# front: (x, z)
FR_BTN, FR_LED, FR_SEL, FR_VOL, FR_IR = (35.0, 48.0), (35.0, 80.0), (100.0, 53.0), (300.0, 53.0), (365.0, 53.0)
FR_DISP = [(165.0, 55.0), (235.0, 55.0)]

def mirror_x(p):
    return (W - p[0], p[1])

def board_mh(name):
    return MH[name]

# ================================================================ czesci
parts = []

# ---------------- DNO
def dno():
    f = {"left": tabs([50, 160, 270, 380], -T), "right": tabs([50, 160, 270, 380], -T),
         "bottom": tabs([60, 200, 340], -T), "top": tabs([60, 200, 340], -T)}
    outer = edge_features(0, 0, W, D, f)
    H = []
    for x in (60, 200, 340):
        H.append(slot(x, Y_BOX + T / 2, TAB, T))                   # przednia scianka trafo
    for xp in (X_P1, X_P2):
        for y in (335, 385, 435):
            H.append(slot(xp + T / 2, y, T, TAB))                  # przegrody
    H += [circle(x, y, 3.5) for (x, y) in OB_MH]                       # tuleje M3 plytki Onyxa (ok. 101 mm)
    for side_, (ux, uy) in UL_POS.items():
        H += [circle(ux + mx, uy + my, 3.5) for (mx, my) in MH["ul"]]   # plytki UL
    H += [circle(x, y, 3.5) for (x, y) in SEL_MH]                      # puszka selektora
    for (xa, xb) in ((30.0, 130.0), (270.0, 370.0)):                   # wentylacja pod plytka
        for i in range(6):
            for j in range(3):
                H.append(circle(xa + 10 + i * 16, 128 + j * 16, 8))
    for (x, y, dd, h) in TRAFO_POS.values():
        H.append(circle(x, y, 8.5))
    for name, (x0, y0) in BOARDS_DNO.items():
        H += [circle(x0 + mx, y0 + my, 3.5) for (mx, my) in board_mh(name)]
    H += [circle(px + PROF / 2, y, 4.5) for px in PROF_X for y in (330, 430)]          # mocowanie profili
    H += [circle(GL_X0 + my, GL_Y0 + mx, 3.5) for (mx, my) in board_mh("glosniki")]      # plytka glosnikow
    H += [circle(x, y, 4.5) for (x, y) in CORNER_POSTS]
    H += [circle(x, y, 5.0) for (x, y) in FEET]
    return prism("AL_dno_400x460x3", ALU2, outer, H, 0, T, "XY")
parts.append(dno())

# ---------------- SCIANKI BOCZNE (jedna czesc: nisko z przodu, wysoko przy trafo)
FING_FRONT = [(13, 28), (48, 63), (78, 93)]               # z (v) zakresy wypustow do sciany przedniej
FING_REAR = [(15, 30), (55, 70), (95, 110), (130, 145)]    # do sciany tylnej
BOXFRONT_TABS = [(25, 40), (70, 85), (115, 130)]                     # wypusty przedniej scianki trafo w scianki boczne
def side(name, x0):
    # lokalnie u=y, v=z
    P = [(T, T)]
    for (a, b) in [(c - TAB / 2, c + TAB / 2) for c in (50, 160, 270, 380)]:
        P += [(a, T), (a, 0), (b, 0), (b, T)]
    P.append((D - T, T))
    for (a, b) in FING_REAR:
        P += [(D - T, a), (D, a), (D, b), (D - T, b)]
    P.append((D - T, Z_LID))
    for (a, b) in sorted([(c - TAB / 2, c + TAB / 2) for c in (335, 385, 435)], reverse=True):
        P += [(b, Z_LID), (b, Z_LID + T), (a, Z_LID + T), (a, Z_LID)]
    P += [(Y_STEP, Z_LID), (Y_STEP, Z_COV), (T, Z_COV)]
    for (a, b) in sorted(FING_FRONT, reverse=True):
        P += [(T, b), (0, b), (0, a), (T, a)]
    H = [slot(Y_BOX + T / 2, (a + b) / 2, T, b - a) for (a, b) in BOXFRONT_TABS]
    H += [circle(y, 53, 4.5) for y in (60, 180, 290, 400)]       # mocowanie bokow drewnianych
    return prism(name, ALU, P, H, x0, x0 + T, "YZ")
parts.append(side("AL_bok_lewy", 0.0))
parts.append(side("AL_bok_prawy", W - T))

# ---------------- PRZEDNIA SCIANKA ALUMINIOWA (za frontem drewnianym)
def front_wall():
    f = {"bottom": tabs([60, 200, 340], T),
         "left": [(a, b, -T) for (a, b) in FING_FRONT], "right": [(a, b, -T) for (a, b) in FING_FRONT]}
    outer = edge_features(0, T, W, Z_COV, f)
    H = [circle(*FR_BTN, 22), circle(*FR_LED, 10), circle(*FR_SEL, 7.5), circle(*FR_VOL, 7.5), circle(*FR_IR, 12)]
    H += [rect(x - 12, z - 6, x + 12, z + 6) for (x, z) in FR_DISP]
    H += [circle(x, z, 4.5) for (x, z) in ((60, 20), (340, 20), (200, 20), (200, 90))]
    return prism("AL_przod_wewn", ALU, outer, H, 0, T, "XZ")
parts.append(front_wall())

# ---------------- OBUDOWA TRAFO: scianka przednia
PART_END_TABS = [(30, 45), (70, 85), (110, 125)]
def box_front():
    f = {"bottom": tabs([60, 200, 340], T), "top": tabs([60, 200, 340], T),
         "left": [(a, b, T) for (a, b) in BOXFRONT_TABS], "right": [(a, b, T) for (a, b) in BOXFRONT_TABS]}
    P = edge_features(T, T, W - T, Z_LID, f)
    # wyciecia na profile w dolnych rogach (x T..T+PROF+0.5, z T..T+PROF+0.5)
    nb = T + PROF + 0.5
    Q = []
    for (u, v) in P:
        if abs(v - T) < 1e-6 and abs(u - T) < 1e-6:
            Q += [(T, nb), (T + PROF + 0.5, nb), (T + PROF + 0.5, T)]
        elif abs(v - T) < 1e-6 and abs(u - (W - T)) < 1e-6:
            Q += [(W - T - PROF - 0.5, T), (W - T - PROF - 0.5, nb), (W - T, nb)]
        else:
            Q.append((u, v))
    H = [slot(xp + T / 2, (a + b) / 2, T, b - a) for xp in (X_P1, X_P2) for (a, b) in PART_END_TABS]
    H += [circle(x, 40, 16) for x in (65, 185, 215, 335)]          # przepusty przewodow (gumowe)
    return prism("AL_trafo_przod", ALU, Q, H, Y_BOX, Y_BOX + T, "XZ")
parts.append(box_front())

def box_rear():
    f = {"bottom": tabs([60, 200, 340], T), "top": tabs([60, 200, 340], T),
         "left": [(a, b, -T) for (a, b) in FING_REAR], "right": [(a, b, -T) for (a, b) in FING_REAR]}
    outer = edge_features(0, T, W, Z_LID, f)
    H = [slot(xp + T / 2, (a + b) / 2, T, b - a) for xp in (X_P1, X_P2) for (a, b) in PART_END_TABS]
    H.append(rect(200 - 13.75, 45 - 16, 200 + 13.75, 45 + 16))      # gniazdo IEC C14 z bezpiecznikiem
    H += [circle(x, z, 9) for (x, z) in SPK_MAR + SPK_OUT]          # zaciski glosnikowe: gora z Marantza, dol do kolumn
    H.append(circle(TRIG_JACK[0], TRIG_JACK[1], 6))                   # gniazdo TRIGGER 3,5 mm (otwor 6 mm, wersja panelowa)
    H.append(circle(200, 110, 4.5))                                   # zacisk PE / masa
    H += [circle(x, z, 10) for (x, z) in RCA]                         # gniazda RCA (izolowane) w osi profili
    return prism("AL_trafo_tyl", ALU, outer, H, D - T, D, "XZ")
parts.append(box_rear())

def partition(name, x0):
    f = {"bottom": tabs([335, 385, 435], T), "top": tabs([335, 385, 435], T),
         "left": [(a, b, T) for (a, b) in PART_END_TABS], "right": [(a, b, T) for (a, b) in PART_END_TABS]}
    outer = edge_features(Y_BOX + T, T, D - T, Z_LID, f)
    H = [circle(y, 25, 16) for y in (360, 410)]
    return prism(name, ALU2, outer, H, x0, x0 + T, "YZ")
parts.append(partition("AL_trafo_przegroda_L", X_P1))
parts.append(partition("AL_trafo_przegroda_P", X_P2))

def lid():
    f = {"left": tabs([335, 385, 435], -T), "right": tabs([335, 385, 435], -T), "top": tabs([60, 200, 340], -T)}
    outer = edge_features(0, Y_STEP, W, D, f)
    H = [slot(x, Y_BOX + T / 2, TAB, T) for x in (60, 200, 340)]
    H += [slot(xp + T / 2, y, T, TAB) for xp in (X_P1, X_P2) for y in (335, 385, 435)]
    for (xa, xb) in ((15, 115), (142, 258), (285, 385)):
        nx = int((xb - xa) // 12)
        for i in range(nx + 1):
            for j in range(10):
                x = xa + (xb - xa - nx * 12) / 2 + i * 12
                y = 330 + j * 12
                if abs(y - 345) < 9 or abs(y - 425) < 9:
                    pass
                H.append(circle(x, y, 6))
    return prism("AL_trafo_dach", ALU, outer, H, Z_LID, Z_LID + T, "XY")
parts.append(lid())

# ---------------- POKRYWA GORNA z oknem na plytke Onyxa (zdejmowana, 4 wkrety w rogach)
def cover():
    outer = rect(0, 0, W, Y_STEP)
    H = [circle(x, y, 4.5) for (x, y) in CORNER_POSTS]
    H.append(rect(*WIN))
    H += [circle(x, y, 4.5) for (x, y) in CAGE_SCREWS]
    for i in range(7):                                   # wentylacja nad sterowaniem / zasilaczem sieciowym
        for j in range(6):
            H.append(circle(164 + i * 12, 22 + j * 12, 6))
    return prism("AL_pokrywa_gorna", ALU, outer, H, Z_COV, Z_COV + T, "XY")
parts.append(cover())

# ---------------- KLATKA nad plytka (stal nierdzewna perforowana 1,5 mm, np. Rv 5-8)
PERF = (0.80, 0.82, 0.84)
def cage():
    z0, z1 = Z_COV + T, CG_Z1
    out = []
    out.append(prism("SS_klatka_gora_perforowana", PERF, rect(CG_X0, CG_Y0, CG_X1, CG_Y1), [], z1 - CG_T, z1, "XY"))
    out.append(prism("SS_klatka_przod_perforowana", PERF, rect(CG_X0, z0, CG_X1, z1 - CG_T), [], CG_Y0, CG_Y0 + CG_T, "XZ"))
    out.append(prism("SS_klatka_tyl_perforowana", PERF, rect(CG_X0, z0, CG_X1, z1 - CG_T), [], CG_Y1 - CG_T, CG_Y1, "XZ"))
    out.append(prism("SS_klatka_bok_L_perforowana", PERF, rect(CG_Y0 + CG_T, z0, CG_Y1 - CG_T, z1 - CG_T), [], CG_X0, CG_X0 + CG_T, "YZ"))
    out.append(prism("SS_klatka_bok_P_perforowana", PERF, rect(CG_Y0 + CG_T, z0, CG_Y1 - CG_T, z1 - CG_T), [], CG_X1 - CG_T, CG_X1, "YZ"))
    # kolnierz dolny (lezy na pokrywie), z otworami na sruby M4 i luzem na leby sruby pokrywy
    fo = rect(CG_X0 - CG_FL, CG_Y0 - CG_FL, CG_X1 + CG_FL, CG_Y1 + CG_FL)
    fh = [rect(CG_X0 + CG_T, CG_Y0 + CG_T, CG_X1 - CG_T, CG_Y1 - CG_T)]
    fh += [circle(x, y, 4.5) for (x, y) in CAGE_SCREWS]
    fh += [circle(x, y, 10) for (x, y) in CORNER_POSTS if CG_Y0 - CG_FL < y < CG_Y1 + CG_FL]
    out.append(prism("SS_klatka_kolnierz", PERF, fo, fh, z0, z0 + CG_T, "XY"))
    return out
parts += cage()

# ---------------- PROFILE STALOWE na przewody wejsciowe (pod podniesionymi TG)
STEEL = (0.18, 0.18, 0.2)
for k, px in enumerate(PROF_X):
    tag = "L" if k == 0 else "P"
    outer = rect(px, T, px + PROF, T + PROF)
    inner = rect(px + PROF_T, T + PROF_T, px + PROF - PROF_T, T + PROF - PROF_T)
    parts.append(prism("ST_profil_20x20x1.5_%s_dl%d" % (tag, int(D - T - PROF_Y0)), STEEL, outer, [inner], PROF_Y0, D - T, "XZ"))

# ---------------- EKRAN NAD PLYTKA STEROWANIA (aluminium, na tulejach M3 30 mm)
def screen():
    x0, y0 = BOARDS_DNO["sterowanie"]
    o = rect(x0 - 2, y0 + 0.5, x0 + 102, y0 + 101)
    H = [circle(x0 + mx, y0 + my, 3.4) for (mx, my) in board_mh("sterowanie")]
    H += [rect(x0 + 5, y0 + 20, x0 + 30, y0 + 30)]                     # przepust tasm/przewodow
    return prism("AL_ekran_sterowania", ALU2, o, H, 47, 47 + T, "XY")
parts.append(screen())

# ---------------- DREWNO
def wood_front():
    X0, X1 = -WOOD, W + WOOD
    skin_h = [circle(*FR_BTN, 16.2), circle(*FR_LED, 5.2), circle(*FR_SEL, 9), circle(*FR_VOL, 9), circle(*FR_IR, 6)]
    skin_h += [circle(x, z, 33) for (x, z) in FR_DISP]
    frame_h = [circle(*FR_BTN, 26), circle(*FR_LED, 12), circle(*FR_SEL, 30), circle(*FR_VOL, 30), circle(*FR_IR, 14)]
    frame_h += [circle(x, z, 40) for (x, z) in FR_DISP]
    return [prism("DREWNO_front_lico_5mm", WOODF, rect(X0, 0, X1, Z_COV + T), skin_h, -WOOD, -WOOD + 5, "XZ"),
            prism("DREWNO_front_rama_15mm", WOODC, rect(X0, 0, X1, Z_COV + T), frame_h, -WOOD + 5, 0, "XZ")]
parts += wood_front()
parts.append(prism("DREWNO_bok_lewy", WOODF, rect(0, 0, D, Z_COV + T), [], -WOOD, 0, "YZ"))
parts.append(prism("DREWNO_bok_prawy", WOODF, rect(0, 0, D, Z_COV + T), [], W, W + WOOD, "YZ"))

# ================================================================ elementy odniesienia (REF)
ref = []
ZB = OB_ZTOP - 1.6
ref.append(box("REF_plytka_Onyx_VA1523", PCB, OB_X0, OB_Y1 - OB_D, ZB, OB_X0 + OB_W, OB_Y1, OB_ZTOP))
for (x, y) in OB_MH:
    ref.append(cyl("REF_tuleja_M3_101mm", BLACK, x, y, 5.5, T, ZB, n=6))
for (x, y) in KT:
    ref.append(cyl("REF_podstawka_oktal", (0.92, 0.90, 0.85), x, y, 32, OB_ZTOP, OB_ZTOP + 12))
    ref.append(cyl("REF_KT88_cokol", BLACK, x, y, 40, OB_ZTOP + 12, OB_ZTOP + 38))
    ref.append(cyl("REF_KT88_banka", GLASS, x, y, 52, OB_ZTOP + 38, OB_ZTOP + 152))
for (x, y, n) in SMALL:
    ref.append(cyl("REF_podstawka_oktal", (0.92, 0.90, 0.85), x, y, 32, OB_ZTOP, OB_ZTOP + 12))
    ref.append(cyl("REF_" + n.replace(" ", "_") + "_butelka", GLASS, x, y, 47, OB_ZTOP + 12, OB_ZTOP + 125))
for k, (x, y) in enumerate([ob(xx, 100.0) for xx in (60.0, 100.0, 180.0, 260.0, 300.0)]):
    ref.append(box("REF_kondensatory_Onyx_%d" % k, (0.7, 0.15, 0.12), x - 20, y - 10, OB_ZTOP, x + 20, y + 10, OB_ZTOP + 48))
for (x, y) in POTS:
    ref.append(cyl("REF_potencjometr_biasu", (0.2, 0.35, 0.8), x, y, 16, OB_ZTOP, OB_ZTOP + 14))
for side_, (ux, uy) in UL_POS.items():
    ref.append(box("REF_plytka_UL_" + side_, PCB, ux, uy, 9, ux + 74, uy + 48, 10.6))
    for cxb in (20.0, 52.0):
        ref.append(box("REF_przekaznik_G2RL_UL", BLACK, ux + cxb - 6.25, uy + 24 - 14.4, 10.6, ux + cxb + 6.25, uy + 24 + 14.4, 26.3))
ref.append(box("REF_selektor_puszka_1590", (0.55, 0.57, 0.6), *SEL_BOX[:2], T, SEL_BOX[2], SEL_BOX[3], T + 31))
for name, (x0, y0) in BOARDS_DNO.items():
    ref.append(box("REF_plytka_" + name, PCB, x0, y0, 13, x0 + 100, y0 + 100, 14.6))
for k, (cx, cy) in enumerate([(16, 84), (47, 84), (16, 53), (47, 53)]):
    x0, y0 = BOARDS_DNO["zasilacz_hv"]
    ref.append(cyl("REF_C_snapin_%d" % k, BLACK, x0 + cx, y0 + cy, 30, 14.6, 64.6))
for name, (x, y, dd, h) in TRAFO_POS.items():
    z0 = T + 3 + (OT_RAISE if name.startswith("OT") else 0)
    ref.append(cyl("REF_" + name, TRAFO, x, y, dd, z0, z0 + h, hole=20))
    if name.startswith("OT"):
        ref.append(cyl("REF_tuleja_TG_%dmm" % OT_RAISE, BLACK, x, y, 30, T, T + 3 + OT_RAISE, hole=8.5))
for (x, z) in RCA:
    ref.append(cyl("REF_gniazdo_RCA", (0.85, 0.7, 0.2), x, z, 9, D, D + 18, axis="Y"))
x0, y0 = BOARDS_DNO["sterowanie"]
for (mx, my) in board_mh("sterowanie"):
    if True:
        ref.append(cyl("REF_tulejka_M3_ekran", BLACK, x0 + mx, y0 + my, 5.5, 14.6, 47, n=6))
ref.append(cyl("REF_dlawik_L1", (0.35, 0.25, 0.25), 200, 385, 105, T + 3 + 65 + 3, T + 3 + 65 + 3 + 55, hole=20))
for (x, y) in CORNER_POSTS:
    ref.append(cyl("REF_tulejka_M4_100mm", BLACK, x, y, 7, T, Z_COV, n=6))
for (x, y) in FEET:
    ref.append(cyl("REF_noga", BLACK, x, y, 40, -15, 0))
for (x, z) in (FR_SEL, FR_VOL):
    ref.append(cyl("REF_galka", (0.6, 0.6, 0.62), x, z, 32, -WOOD - 22, -WOOD, axis="Y"))
ref.append(cyl("REF_przycisk", (0.6, 0.6, 0.62), FR_BTN[0], FR_BTN[1], 16, -WOOD - 3, -WOOD + 5, axis="Y"))
ref.append(cyl("REF_LED_2kol", (0.9, 0.3, 0.2), FR_LED[0], FR_LED[1], 5, -WOOD - 2, -WOOD + 5, axis="Y"))
for (x, z) in FR_DISP:
    ref.append(cyl("REF_wyswietlacz_okragly", BLACK, x, z, 38, -WOOD + 5, -WOOD + 9, axis="Y"))
for k, (x, z) in enumerate(SPK_MAR + SPK_OUT):
    ref.append(cyl("REF_zacisk_glosnikowy", (0.8, 0.1, 0.1) if k % 2 == 0 else BLACK, x, z, 12, D, D + 22, axis="Y"))
ref.append(cyl("REF_gniazdo_trigger_3.5mm", BLACK, TRIG_JACK[0], TRIG_JACK[1], 8, D - T - 12, D + 8, axis="Y"))
ref.append(box("REF_plytka_glosniki", PCB, GL_X0, GL_Y0, 9, GL_X0 + 42, GL_Y0 + 100, 10.6))
for cxb in (30, 72):
    ref.append(box("REF_przekaznik_G2RL", BLACK, GL_X0 + 28 - 6.25, GL_Y0 + cxb - 14.4, 10.6, GL_X0 + 28 + 6.25, GL_Y0 + cxb + 14.4, 26.3))
ref.append(box("REF_gniazdo_IEC", BLACK, 200 - 15, D, 45 - 17, 200 + 15, D + 4, 45 + 17))  # placeholder (orientacja XY)
for S in ref:
    S.ref = True

if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    bad = 0
    for S in parts + ref:
        b = check_closed(S); v = volume(S)
        if b or v <= 0:
            print("PROBLEM", S.name, b, v); bad += 1
    print("parts", len(parts), "ref", len(ref), "problems", bad)
    write_step(os.path.join(out, "Williamson_obudowa.step"), parts, "Williamson_obudowa")
    write_step(os.path.join(out, "Williamson_obudowa_z_elementami.step"), parts + ref, "Williamson_obudowa_z_elementami")
