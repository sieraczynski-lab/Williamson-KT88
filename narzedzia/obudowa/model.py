"""Williamson KT88 (plytka Onyxa VA1523) w obudowie Soloist 88 - wariant W2. Wymiary w mm.
Na bazie modelu obudowy Soloist 88 v0.4 (src/case/model.py w repozytorium Soloist-KT88).
Uklad osi: X w prawo (patrzac od przodu), Y do tylu, Z w gore. 0,0,0 = lewy przedni dolny rog dna aluminiowego."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stepw import *
import os

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

# ---------------- plytka Onyxa VA1523 (360 x 160 mm) pod pokrywa
# Od gory: podstawki oktalowe, male rezystory, potencjometry biasu (na srubokret). Wysokie elementy od spodu.
# Plytka stoi na dlugich tulejach M3 przykreconych do dna; podstawki wchodza w otwory pokrywy (pokrywa bez nakretek).
# uklad plytki z rysunku mechanicznego Onyxa: x od lewej, y od tylnej krawedzi (strona KT88)
OB_W, OB_D = 360.0, 160.0
OB_X0, OB_Y1 = 20.0, 302.0            # lewa krawedz plytki, tylna krawedz plytki (Y); przod = Y 142
SOCK_H = 16.0                         # wysokosc podstawki oktalowej nad plytka (zmierzone)
OB_ZTOP = Z_COV + T - SOCK_H          # wierzch plytki: gora podstawki rowno z wierzchem pokrywy (Z 90)

OB_BOTTOM_H = 50.0                    # wysokie elementy pod plytka (kondensatory)
SOCK_HOLE = 30.0                      # otwor na podstawke (srednica korpusu + 1-2 mm)
# oslona lamp: 3 ramki ze stali nierdzewnej 2,5 mm (laser), na tulejach M4 przykreconych do pokrywy
TS = 2.5
G_LEVELS = [Z_COV + T + 30.0, Z_COV + T + 30.0 + TS + 60.0, Z_COV + T + 30.0 + 2 * (TS + 60.0)]   # spody ramek: 136 / 198,5 / 261
G_RIN, G_BAND, G_BAR, G_BOSS, G_FILLET = 28.0, 5.0, 4.0, 8.0, 6.0   # otwor fi 56 (banka fi 52), obwodka 5 mm, mostki 8 mm
_GX = [50.0, 150.0, 250.0, 350.0]; _GY6, _GYK = 172.0, 262.0         # osie 6SN7 / KT88 (jak SMALL / KT)
G_RODS = ([(x, _GY6) for x in (100.0, 200.0, 300.0)]                 # przod: miedzy 6SN7, w osi lamp
          + [(x, (_GY6 + _GYK) / 2) for x in _GX]                     # miedzy 6SN7 i KT88, w osi kazdej lampy
          + [(x, _GYK + 26.0) for x in (100.0, 200.0, 300.0)])        # tyl: miedzy KT88, na wysokosci brzegu banki
POT_HOLE = 8.0                        # otwor na srubokret do potencjometru biasu
def ob(x, y):                          # wspolrzedne z rysunku Onyxa -> obudowa
    return (OB_X0 + x, OB_Y1 - y)
KT = [ob(x, 40.0) for x in (30.0, 130.0, 230.0, 330.0)]          # KT88 (rzad tylny)
SMALL = [ob(x, 130.0) + (n,) for x, n in ((30.0, "V1_L 6SN7"), (130.0, "V2_L 6SN7"), (230.0, "V2_R 6SN7"), (330.0, "V1_R 6SN7"))]
POTS = [ob(x, 40.0) for x in (65.0, 95.0, 265.0, 295.0)]          # osie P101/P102, P201/P202
OB_MH = [ob(x, y) for (x, y) in ((4, 4), (356, 4), (4, 76), (356, 76), (356, 104), (4, 156), (80, 156), (280, 156), (356, 156))]  # (4,104) pomijam: nad puszka selektora
# plytki Soloista na dnie - w przednim rzedzie, bo pod plytka Onyxa sa wysokie elementy
BOARDS_DNO = {"sterowanie": (45.0, 8.0), "zasilacz": (150.0, 8.0)}      # X 255-355 wolne (np. dlawiki 10 H)
MH = {"sterowanie": [(4.5, 4.5), (95.5, 4.5), (4.5, 95.5), (95.5, 95.5)],
      "zasilacz": [(4.5, 4.5), (95.5, 4.5), (4.5, 95.5), (95.5, 95.5)],
      "glosniki": [(4.5, 37.5), (51.0, 37.5), (95.5, 22.0)],
      "ul": [(4.5, 4.5), (78.0, 4.5), (4.5, 61.5), (95.5, 61.5)]}
UL_POS = {"LP": (150.0, 230.0)}                                    # jedna plytka UL 100 x 66 na dnie, na srodku pod plytka Onyxa
SEL_BOX = (24.0, 150.0, 136.0, 210.0)                               # selektor w puszce aluminiowej ok. 112 x 60 x 31 (Hammond 1590), pod plytka
SEL_MH = [(30.0, 156.0), (130.0, 156.0), (30.0, 204.0), (130.0, 204.0)]
TRAFO_POS = {"OT_L": (65.0, 377.0, 120.0, 65.0), "TR1": (200.0, 382.0, 130.0, 65.0), "OT_R": (335.0, 377.0, 120.0, 65.0)}   # przesuniete do przodu: miejsce na zaciski i gniazda z tylu
OT_RAISE = 35.0                      # TG na tulejach: pod nimi gniazda RCA (lewa komora)
YP = D - T                           # wewnetrzna plaszczyzna zdejmowanej tylnej scianki (wchodzi w obudowe, rowno z krawedziami)
RP_CL = 0.5                          # luz tylnej scianki w otworze obudowy (na strone)
# tylna scianka (x, z) - x jak patrzac od przodu, czyli patrzac od tylu lewa komora (TG L) jest po PRAWEJ
RCA = [(x, z) for x in (34.0, 56.0, 78.0, 100.0) for z in (32.0, 13.0)]   # 4 wejscia x (L gora, P dol), komora TG L
SPK_OUT = [(30.0, z) for z in (100.0, 75.0, 50.0)] + [(W - 30.0, z) for z in (100.0, 75.0, 50.0)]  # wyjscia 8 / 4 Ohm / COM
SPK_MAR = [(100.0, z) for z in (88.0, 62.0)] + [(W - 100.0, z) for z in (88.0, 62.0)]                # wejscie z Marantza +/-
IEC = (200.0, 100.0)                 # Schurter DD11 (C14 + bezpiecznik 5x20 + wylacznik 2-bieg.), pionowo, nad TR1
IEC_CUT = (27.1, 56.0); IEC_SCR = 32.5; IEC_DEPTH = 46.6
TRIG_JACK = (140.0, 36.0)
PE_STUD = (260.0, 35.0)
BR_SIDE_Z = [20.0, 120.0]            # wsporniki tylnej scianki (na wpust, klejone): boki
BR_FLOOR_X = [150.0, 250.0, 335.0]   # (w komorze TR1 tylko niskie wsporniki - TR1 obok)   # dno
BR_LID_X = [65.0, 150.0, 250.0, 335.0]   # dach obudowy trafo
BR_LEN, BR_H, BR_TAB = 30.0, 22.0, 20.0  # zaczep z blachy 3 mm: plytka 30 x 22 rownolegla do tylnej scianki, wpust 20 x 3
BR_FL = BR_H
BR_SCR = 11.0                        # os otworu M4 od wewnetrznej powierzchni sciany
CORNER_POSTS = [(11.0, 11.0), (W - 11.0, 11.0), (11.0, Y_BOX - 8.0), (W - 11.0, Y_BOX - 8.0)]   # sruby pokrywy w rogach
GUS = 25.0                             # trojkatne zaczepy pokrywy 25 x 25 x 3, poziomo pod pokrywa
GUS_Z0 = Z_COV - 8.0                   # Z 95-98 (5 mm pod gorna krawedzia scianek)
GUS_TABS = [(5.0, 12.0), (15.0, 22.0)]  # wpusty 7 x 3 na kazdym boku (od naroza)
FEET = [(35.0, 25.0), (365.0, 25.0), (45.0, 440.0), (355.0, 440.0)]
GL_X0, GL_Y0 = 82.0, 330.0
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
         "bottom": tabs([60, 200, 340], -T)}
    outer = edge_features(0, 0, W, D, f)
    H = []
    for x in (60, 200, 340):
        H.append(slot(x, Y_BOX + T / 2, TAB, T))                   # przednia scianka trafo
    for xp in (X_P1, X_P2):
        for y in (335, 385, 435):
            H.append(slot(xp + T / 2, y, T, TAB))                  # przegrody
    for side_, (ux, uy) in UL_POS.items():
        H += [circle(ux + mx, uy + my, 3.5) for (mx, my) in MH["ul"]]   # plytki UL
    H += [circle(x, y, 3.5) for (x, y) in SEL_MH]                      # puszka selektora
    for i in range(10):                                                  # wentylacja pod plytka (srodek)
        for j in range(3):
            H.append(circle(166 + i * 16, 160 + j * 16, 8))
    for (x, y, dd, h) in TRAFO_POS.values():
        H.append(circle(x, y, 8.5))
    for name, (x0, y0) in BOARDS_DNO.items():
        H += [circle(x0 + mx, y0 + my, 3.5) for (mx, my) in board_mh(name)]
    H += [slot(x, YP - T / 2, BR_TAB, T) for x in BR_FLOOR_X]                             # wpusty wspornikow tylnej scianki
    H += [circle(GL_X0 + my, GL_Y0 + mx, 3.5) for (mx, my) in board_mh("glosniki")]      # plytka glosnikow
    H += [circle(x, y, 3.4) for (x, y) in OB_MH]                       # tuleje M3 plytki Onyxa (z dna)
    H += [circle(x, y, 5.0) for (x, y) in FEET]
    return prism("AL_dno_400x460x3", ALU2, outer, H, 0, T, "XY")
parts.append(dno())

# ---------------- SCIANKI BOCZNE (jedna czesc: nisko z przodu, wysoko przy trafo)
FING_FRONT = [(13, 28), (48, 63), (78, 93)]               # z (v) zakresy wypustow do sciany przedniej
BOXFRONT_TABS = [(25, 40), (70, 85), (115, 130)]                     # wypusty przedniej scianki trafo w scianki boczne
def side(name, x0):
    # lokalnie u=y, v=z
    P = [(T, T)]
    for (a, b) in [(c - TAB / 2, c + TAB / 2) for c in (50, 160, 270, 380)]:
        P += [(a, T), (a, 0), (b, 0), (b, T)]
    P.append((D, T))
    P.append((D, Z_LID))
    for (a, b) in sorted([(c - TAB / 2, c + TAB / 2) for c in (335, 385, 435)], reverse=True):
        P += [(b, Z_LID), (b, Z_LID + T), (a, Z_LID + T), (a, Z_LID)]
    P += [(Y_STEP, Z_LID), (Y_STEP, Z_COV), (T, Z_COV)]
    for (a, b) in sorted(FING_FRONT, reverse=True):
        P += [(T, b), (0, b), (0, a), (T, a)]
    H = [slot(Y_BOX + T / 2, (a + b) / 2, T, b - a) for (a, b) in BOXFRONT_TABS]
    H += [circle(y, 53, 4.5) for y in (60, 180, 290, 400)]       # mocowanie bokow drewnianych
    H += [slot(T + (a + b) / 2, GUS_Z0 + T / 2, b - a, T) for (a, b) in GUS_TABS]          # zaczepy pokrywy (przod)
    H += [slot(Y_BOX - (a + b) / 2, GUS_Z0 + T / 2, b - a, T) for (a, b) in GUS_TABS]      # zaczepy pokrywy (tyl)
    H += [slot(YP - T / 2, z, T, BR_TAB) for z in BR_SIDE_Z]       # wpusty wspornikow tylnej scianki
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
    H += [slot(xx, GUS_Z0 + T / 2, b - a, T) for (a, b) in GUS_TABS for xx in (T + (a + b) / 2, W - T - (a + b) / 2)]
    return prism("AL_przod_wewn", ALU, outer, H, 0, T, "XZ")
parts.append(front_wall())

# ---------------- OBUDOWA TRAFO: scianka przednia
PART_END_TABS = [(30, 45), (70, 85), (110, 125)]
def box_front():
    f = {"bottom": tabs([60, 200, 340], T), "top": tabs([60, 200, 340], T),
         "left": [(a, b, T) for (a, b) in BOXFRONT_TABS], "right": [(a, b, T) for (a, b) in BOXFRONT_TABS]}
    P = edge_features(T, T, W - T, Z_LID, f)
    Q = P
    H = [slot(xp + T / 2, (a + b) / 2, T, b - a) for xp in (X_P1, X_P2) for (a, b) in PART_END_TABS]
    H += [circle(x, 40, 16) for x in (65, 185, 215, 335)]          # przepusty przewodow (gumowe)
    H += [slot(xx, GUS_Z0 + T / 2, b - a, T) for (a, b) in GUS_TABS for xx in (T + (a + b) / 2, W - T - (a + b) / 2)]
    for z in (62.0, 74.0, 86.0):                                    # wentylacja komor trafo <-> komora wzmacniacza (pod pokrywa)
        for i in range(32):
            x = 14.0 + i * 12
            if x > 386 or abs(x - (X_P1 + T / 2)) < 10 or abs(x - (X_P2 + T / 2)) < 10: continue
            if any(math.hypot(x - g, z - 40) < 8 + 4 + 3 for g in (65, 185, 215, 335)): continue
            H.append(circle(x, z, 8))
    return prism("AL_trafo_przod", ALU, Q, H, Y_BOX, Y_BOX + T, "XZ")
parts.append(box_front())

def box_rear():
    """Zdejmowana tylna scianka: plaska plyta wchodzaca w otwor obudowy z luzem 0,5 mm, przykrecana M4 do zaczepow."""
    outer = rect(T + RP_CL, T + RP_CL, W - T - RP_CL, Z_LID - RP_CL)
    H = [circle(T + BR_SCR, z, 4.5) for z in BR_SIDE_Z] + [circle(W - T - BR_SCR, z, 4.5) for z in BR_SIDE_Z]
    H += [circle(x, T + BR_SCR, 4.5) for x in BR_FLOOR_X] + [circle(x, Z_LID - BR_SCR, 4.5) for x in BR_LID_X]
    H += [circle(x, z, 11) for (x, z) in RCA]                         # RCA izolowane, 4 pary
    H += [circle(x, z, 9) for (x, z) in SPK_OUT + SPK_MAR]           # zaciski glosnikowe
    cx, cz = IEC
    H.append(rrect(cx - IEC_CUT[0] / 2, cz - IEC_CUT[1] / 2, cx + IEC_CUT[0] / 2, cz + IEC_CUT[1] / 2, 1.0))
    H += [circle(cx, cz - IEC_SCR, 3.4), circle(cx, cz + IEC_SCR, 3.4)]
    H.append(circle(TRIG_JACK[0], TRIG_JACK[1], 6))                   # TRIGGER jack 3,5 mm
    H.append(circle(PE_STUD[0], PE_STUD[1], 4.5))                     # sruba PE
    taken = [(x, z, 4.5) for (x, z) in RCA] + [(x, z, 9) for (x, z) in SPK_OUT + SPK_MAR]
    for z in (108.0, 120.0, 132.0, 144.0):                            # wentylacja: gorna 1/3 scianki
        for i in range(33):
            x = 14.0 + i * 12
            if x > 386: continue
            if abs(x - (X_P1 + T / 2)) < 9 or abs(x - (X_P2 + T / 2)) < 9: continue
            if (x < T + BR_FL + 6 or x > W - T - BR_FL - 6) and 100 < z < 141: continue
            if any(abs(x - bx) < BR_LEN / 2 + 5 for bx in BR_LID_X) and z > Z_LID - BR_FL - 8: continue
            if abs(x - cx) < 20 and abs(z - cz) < 42: continue
            if any(math.hypot(x - a, z - b) < r + 4 + 3 for (a, b, r) in taken): continue
            H.append(circle(x, z, 8))
    return prism("AL_trafo_tyl_zdejmowany", ALU, outer, H, YP, D, "XZ")
def brackets():
    """Zaczepy z blachy aluminiowej 3 mm (jak reszta), plytka 30 x 22 rownolegla do tylnej scianki, tuz za nia
    (Y 454-457); wpust 20 x 3 w gniazdo boku / dna / dachu, klejony. Otwor fi 3,3 pod gwint M4
    albo fi 6 pod nakretke nitowana M4."""
    out = []
    y0, y1 = YP - T, YP
    h = (BR_LEN - BR_TAB) / 2
    for k, z in enumerate(BR_SIDE_Z):
        for side_, sx in (("L", 1), ("P", -1)):
            X = (lambda u: u) if sx == 1 else (lambda u: W - u)
            P = [(X(T), z - BR_LEN / 2), (X(T + BR_H), z - BR_LEN / 2), (X(T + BR_H), z + BR_LEN / 2), (X(T), z + BR_LEN / 2),
                 (X(T), z + BR_TAB / 2), (X(0), z + BR_TAB / 2), (X(0), z - BR_TAB / 2), (X(T), z - BR_TAB / 2)]
            H = [circle(X(T + BR_SCR), z, 3.3)]
            out.append(prism("AL_zaczep_tyl_bok_%s%d" % (side_, k + 1), ALU2, P, H, y0, y1, "XZ"))
    for k, x in enumerate(BR_FLOOR_X):
        P = [(x - BR_LEN / 2, T), (x - BR_TAB / 2, T), (x - BR_TAB / 2, 0), (x + BR_TAB / 2, 0), (x + BR_TAB / 2, T),
             (x + BR_LEN / 2, T), (x + BR_LEN / 2, T + BR_H), (x - BR_LEN / 2, T + BR_H)]
        out.append(prism("AL_zaczep_tyl_dno_%d" % (k + 1), ALU2, P, [circle(x, T + BR_SCR, 3.3)], y0, y1, "XZ"))
    for k, x in enumerate(BR_LID_X):
        P = [(x - BR_LEN / 2, Z_LID - BR_H), (x + BR_LEN / 2, Z_LID - BR_H), (x + BR_LEN / 2, Z_LID), (x + BR_TAB / 2, Z_LID),
             (x + BR_TAB / 2, Z_LID + T), (x - BR_TAB / 2, Z_LID + T), (x - BR_TAB / 2, Z_LID), (x - BR_LEN / 2, Z_LID)]
        out.append(prism("AL_zaczep_tyl_dach_%d" % (k + 1), ALU2, P, [circle(x, Z_LID - BR_SCR, 3.3)], y0, y1, "XZ"))
    return out
parts += brackets()

def gussets():
    """Trojkatne zaczepy pokrywy z blachy 3 mm (przyprostokatne 25 mm), poziomo w rogach komory wzmacniacza,
    po 2 wpusty 7 x 3 w bok i 2 w scianke przednia / przod obudowy trafo, klejone. Otwor fi 3,3 (M4) albo fi 6 (nakretka nitowana)."""
    P = [(T + GUS, T), (T, T + GUS)]
    for (a, b) in sorted(GUS_TABS, reverse=True):
        P += [(T, T + b), (0, T + b), (0, T + a), (T, T + a)]
    P.append((T, T))
    for (a, b) in GUS_TABS:
        P += [(T + a, T), (T + a, 0), (T + b, 0), (T + b, T)]
    out = []
    for name, fx, fy in (("LP", lambda x: x, lambda y: y), ("PP", lambda x: W - x, lambda y: y),
                         ("LT", lambda x: x, lambda y: Y_BOX + T - y), ("PT", lambda x: W - x, lambda y: Y_BOX + T - y)):
        Q = [(fx(x), fy(y)) for (x, y) in P]
        hx, hy = fx(11.0), fy(11.0) if name.endswith("P") else Y_BOX - 8.0
        out.append(prism("AL_zaczep_pokrywy_" + name, ALU2, Q, [circle(hx, hy, 3.3)], GUS_Z0, GUS_Z0 + T, "XY"))
    return out
parts += gussets()

def guard_A():
    """Oslona lamp, WARIANT A: kazda ramka to obwodki 5 mm wokol lamp polaczone mostkami 8 mm przez slupki; zaokraglone
    wciecia (fillet ok. 6 mm) w miejscach polaczen. Kontur z pola odleglosci (smooth union), otwory lamp i slupkow dokladne."""
    import numpy as np
    from skimage import measure
    tubes = [(x, y) for y in (_GY6, _GYK) for x in _GX]
    caps = [((_GX[i], _GY6), (_GX[i + 1], _GY6)) for i in range(3)]             # przod: wzdluz osi 6SN7
    caps += [((x, _GY6), (x, _GYK)) for x in _GX]                                 # miedzy rzedami
    caps += [((_GX[i], _GYK + 26.0), (_GX[i + 1], _GYK + 26.0)) for i in range(3)]   # tyl: na brzegu KT88
    st = 0.2
    xs = np.arange(-5.0, 405.0, st); ys = np.arange(120.0, 320.0, st)
    X, Y = np.meshgrid(xs, ys)
    def smin(a, b, k):
        h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
        return b * (1 - h) + a * h - k * h * (1 - h)
    f = None
    prims = [np.hypot(X - cx, Y - cy) - (G_RIN + G_BAND) for (cx, cy) in tubes]
    prims += [np.hypot(X - cx, Y - cy) - G_BOSS for (cx, cy) in G_RODS]
    for (a, b) in caps:
        ax, ay = a; bx, by = b
        dx, dy = bx - ax, by - ay
        t = np.clip(((X - ax) * dx + (Y - ay) * dy) / (dx * dx + dy * dy), 0, 1)
        prims.append(np.hypot(X - ax - t * dx, Y - ay - t * dy) - G_BAR)
    for p_ in prims:
        f = p_ if f is None else smin(f, p_, G_FILLET)
    loops = []
    for c in measure.find_contours(f, 0.0):
        c = measure.approximate_polygon(c, tolerance=0.02)
        pts = [(float(xs[0] + col * st), float(ys[0] + row * st)) for (row, col) in c[:-1]]
        loops.append(pts)
    loops.sort(key=lambda L: -abs(area2(L)))
    outer, windows = loops[0], loops[1:]
    H = windows + [circle(x, y, 2 * G_RIN) for (x, y) in tubes] + [circle(x, y, 4.5) for (x, y) in G_RODS]
    names = ("dolna", "srodkowa", "gorna")
    return [prism("SS_oslona_lamp_A_%s" % names[k], SS, outer, H, z, z + TS, "XY") for k, z in enumerate(G_LEVELS)]


def guard_B(front="flat", tag="B"):
    """Oslona lamp, WARIANT B: obwodki 5 mm wokol lamp; polaczenia srubowe wyplaszczone - od zewnatrz prosta
    styczna do obwodek, od srodka polokragle wciecie styczne do zewnetrznej krawedzi obwodek (bez wypustek)."""
    import numpy as np
    from skimage import measure
    Ro = G_RIN + G_BAND
    tubes = [(x, y) for y in (_GY6, _GYK) for x in _GX]
    st = 0.2
    xs = np.arange(-5.0, 405.0, st); ys = np.arange(120.0, 320.0, st)
    X, Y = np.meshgrid(xs, ys)
    def disk(c, r): return np.hypot(X - c[0], Y - c[1]) - r
    def poly(P):                                  # wypukly wielokat CCW: max po krawedziach
        P = ccw(P); d = None
        for i in range(len(P)):
            (ax, ay), (bx, by) = P[i], P[(i + 1) % len(P)]
            ex, ey = bx - ax, by - ay; L = math.hypot(ex, ey)
            di = ((X - ax) * ey - (Y - ay) * ex) / L     # >0 na zewnatrz (po prawej krawedzi CCW)
            d = di if d is None else np.maximum(d, di)
        return d
    def unit(v): L = math.hypot(*v); return (v[0] / L, v[1] / L)
    def tan_pt(A, c): u = unit((c[0] - A[0], c[1] - A[1])); return (A[0] + Ro * u[0], A[1] + Ro * u[1])
    def notch_r(A, c): return math.hypot(c[0] - A[0], c[1] - A[1]) - Ro
    f = None
    for c in tubes:
        d = disk(c, Ro); f = d if f is None else np.minimum(f, d)
    webs = []
    for (yA, nrm, sft) in ((_GY6, -1.0, -32.0), (_GYK, +1.0, +3.0)):   # przod / tyl: plaska strona n, wciecie z drugiej
        if yA == _GY6 and front == "waist":                               # wariant C: przod jak boki - przewezenie
            for i in range(3):
                A, B = (_GX[i], yA), (_GX[i + 1], yA)
                xm = (A[0] + B[0]) / 2
                cd, cu = (xm, yA - 32.0), (xm, yA + 32.0)
                r = notch_r(A, cd)
                P = [tan_pt(A, cd), tan_pt(B, cd), tan_pt(B, cu), tan_pt(A, cu)]
                webs.append(np.maximum(np.maximum(poly(P), -disk(cd, r)), -disk(cu, r)))
            continue
        for i in range(3):
            A, B = (_GX[i], yA), (_GX[i + 1], yA)
            nc = ((A[0] + B[0]) / 2, yA + nrm * sft)
            r = notch_r(A, nc)
            P = [tan_pt(A, nc), tan_pt(B, nc), (B[0], yA + nrm * Ro), (A[0], yA + nrm * Ro)]
            webs.append(np.maximum(poly(P), -disk(nc, r)))
    for x in _GX:                                                        # miedzy rzedami: wciecia z obu stron
        A, B = (x, _GY6), (x, _GYK)
        ym = (_GY6 + _GYK) / 2
        cl, cr = (x - 24.0, ym), (x + 24.0, ym)
        r = notch_r(A, cl)
        P = [tan_pt(A, cr), tan_pt(B, cr), tan_pt(B, cl), tan_pt(A, cl)]
        webs.append(np.maximum(np.maximum(poly(P), -disk(cl, r)), -disk(cr, r)))
    for w in webs:
        f = np.minimum(f, w)
    loops = []
    for c in measure.find_contours(f, 0.0):
        c = measure.approximate_polygon(c, tolerance=0.02)
        loops.append([(float(xs[0] + col * st), float(ys[0] + row * st)) for (row, col) in c[:-1]])
    loops.sort(key=lambda L: -abs(area2(L)))
    outer, windows = loops[0], [L for L in loops[1:] if abs(area2(L)) > 20.0]
    H = windows + [circle(x, y, 2 * G_RIN) for (x, y) in tubes] + [circle(x, y, 4.5) for (x, y) in G_RODS]
    names = ("dolna", "srodkowa", "gorna")
    return [prism("SS_oslona_lamp_%s_%s" % (tag, names[k]), SS, outer, H, z, z + TS, "XY") for k, z in enumerate(G_LEVELS)]

def guard_C():
    """Oslona lamp, WARIANT C: jak B (tyl plaski, srodek przewezenia), ale przod jak boki - polokragle obwodki
    6SN7 z przewezeniem i wcieciami z obu stron w miejscu slupka."""
    return guard_B(front="waist", tag="C")

GUARDS = {"A": guard_A, "B": guard_B, "C": guard_C}
GUARD_VARIANT = os.environ.get("OSLONA", "C")
parts += GUARDS[GUARD_VARIANT]()
parts.append(box_rear())

def partition(name, x0):
    f = {"bottom": tabs([335, 385, 435], T), "top": tabs([335, 385, 435], T),
         "left": [(a, b, T) for (a, b) in PART_END_TABS]}
    outer = edge_features(Y_BOX + T, T, D - T, Z_LID, f)
    H = [circle(y, 25, 16) for y in (360, 410)]
    return prism(name, ALU2, outer, H, x0, x0 + T, "YZ")
parts.append(partition("AL_trafo_przegroda_L", X_P1))
parts.append(partition("AL_trafo_przegroda_P", X_P2))

def lid():
    f = {"left": tabs([335, 385, 435], -T), "right": tabs([335, 385, 435], -T)}
    outer = edge_features(0, Y_STEP, W, D, f)
    H = [slot(x, Y_BOX + T / 2, TAB, T) for x in (60, 200, 340)]
    H += [slot(xp + T / 2, y, T, TAB) for xp in (X_P1, X_P2) for y in (335, 385, 435)]
    H += [slot(x, YP - T / 2, BR_TAB, T) for x in BR_LID_X]               # wpusty wspornikow tylnej scianki
    return prism("AL_trafo_dach", ALU, outer, H, Z_LID, Z_LID + T, "XY")
parts.append(lid())

# ---------------- POKRYWA GORNA (zdejmowana, tylko 4 sruby M4 w rogach, w trojkatne zaczepy)
def cover():
    outer = rect(0, 0, W, Y_STEP)
    H = [circle(x, y, 4.5) for (x, y) in CORNER_POSTS]
    H += [circle(x, y, 4.5) for (x, y) in G_RODS]                       # sruby M4 od spodu w tuleje oslony lamp
    socks = [(x, y) for (x, y) in KT] + [(x, y) for (x, y, n) in SMALL]
    H += [circle(x, y, SOCK_HOLE) for (x, y) in socks]
    H += [circle(x, y, POT_HOLE) for (x, y) in POTS]
    def free(x, y, r):
        if any(math.hypot(x - a, y - b) < SOCK_HOLE / 2 + r + 2 for (a, b) in socks): return False
        if any(math.hypot(x - a, y - b) < POT_HOLE / 2 + r + 2 for (a, b) in POTS): return False
        if any(math.hypot(x - a, y - b) < 1.7 + r + 3 for (a, b) in OB_MH): return False
        if any(math.hypot(x - a, y - b) < 2.25 + r + 4 for (a, b) in CORNER_POSTS + G_RODS): return False
        if any(math.hypot(x - a, y - b) < 2 * r + 3 for (a, b) in VENTS): return False
        VENTS.append((x, y))
        return True
    VENTS = []
    for (x, y) in KT:                                                    # jeden wieniec 12 x fi 6 wokol kazdej KT88
        for k in range(12):
            a = math.radians(30.0 * k)
            vx, vy = x + 27.0 * math.cos(a), y + 27.0 * math.sin(a)
            if free(vx, vy, 3.0): H.append(circle(vx, vy, 6.0))
    return prism("AL_pokrywa_gorna", ALU, outer, H, Z_COV, Z_COV + T, "XY")
parts.append(cover())

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
    ref.append(cyl("REF_tuleja_M3_dno_%dmm" % round(ZB - T), BLACK, x, y, 5.5, T, ZB, n=6))
for (x, y) in KT:
    ref.append(cyl("REF_podstawka_oktal", (0.92, 0.90, 0.85), x, y, 28, OB_ZTOP, OB_ZTOP + SOCK_H))
    ref.append(cyl("REF_KT88_cokol", BLACK, x, y, 40, Z_COV + T, Z_COV + T + 26))
    ref.append(cyl("REF_KT88_banka", GLASS, x, y, 52, Z_COV + T + 26, Z_COV + T + 140))
for (x, y, n) in SMALL:
    ref.append(cyl("REF_podstawka_oktal", (0.92, 0.90, 0.85), x, y, 28, OB_ZTOP, OB_ZTOP + SOCK_H))
    ref.append(cyl("REF_" + n.replace(" ", "_") + "_cokol", BLACK, x, y, 40, Z_COV + T, Z_COV + T + 26))
    ref.append(cyl("REF_" + n.replace(" ", "_") + "_Psvane_UK_Plus", GLASS, x, y, 52, Z_COV + T + 26, Z_COV + T + 140))
for (x, y) in G_RODS:
    zs = [Z_COV + T] + [z for zl in G_LEVELS for z in (zl, zl + TS)]
    for k in range(0, len(zs) - 1, 2):
        ref.append(cyl("REF_tuleja_M4_%dmm" % round(zs[k + 1] - zs[k]), (0.75, 0.75, 0.70), x, y, 7, zs[k], zs[k + 1], n=6))
    ref.append(cyl("REF_nakretka_kolpakowa_M4", (0.75, 0.75, 0.70), x, y, 7, G_LEVELS[-1] + TS, G_LEVELS[-1] + TS + 7))
    ref.append(cyl("REF_sruba_M4_spod_pokrywy", BLACK, x, y, 7, Z_COV - 3, Z_COV))
for k, (x, y) in enumerate([ob(xx, 100.0) for xx in (60.0, 100.0, 180.0, 260.0, 300.0)]):
    ref.append(box("REF_kondensatory_pod_plytka_%d" % k, (0.7, 0.15, 0.12), x - 20, y - 10, ZB - OB_BOTTOM_H, x + 20, y + 10, ZB))
for (x, y) in POTS:
    ref.append(cyl("REF_potencjometr_biasu", (0.2, 0.35, 0.8), x, y, 10, OB_ZTOP, OB_ZTOP + 8))
for side_, (ux, uy) in UL_POS.items():
    ref.append(box("REF_plytka_UL_" + side_, PCB, ux, uy, 9, ux + 100, uy + 66, 10.6))
    for (cxb, cyb) in ((17.0, 16.5), (17.0, 40.5), (67.0, 16.5), (67.0, 40.5)):
        ref.append(box("REF_przekaznik_G2RL_UL", BLACK, ux + cxb - 14.4, uy + cyb - 6.25, 10.6, ux + cxb + 14.6, uy + cyb + 6.25, 26.3))
ref.append(box("REF_selektor_puszka_1590", (0.55, 0.57, 0.6), *SEL_BOX[:2], T, SEL_BOX[2], SEL_BOX[3], T + 31))
for name, (x0, y0) in BOARDS_DNO.items():
    ref.append(box("REF_plytka_" + name, PCB, x0, y0, 13, x0 + 100, y0 + 100, 14.6))
for name, (x, y, dd, h) in TRAFO_POS.items():
    z0 = T + 3 + (OT_RAISE if name.startswith("OT") else 0)
    ref.append(cyl("REF_" + name, TRAFO, x, y, dd, z0, z0 + h, hole=20))
    if name.startswith("OT"):
        ref.append(cyl("REF_tuleja_TG_%dmm" % OT_RAISE, BLACK, x, y, 30, T, T + 3 + OT_RAISE, hole=8.5))
for (x, z) in RCA:
    ref.append(cyl("REF_gniazdo_RCA", (0.85, 0.7, 0.2), x, z, 9, D, D + 18, axis="Y"))
    ref.append(cyl("REF_gniazdo_RCA_tyl", (0.85, 0.7, 0.2), x, z, 10, YP - 18, YP, axis="Y"))
x0, y0 = BOARDS_DNO["sterowanie"]
for (mx, my) in board_mh("sterowanie"):
    if True:
        ref.append(cyl("REF_tulejka_M3_ekran", BLACK, x0 + mx, y0 + my, 5.5, 14.6, 47, n=6))
for (x, y) in FEET:
    ref.append(cyl("REF_noga", BLACK, x, y, 40, -15, 0))
for (x, z) in (FR_SEL, FR_VOL):
    ref.append(cyl("REF_galka", (0.6, 0.6, 0.62), x, z, 32, -WOOD - 22, -WOOD, axis="Y"))
ref.append(cyl("REF_przycisk", (0.6, 0.6, 0.62), FR_BTN[0], FR_BTN[1], 16, -WOOD - 3, -WOOD + 5, axis="Y"))
ref.append(cyl("REF_LED_2kol", (0.9, 0.3, 0.2), FR_LED[0], FR_LED[1], 5, -WOOD - 2, -WOOD + 5, axis="Y"))
for (x, z) in FR_DISP:
    ref.append(cyl("REF_wyswietlacz_okragly", BLACK, x, z, 38, -WOOD + 5, -WOOD + 9, axis="Y"))
for k, (x, z) in enumerate(SPK_OUT):
    ref.append(cyl("REF_zacisk_wyjscie", (0.8, 0.1, 0.1) if k % 3 != 2 else BLACK, x, z, 14, D, D + 22, axis="Y"))
    ref.append(cyl("REF_zacisk_tyl", (0.8, 0.7, 0.3), x, z, 10, YP - 25, YP, axis="Y"))
for k, (x, z) in enumerate(SPK_MAR):
    ref.append(cyl("REF_zacisk_Marantz", (0.8, 0.1, 0.1) if k % 2 == 0 else BLACK, x, z, 12, D, D + 18, axis="Y"))
    ref.append(cyl("REF_zacisk_tyl", (0.8, 0.7, 0.3), x, z, 10, YP - 25, YP, axis="Y"))
ref.append(cyl("REF_PE", (0.8, 0.7, 0.3), PE_STUD[0], PE_STUD[1], 10, YP - 8, D + 8, axis="Y"))
ref.append(cyl("REF_gniazdo_trigger_3.5mm", BLACK, TRIG_JACK[0], TRIG_JACK[1], 8, D - T - 12, D + 8, axis="Y"))
ref.append(box("REF_plytka_glosniki", PCB, GL_X0, GL_Y0, 9, GL_X0 + 42, GL_Y0 + 100, 10.6))
for cxb in (30, 72):
    ref.append(box("REF_przekaznik_G2RL", BLACK, GL_X0 + 28 - 6.25, GL_Y0 + cxb - 14.4, 10.6, GL_X0 + 28 + 6.25, GL_Y0 + cxb + 14.4, 26.3))
cx, cz = IEC
ref.append(box("REF_Schurter_DD11_front", BLACK, cx - 16, D, cz - 37.5, cx + 16, D + 4, cz + 37.5))
ref.append(box("REF_Schurter_DD11_korpus", BLACK, cx - IEC_CUT[0] / 2, YP - IEC_DEPTH, cz - IEC_CUT[1] / 2, cx + IEC_CUT[0] / 2, YP, cz + IEC_CUT[1] / 2))
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
