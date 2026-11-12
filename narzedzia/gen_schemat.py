import math

S = []  # svg parts for current drawing

def add(s): S.append(s)

def wire(*pts, cls="w"):
    add('<polyline class="%s" points="%s"/>' % (cls, " ".join("%g,%g" % p for p in pts)))

def dot(x, y):
    add('<circle class="dot" cx="%g" cy="%g" r="3.2"/>' % (x, y))

def txt(x, y, s, cls="val", anchor="start"):
    add('<text class="%s" x="%g" y="%g" text-anchor="%s">%s</text>' % (cls, x, y, anchor, s))

def label2(x, y, ref, val, anchor="start", chg=False):
    c = " chg" if chg else ""
    txt(x, y, ref, "ref" + c, anchor)
    txt(x, y + 14, val, "val" + c, anchor)

def res_v(x, y1, y2, ref, val, side="r", chg=False, body=46):
    m = (y1 + y2) / 2
    b1, b2 = m - body / 2, m + body / 2
    wire((x, y1), (x, b1)); wire((x, b2), (x, y2))
    add('<rect class="part%s" x="%g" y="%g" width="14" height="%g"/>' % (" chgp" if chg else "", x - 7, b1, body))
    if side == "r":
        label2(x + 13, m - 3, ref, val, "start", chg)
    else:
        label2(x - 13, m - 3, ref, val, "end", chg)

def res_h(x1, x2, y, ref, val, above=True, chg=False, body=46):
    m = (x1 + x2) / 2
    b1, b2 = m - body / 2, m + body / 2
    wire((x1, y), (b1, y)); wire((b2, y), (x2, y))
    add('<rect class="part%s" x="%g" y="%g" width="%g" height="14"/>' % (" chgp" if chg else "", b1, y - 7, body))
    if above:
        label2(m, y - 26, ref, val, "middle", chg)
    else:
        label2(m, y + 22, ref, val, "middle", chg)

def cap_h(x1, x2, y, ref, val, above=True, chg=False):
    m = (x1 + x2) / 2
    wire((x1, y), (m - 4, y)); wire((m + 4, y), (x2, y))
    c = "plate chgp" if chg else "plate"
    add('<line class="%s" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (c, m - 4, y - 12, m - 4, y + 12))
    add('<line class="%s" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (c, m + 4, y - 12, m + 4, y + 12))
    if above:
        label2(m, y - 30, ref, val, "middle", chg)
    else:
        label2(m, y + 26, ref, val, "middle", chg)

def cap_v(x, y1, y2, ref, val, side="r", polar=False, chg=False):
    m = (y1 + y2) / 2
    wire((x, y1), (x, m - 4)); wire((x, m + 4), (x, y2))
    c = "plate chgp" if chg else "plate"
    add('<line class="%s" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (c, x - 12, m - 4, x + 12, m - 4))
    if polar:
        add('<path class="%s" d="M%g %g Q%g %g %g %g" fill="none"/>' % (c, x - 12, m + 7, x, m + 1, x + 12, m + 7))
        txt(x + 18 if side == "l" else x - 18, m - 7, "+", "pol", "middle")
    else:
        add('<line class="%s" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (c, x - 12, m + 4, x + 12, m + 4))
    if side == "r":
        label2(x + 17, m - 3, ref, val, "start", chg)
    else:
        label2(x - 17, m - 3, ref, val, "end", chg)

def gnd(x, y, stub=12):
    wire((x, y), (x, y + stub))
    yy = y + stub
    add('<line class="w" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x - 10, yy, x + 10, yy))
    add('<line class="w" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x - 6, yy + 4, x + 6, yy + 4))
    add('<line class="w" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x - 2.5, yy + 8, x + 2.5, yy + 8))

def flag(x, y, s, d="up", stub=14, chg=False):
    c = "rail chg" if chg else "rail"
    if d == "up":
        wire((x, y), (x, y - stub))
        yy = y - stub
        add('<path class="flagm" d="M%g %g L%g %g L%g %g Z"/>' % (x - 6, yy, x + 6, yy, x, yy - 8))
        txt(x, yy - 13, s, c, "middle")
    elif d == "down":
        wire((x, y), (x, y + stub))
        yy = y + stub
        add('<path class="flagm" d="M%g %g L%g %g L%g %g Z"/>' % (x - 6, yy, x + 6, yy, x, yy + 8))
        txt(x, yy + 22, s, c, "middle")
    elif d == "right":
        wire((x, y), (x + stub, y))
        xx = x + stub
        add('<path class="flagm" d="M%g %g L%g %g L%g %g Z"/>' % (xx, y - 6, xx, y + 6, xx + 8, y))
        txt(xx + 13, y + 4, s, c, "start")

def pot_v(x, y1, y2, wy, wx, ref, val, side="r", chg=False, body=50):
    m = (y1 + y2) / 2
    b1, b2 = m - body / 2, m + body / 2
    wire((x, y1), (x, b1)); wire((x, b2), (x, y2))
    add('<rect class="part%s" x="%g" y="%g" width="14" height="%g"/>' % (" chgp" if chg else "", x - 7, b1, body))
    # wiper arrow from wx to body edge
    if wx > x:
        wire((wx, wy), (x + 9, wy))
        add('<path class="flagm" d="M%g %g L%g %g L%g %g Z"/>' % (x + 8, wy, x + 16, wy - 5, x + 16, wy + 5))
    else:
        wire((wx, wy), (x - 9, wy))
        add('<path class="flagm" d="M%g %g L%g %g L%g %g Z"/>' % (x - 8, wy, x - 16, wy - 5, x - 16, wy + 5))
    if side == "rr":
        label2(x + 13, m - 3, ref, val, "start", chg)
    elif side == "r":
        label2(x + 13, b1 - 18, ref, val, "start", chg)
    else:
        label2(x - 13, m - 3, ref, val, "end", chg)

def triode(cx, cy, inv=False, name="", r=34):
    s = -1 if inv else 1
    add('<circle class="tube" cx="%g" cy="%g" r="%g"/>' % (cx, cy, r))
    ya = cy - 14 * s
    add('<line class="el" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (cx - 13, ya, cx + 13, ya))
    wire((cx, ya), (cx, cy - r * s))
    add('<line class="el grid" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (cx - 13, cy, cx + 13, cy))
    wire((cx - r, cy), (cx - 13, cy))
    yk = cy + 14 * s
    add('<polyline class="el" points="%g,%g %g,%g %g,%g"/>' % (cx - 13, yk + 5 * s, cx - 13, yk, cx + 13, yk))
    wire((cx, yk), (cx, cy + r * s))

def tetrode(cx, cy, inv=False, r=40):
    s = -1 if inv else 1
    add('<circle class="tube" cx="%g" cy="%g" r="%g"/>' % (cx, cy, r))
    ya = cy - 22 * s
    add('<line class="el" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (cx - 15, ya, cx + 15, ya))
    wire((cx, ya), (cx, cy - r * s))
    yg2 = cy - 8 * s
    add('<line class="el grid" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (cx - 15, yg2, cx + 15, yg2))
    wire((cx + 15, yg2), (cx + r, yg2))
    yg1 = cy + 6 * s
    add('<line class="el grid" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (cx - 15, yg1, cx + 15, yg1))
    wire((cx - r, yg1), (cx - 15, yg1))
    yk = cy + 22 * s
    add('<polyline class="el" points="%g,%g %g,%g %g,%g"/>' % (cx - 15, yk + 5 * s, cx - 15, yk, cx + 15, yk))
    wire((cx, yk), (cx, cy + r * s))
    # beam plates
    add('<path class="el grid" d="M%g %g Q%g %g %g %g"/>' % (cx - 24, yk - 2 * s, cx - 27, cy, cx - 24, ya + 6 * s))
    add('<path class="el grid" d="M%g %g Q%g %g %g %g"/>' % (cx + 24, yk - 2 * s, cx + 27, cy, cx + 24, ya + 6 * s))

def coil_v(x, ys, bulge=1, cls="coil"):
    """ys: list of tap y's (sorted). bulge +1 right, -1 left"""
    d = "M%g %g" % (x, ys[0])
    for a, b in zip(ys[:-1], ys[1:]):
        L = b - a
        n = max(1, round(L / 16))
        h = L / n
        for i in range(n):
            y0 = a + i * h
            d += " A%g %g 0 0 %d %g %g" % (h / 2, h / 2, 1 if bulge > 0 else 0, x, y0 + h)
    add('<path class="%s" d="%s"/>' % (cls, d))

def coil_h(x1, x2, y, ref, val):
    L = x2 - x1
    n = max(1, round(L / 18)); h = L / n
    d = "M%g %g" % (x1, y)
    for i in range(n):
        d += " A%g %g 0 0 1 %g %g" % (h / 2, h / 2, x1 + (i + 1) * h, y)
    add('<path class="coil" d="%s"/>' % d)
    label2((x1 + x2) / 2, y - 30, ref, val, "middle")

def diode_h(x1, x2, y, ref, val, left=True):
    m = (x1 + x2) / 2
    wire((x1, y), (m - 9, y)); wire((m + 9, y), (x2, y))
    if left:  # anode right, cathode left -> arrow points left
        add('<path class="flagm" d="M%g %g L%g %g L%g %g Z"/>' % (m + 9, y - 9, m + 9, y + 9, m - 7, y))
        add('<line class="plate" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (m - 8, y - 9, m - 8, y + 9))
    label2(m, y - 26, ref, val, "middle")

def tube_label(x, y, name, typ, anchor="end"):
    txt(x, y, name, "tref", anchor)
    txt(x, y + 15, typ, "ttyp", anchor)

def op(x, y, lines, anchor="start"):
    for i, l in enumerate(lines):
        txt(x, y + i * 13, l, "op", anchor)

def term(x, y):
    add('<circle class="term" cx="%g" cy="%g" r="5"/>' % (x, y))

# ===================== AMPLIFIER (one channel, wg VA1523 Onyxa) =====================
def cap_pair_v(x, y1, y2, ref, val, side="l"):
    """szeregowa para elektrolitów z rezystorami wyrównującymi, rysowana jako jeden kondensator"""
    cap_v(x, y1, y2, ref, val, side=side, polar=True)

def amp():
    S.clear()
    # --- wejście ---
    term(30, 560); txt(30, 545, "J100", "ref", "middle"); txt(30, 590, "WE", "val", "middle")
    wire((35, 560), (150, 560)); dot(80, 560)
    res_v(80, 560, 660, "R101", "1 M", side="l", body=40); gnd(80, 660)
    res_h(80, 156, 560, "R100", "1 k", above=True, body=36)
    # V1B wejście
    triode(190, 560); txt(176, 615, "V1B", "tref", "end"); txt(176, 630, "½ 6SN7", "ttyp", "end")
    op(232, 548, ["wejście", "Ia ≈ 3,7 mA", "Ua ≈ 89 V", "A ≈ 14"])
    wire((190, 526), (190, 460)); dot(190, 460)
    res_v(190, 380, 460, "R103", "47 k 1 W", side="r", body=40)
    dot(190, 380)
    res_v(190, 290, 380, "R106", "33 k 1 W", side="l", body=40)
    flag(190, 290, "Uaa")
    wire((190, 380), (120, 380)); cap_pair_v(120, 380, 450, "C110+C111", "2×120 µ/400 V", side="l"); gnd(120, 450)
    # katoda V1B: R104 zbocznikowany C102, R105 = punkt wejścia NFB
    wire((190, 594), (190, 630)); dot(190, 630)
    res_v(190, 630, 690, "R104", "47 Ω", side="r", body=30)
    wire((190, 630), (140, 630)); cap_v(140, 630, 690, "C102", "47 µ/25 V", side="l", polar=True); wire((140, 690), (190, 690))
    dot(190, 690)
    res_v(190, 690, 770, "R105", "470 Ω", side="l", body=36); gnd(190, 770)
    wire((190, 690), (260, 690), (260, 860), (300, 860)); dot(300, 860)
    res_h(300, 430, 860, "R129", "22 k* (dobrać)", above=True, chg=True)
    wire((300, 860), (300, 902)); cap_h(300, 430, 902, "C123", "n.m. · ew. 33–150 p", above=False, chg=True)
    wire((430, 902), (430, 860)); dot(430, 860)
    wire((430, 860), (1340, 860), (1340, 300))
    term(1000, 860); txt(1000, 848, "J102 FB", "ref chg", "middle")
    txt(790, 852, "sprzężenie zwrotne z odczepu 8 Ω (ok. 10 dB)", "net", "middle")
    # V1A katodyna
    wire((190, 460), (260, 460), (260, 440), (296, 440))
    triode(330, 440); txt(316, 497, "V1A", "tref", "end"); txt(316, 512, "½ 6SN7", "ttyp", "end")
    op(345, 520, ["katodyna", "Ia ≈ 4,2 mA", "Uk ≈ 92 V", "Ua ≈ 198 V"])
    wire((330, 406), (330, 260)); dot(330, 260)
    res_v(330, 170, 260, "R107", "22 k 3 W", side="l", body=40)
    dot(330, 170)
    res_v(330, 80, 170, "R109", "22 k 1 W", side="r", body=40)
    flag(330, 80, "Uaa")
    wire((330, 170), (260, 170)); cap_pair_v(260, 170, 240, "C112+C114", "2×120 µ/400 V", side="l"); gnd(260, 240)
    wire((330, 474), (330, 620)); dot(330, 620)
    res_v(330, 620, 720, "R108", "22 k 3 W", side="l", body=40); gnd(330, 720)
    # sprzęganie do drivera
    cap_h(330, 470, 260, "C103", "47 n", above=True)
    dot(470, 260); res_v(470, 260, 350, "R111", "470 k", side="r", body=36); gnd(470, 350)
    res_h(470, 546, 260, "R113", "1 k", above=True, body=30)
    cap_h(330, 470, 620, "C104", "47 n", above=True)
    dot(470, 620); res_v(470, 620, 710, "R112", "470 k", side="r", body=36); gnd(470, 710)
    res_h(470, 546, 620, "R114", "1 k", above=True, body=30)
    # driver V2
    triode(580, 260); txt(628, 300, "V2A", "tref"); txt(628, 315, "½ 6SN7", "ttyp")
    triode(580, 620, inv=True); txt(628, 578, "V2B", "tref"); txt(628, 593, "½ 6SN7", "ttyp")
    op(628, 350, ["driver, bez balansu AC", "Ia ≈ 5 mA na triodę", "Ua ≈ 144 V", "Uk ≈ 3,9 V"])
    wire((580, 226), (580, 170)); dot(580, 170)
    res_v(580, 70, 170, "R115", "47 k 3 W", side="l", body=40); flag(580, 70, "Uaa")
    wire((580, 654), (580, 710)); dot(580, 710)
    res_v(580, 710, 810, "R116", "47 k 3 W", side="l", body=40); flag(580, 810, "Uaa", d="down")
    wire((580, 294), (580, 586)); dot(580, 440)
    res_h(580, 660, 440, "R110", "390 Ω 3 W", above=False, body=40); wire((660, 440), (672, 440)); gnd(672, 440)
    # sprzęganie do KT88
    cap_h(580, 700, 170, "C105", "220 n", above=True)
    wire((700, 170), (700, 226), (750, 226)); dot(750, 226)
    cap_h(580, 700, 710, "C106", "220 n", above=False)
    wire((700, 710), (700, 614), (750, 614)); dot(750, 614)
    res_h(750, 840, 226, "R121", "1 k", above=False, body=36)
    res_h(750, 840, 614, "R122", "1 k", above=True, body=36)
    res_v(750, 110, 226, "R117", "100 k", side="r", body=40)
    res_v(750, 614, 730, "R118", "100 k", side="r", body=40)
    # bias V5 (góra): Bias-L -> P101 (suwak) -> R139 -> GND; R119 470k Bias->suwak
    wire((750, 110), (750, 30), (1150, 30), (1150, 110), (1200, 110)); dot(1200, 110)
    flag(1270, 50, "Bias-L")
    wire((1270, 50), (1200, 50)); dot(1270, 50)
    res_v(1200, 50, 110, "R119", "470 k", side="l", body=30)
    pot_v(1270, 50, 170, 110, 1200, "P101", "47 k", side="rr", body=50)
    res_v(1270, 170, 230, "R139", "47 k", side="rr", body=30); gnd(1270, 230)
    txt(1270, 270, "C107 100 n: Bias-L → GND", "net", "middle")
    # bias V6 (dół)
    wire((750, 730), (750, 830), (1150, 830), (1150, 670), (1200, 670)); dot(1200, 670)
    flag(1270, 610, "Bias-L")
    wire((1270, 610), (1200, 610)); dot(1270, 610)
    res_v(1200, 610, 670, "R120", "470 k", side="l", body=30)
    pot_v(1270, 610, 730, 670, 1200, "P102", "47 k", side="rr", body=50)
    res_v(1270, 730, 790, "R140", "47 k", side="rr", body=30); gnd(1270, 790)
    txt(1290, 826, "C108 100 n: Bias-L → GND", "net", "middle")
    # KT88
    tetrode(880, 220); tetrode(880, 620, inv=True)
    txt(898, 147, "V5A", "tref"); txt(936, 147, "KT88", "ttyp")
    txt(898, 702, "V6A", "tref"); txt(936, 702, "KT88", "ttyp")
    wire((880, 180), (880, 120), (1040, 120))
    wire((880, 660), (880, 720), (1040, 720))
    res_h(920, 1000, 212, "R125", "100 Ω 1 W", above=True, body=40)
    wire((1000, 212), (1010, 212), (1010, 291), (1040, 291))
    res_h(920, 1000, 628, "R126", "100 Ω 1 W", above=False, body=40)
    wire((1000, 628), (1010, 628), (1010, 549), (1040, 549))
    res_v(880, 260, 410, "R123", "10 Ω 3 W", side="l")
    res_v(880, 430, 580, "R124", "10 Ω 3 W", side="l")
    wire((880, 410), (880, 430)); dot(880, 420)
    wire((880, 420), (845, 420)); gnd(845, 420)
    dot(880, 272); txt(888, 284, "TP", "net")
    dot(880, 568); txt(888, 562, "TP", "net")
    op(896, 316, ["Ua ≈ 465 V", "Ik 50–55 mA", "(0,50–0,55 V na 10 Ω)", "Ug1 ≈ −45…−55 V"])
    # transformator wyjściowy, J101: 1 anoda A, 2 UL A, 3 CT, 4 UL B, 5 anoda B
    coil_v(1040, [120, 291, 420, 549, 720], bulge=1, cls="coil chgc")
    add('<line class="core" x1="1062" y1="110" x2="1062" y2="730"/>')
    add('<line class="core" x1="1072" y1="110" x2="1072" y2="730"/>')
    coil_v(1094, [300, 370, 540], bulge=-1, cls="coil chgc")
    wire((1040, 420), (960, 420)); dot(1040, 420); dot(990, 420)
    flag(960, 420, "Ua", stub=26)
    cap_v(990, 420, 490, "C118", "100 n", side="l"); gnd(990, 490)
    txt(1032, 412, "CT", "net", "end")
    txt(1032, 110, "J101-1", "net", "end"); txt(1032, 286, "J101-2", "net", "end")
    txt(1032, 545, "J101-4", "net", "end"); txt(1032, 712, "J101-5", "net", "end")
    # wtórne
    wire((1094, 300), (1240, 300)); wire((1094, 370), (1240, 370)); wire((1094, 540), (1240, 540))
    term(1245, 300); term(1245, 370); term(1245, 540)
    txt(1258, 290, "8 Ω", "ref"); txt(1258, 360, "4 Ω", "ref"); txt(1258, 530, "COM", "ref")
    wire((1250, 300), (1340, 300)); dot(1340, 300)
    txt(1258, 396, "kolumny 4 Ω", "net")
    res_v(1200, 370, 540, "RL (dodatek)", "100 Ω 2 W", side="r", chg=True, body=40)
    dot(1200, 370); dot(1200, 540)
    wire((1160, 540), (1160, 556)); dot(1160, 540); gnd(1160, 556, stub=4)
    txt(990, 770, "TR-OUT  TTG-KT88PP (u Onyxa: Hammond 1650HA)", "ref chg", "middle")
    txt(990, 785, "Raa 4 kΩ · UL 43% · 80 W · 4/8 Ω", "val chg", "middle")
    return "\n".join(S)

# ===================== ZASILACZ (wg VA1523; na płytce osobno dla każdego kanału) =====================
def bridge(x, y, ref, val, neg_top=False):
    add('<rect class="part" x="%g" y="%g" width="90" height="110"/>' % (x, y))
    txt(x + 45, y + 42, ref, "ref", "middle"); txt(x + 45, y + 57, val, "val", "middle"); txt(x + 45, y + 72, "mostek", "val", "middle")
    txt(x + 10, y + 19, "~", "val"); txt(x + 10, y + 99, "~", "val"); txt(x + 80, y + 24, "−" if neg_top else "+", "val", "end"); txt(x + 80, y + 99, "+" if neg_top else "−", "val", "end")

def psu():
    S.clear()
    # sieć (poza płytką)
    term(30, 120); txt(30, 104, "L", "ref", "middle")
    term(30, 300); txt(30, 326, "N", "ref", "middle")
    wire((35, 120), (70, 120))
    res_h(70, 150, 120, "F1", "T 2 A", above=True, body=40)
    wire((150, 120), (170, 120)); add('<circle class="dot" cx="170" cy="120" r="2.6"/>')
    add('<line class="w" x1="170" y1="120" x2="198" y2="106"/>')
    add('<circle class="dot" cx="200" cy="120" r="2.6"/>')
    txt(185, 94, "S1", "ref", "middle")
    wire((200, 120), (220, 120))
    res_h(220, 310, 120, "NTC", "soft-start", above=True, body=40)
    wire((310, 120), (350, 120))
    wire((35, 300), (350, 300))
    coil_v(350, [120, 300], bulge=1)
    add('<line class="core" x1="374" y1="70" x2="374" y2="640"/>')
    add('<line class="core" x1="384" y1="70" x2="384" y2="640"/>')
    txt(379, 672, "TR1  toroid 400 VA (poza płytką)", "ref chg", "middle")
    txt(379, 687, "360 V (+345 V)/0,65 A · 65 V/50 mA · 6,3 V/8 A · 6,3 V/3 A", "val chg", "middle")
    # anodowe -> J103 (i J203 dla prawego kanału)
    coil_v(408, [80, 190], bulge=-1); txt(420, 140, "360 V", "op")
    wire((408, 80), (470, 80), (470, 95), (480, 95))
    wire((408, 190), (470, 190), (470, 175), (480, 175))
    txt(445, 72, "J103", "ref", "middle")
    bridge(480, 80, "D101–D104", "UF5408")
    wire((570, 175), (590, 175)); gnd(590, 175)
    wire((570, 100), (600, 100))
    res_h(600, 680, 100, "R134", "10 Ω 3 W", above=False, body=36)
    wire((680, 100), (700, 100)); dot(700, 100)
    cap_v(700, 100, 190, "C119+C120", "2×120 µ/400 V", side="r", polar=True); gnd(700, 190)
    wire((700, 100), (790, 100))
    coil_h(790, 890, 100, "L106 (prawy: L206)", "10 H / 400 mA, zewnętrzny")
    wire((890, 100), (920, 100)); dot(920, 100)
    cap_v(920, 100, 190, "C121+C122", "2×120 µ/400 V", side="r", polar=True); gnd(920, 190)
    wire((920, 100), (1060, 100)); dot(1040, 100)
    flag(1040, 100, "Ua ≈ 465 V → CT", stub=22)
    res_h(1060, 1150, 100, "R128", "4k7 3 W*", above=False, body=40, chg=True)
    wire((1150, 100), (1190, 100)); dot(1190, 100)
    cap_v(1190, 100, 190, "C116+C117", "2×120 µ/400 V", side="r", polar=True); gnd(1190, 190)
    flag(1190, 100, "Uaa ≈ 381 V", stub=22)
    txt(1190, 232, "* dobrać, jeśli Ua inne niż ok. 465 V", "net", "middle")
    # podniesienie żarzenia
    dot(1040, 100); wire((1040, 100), (1040, 250)); dot(1040, 250)
    res_v(1040, 250, 330, "R136", "100 k", side="l", body=36)
    dot(1040, 330); res_v(1040, 330, 400, "R137", "10 k", side="l", body=30); gnd(1040, 400)
    wire((1040, 330), (1120, 330)); dot(1120, 330)
    cap_v(1120, 330, 400, "C124", "1 µ/200 V", side="r"); gnd(1120, 400)
    flag(1120, 330, "UaFF ≈ 42 V", d="right", stub=60)
    wire((1040, 250), (1040, 250))
    # bias -> J106
    coil_v(408, [250, 330], bulge=-1); txt(420, 296, "65 V", "op")
    wire((408, 250), (470, 250), (470, 255), (480, 255))
    wire((408, 330), (470, 330), (470, 335), (480, 335))
    txt(445, 242, "J106", "ref", "middle")
    bridge(480, 240, "D105–D108", "UF5408", neg_top=True)
    wire((570, 335), (600, 335))
    res_h(600, 680, 335, "R141", "10 Ω", above=False, body=30)
    wire((680, 335), (700, 335)); dot(700, 335)
    res_h(700, 780, 335, "R142", "100 Ω", above=False, body=30)
    wire((780, 335), (800, 335)); dot(800, 335); gnd(800, 335)
    wire((570, 260), (800, 260)); dot(700, 260); dot(800, 260)
    cap_v(700, 260, 335, "C125", "100 µ/200 V", side="l")
    cap_v(800, 260, 335, "C126", "100 µ/200 V", side="r")
    wire((800, 260), (860, 260))
    flag(860, 260, "Bias ≈ −90 V → P101/P102", d="right", stub=20)
    # żarzenie lamp sterujących -> J104
    coil_v(408, [420, 490], bulge=-1); txt(420, 460, "6,3 V", "op")
    wire((408, 420), (640, 420)); wire((408, 490), (640, 490))
    txt(445, 412, "J104", "ref", "middle")
    res_v(560, 420, 455, "", "", body=20); res_v(560, 455, 490, "", "", body=20)
    txt(572, 446, "R130, R131 330 Ω", "val")
    dot(560, 420); dot(560, 490); dot(560, 455)
    wire((560, 455), (520, 455)); txt(516, 459, "UaFF", "rail", "end")
    txt(700, 450, "→ 2× 6SN7 (1,2 A na kanał)", "net")
    # żarzenie KT88 -> J105
    coil_v(408, [540, 610], bulge=-1); txt(420, 580, "6,3 V", "op")
    wire((408, 540), (640, 540)); wire((408, 610), (640, 610))
    txt(445, 532, "J105", "ref", "middle")
    res_v(560, 540, 575, "", "", body=20); res_v(560, 575, 610, "", "", body=20)
    txt(572, 566, "R132, R133 330 Ω", "val")
    dot(560, 540); dot(560, 610); dot(560, 575)
    wire((560, 575), (520, 575)); txt(516, 579, "UaFF-L2*", "rail", "end")
    txt(700, 570, "→ 2× KT88 (3,2 A na kanał)", "net")
    txt(700, 586, "* sieć UaFF-L2 sprawdzić na płytce", "net")
    txt(1060, 600, "Prawy kanał: to samo z oznaczeniami 2xx", "net", "middle")
    txt(1060, 616, "(J203, J206, J204, J205, L206).", "net", "middle")
    txt(1060, 632, "Zworki B103/B104: wspólne uzwojenie anodowe dla obu kanałów.", "net", "middle")
    txt(1060, 648, "Każdy kanał ma własny mostek, filtr i dławik.", "net", "middle")
    return "\n".join(S)

# ===================== PLYTKA ZASILACZA (wlasna, uproszczona) =====================
def sw_h(x1, x2, y, ref, val, above=True):
    m1, m2 = x1 + 12, x2 - 12
    wire((x1, y), (m1, y)); wire((m2, y), (x2, y))
    add('<circle class="dot" cx="%g" cy="%g" r="2.6"/>' % (m1, y))
    add('<circle class="dot" cx="%g" cy="%g" r="2.6"/>' % (m2, y))
    add('<line class="w" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (m1, y, m2 - 2, y - 14))
    if above:
        label2((x1 + x2) / 2, y - 34, ref, val, "middle")
    else:
        label2((x1 + x2) / 2, y + 22, ref, val, "middle")

def led_v(x, y1, y2, ref, val):
    m = (y1 + y2) / 2
    wire((x, y1), (x, m - 9)); wire((x, m + 9), (x, y2))
    add('<path class="flagm" d="M%g %g L%g %g L%g %g Z"/>' % (x - 9, m - 8, x + 9, m - 8, x, m + 7))
    add('<line class="plate" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x - 9, m + 8, x + 9, m + 8))
    add('<line class="w" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x + 12, m - 4, x + 20, m - 12))
    add('<line class="w" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x + 12, m + 2, x + 20, m - 6))
    label2(x + 26, m - 3, ref, val, "start")

def outs(x, y, a, b, note=None):
    term(x, y); term(x, y + 26)
    txt(x + 12, y + 4, a, "ref"); txt(x + 12, y + 30, b, "ref")
    if note:
        txt(x + 12, y + 50, note, "net")

def psu_w():
    S.clear()
    # --- siec ---
    term(30, 100); txt(30, 84, "L", "ref", "middle")
    term(30, 300); txt(30, 326, "N", "ref", "middle")
    wire((35, 100), (50, 100))
    res_h(50, 120, 100, "F1", "T2,5 A (gniazdo IEC)", above=False, body=36)
    wire((120, 100), (150, 100)); dot(140, 100)
    wire((140, 100), (140, 170), (160, 170))
    res_h(160, 240, 170, "F2", "T500 mA", above=False, body=36)
    wire((240, 170), (260, 170)); term(265, 170)
    wire((35, 300), (400, 300)); dot(250, 300)
    wire((250, 300), (250, 200), (260, 200)); term(265, 200)
    txt(277, 174, "J3 L", "ref"); txt(277, 204, "J3 N", "ref")
    txt(277, 224, "→ PS1 czuwanie", "net"); txt(277, 238, "IRM-15-12", "net")
    sw_h(150, 230, 100, "K1", "sieć", above=False)
    dot(240, 100); wire((230, 100), (260, 100))
    res_h(260, 350, 100, "R1  R_SS", "47 Ω 10 W", above=False, body=40)
    wire((350, 100), (400, 100)); dot(370, 100)
    wire((240, 100), (240, 50)); sw_h(240, 370, 50, "K2", "+1,5 s", above=True); wire((370, 50), (370, 100))
    coil_v(400, [100, 300], bulge=1)
    add('<line class="core" x1="424" y1="50" x2="424" y2="640"/>')
    add('<line class="core" x1="434" y1="50" x2="434" y2="640"/>')
    txt(429, 672, "TR1 toroid 400 VA, ekran do PE", "ref chg", "middle")
    txt(429, 687, "S1 360 V (345 / 375) · S4 58 V · S2 6,3 V/8 A · S3 6,3 V/3 A", "val chg", "middle")
    # --- S1 anodowe ---
    coil_v(458, [70, 200], bulge=-1)
    txt(470, 132, "S1 360 V / 0,65 A", "op"); txt(470, 146, "odczepy 345 / 375 V", "op")
    wire((458, 70), (470, 70))
    res_h(470, 550, 70, "F3", "T1 A 500 V", above=False, body=36)
    sw_h(550, 650, 70, "K3", "+45 s", above=False)
    wire((650, 70), (670, 70)); dot(670, 70)
    res_h(670, 790, 70, "R2  R_IN", "100 Ω 10 W", above=False, body=44)
    wire((790, 70), (830, 70)); dot(810, 70)
    wire((670, 70), (670, 30)); sw_h(670, 810, 30, "", "", above=True); txt(740, 20, "K4  +1,5 s", "ref", "middle")
    wire((810, 30), (810, 70))
    wire((830, 70), (900, 70)); dot(880, 70); wire((880, 70), (880, 96), (900, 96))
    term(905, 70); term(905, 96)
    txt(917, 74, "J103-1 (L)", "ref"); txt(917, 100, "J203-1 (P)", "ref")
    wire((458, 200), (880, 200)); dot(860, 200); wire((860, 200), (860, 226), (900, 226)); wire((880, 200), (900, 200))
    term(905, 200); term(905, 226)
    txt(917, 204, "J103-2", "ref"); txt(917, 230, "J203-2", "ref")
    txt(620, 132, "→ mostki, filtry i dławiki 10 H", "net"); txt(620, 146, "   na płytce Onyxa: Ua ≈ 465 V", "net")
    # --- S4 bias ---
    coil_v(458, [250, 320], bulge=-1); txt(470, 290, "S4 58 V", "op")
    wire((458, 250), (560, 250))
    res_h(560, 640, 250, "F4", "T100 mA", above=True, body=36)
    wire((640, 250), (880, 250)); dot(880, 250); wire((880, 250), (880, 276), (900, 276)); wire((880, 250), (900, 250))
    wire((458, 320), (880, 320)); dot(860, 320); wire((860, 320), (860, 346), (900, 346)); wire((880, 320), (900, 320))
    term(905, 250); term(905, 276); term(905, 320); term(905, 346)
    txt(917, 254, "J106-1", "ref"); txt(917, 280, "J206-1", "ref"); txt(917, 324, "J106-2", "ref"); txt(917, 350, "J206-2", "ref")
    txt(580, 290, "→ mostki biasu Onyxa: ok. −80 V", "net")
    # --- S2 zarzenie KT88 ---
    coil_v(458, [400, 460], bulge=-1); txt(470, 436, "S2 6,3 V / 8 A", "op")
    wire((458, 400), (880, 400)); wire((458, 460), (880, 460))
    dot(860, 400); dot(840, 460)
    wire((860, 400), (860, 426), (900, 426)); wire((840, 460), (840, 486), (900, 486)); wire((880, 400), (900, 400)); wire((880, 460), (900, 460))
    term(905, 400); term(905, 426); term(905, 460); term(905, 486)
    txt(917, 404, "J105-1", "ref"); txt(917, 430, "J205-1", "ref"); txt(917, 464, "J105-2", "ref"); txt(917, 490, "J205-2", "ref")
    txt(730, 446, "→ 4× KT88, 6,4 A", "net")
    dot(640, 400); dot(640, 460)
    res_v(640, 400, 430, "", "", chg=True, body=18); res_v(640, 430, 460, "", "", chg=True, body=18)
    wire((640, 430), (700, 430)); gnd(700, 430, stub=6)
    txt(660, 420, "R11, R12 100 Ω 1 W", "val chg")
    txt(520, 510, "tylko gdy środek R132/R133 Onyxa pływa (UaFF-L2)", "net")
    # --- S3 zarzenie 6SN7 ---
    coil_v(458, [540, 600], bulge=-1); txt(470, 576, "S3 6,3 V / 3 A", "op")
    wire((458, 540), (880, 540)); wire((458, 600), (880, 600))
    dot(860, 540); dot(840, 600)
    wire((860, 540), (860, 566), (900, 566)); wire((840, 600), (840, 626), (900, 626)); wire((880, 540), (900, 540)); wire((880, 600), (900, 600))
    term(905, 540); term(905, 566); term(905, 600); term(905, 626)
    txt(917, 544, "J104-1", "ref"); txt(917, 570, "J204-1", "ref"); txt(917, 604, "J104-2", "ref"); txt(917, 630, "J204-2", "ref")
    txt(600, 576, "→ 4× 6SN7, 2,4 A", "net")
    # --- pomiar Ua i LED HV ---
    term(1040, 70); txt(1040, 50, "Ua-L z płytki Onyxa", "ref", "middle")
    wire((1045, 70), (1060, 70)); dot(1060, 70)
    res_h(1060, 1120, 70, "R3", "1 M", above=False, body=30)
    res_h(1120, 1180, 70, "R4", "1 M", above=False, body=30)
    res_h(1180, 1240, 70, "R5", "1 M", above=False, body=30)
    wire((1240, 70), (1260, 70)); dot(1260, 70)
    txt(1150, 124, "R3–R5 1600 V", "val", "middle")
    res_v(1260, 70, 150, "R6", "15 k", side="r", body=30); gnd(1260, 150)
    flag(1260, 70, "HV_SENSE → sterowanie J5-2", d="up", stub=14)
    txt(1275, 170, "≈ 2,3 V przy 465 V", "op")
    wire((1060, 70), (1060, 200))
    res_v(1060, 200, 260, "R7", "220 k 1 W", side="l", body=30)
    res_v(1060, 260, 320, "R8", "220 k 1 W", side="l", body=30)
    led_v(1060, 320, 370, "D1", "LED HV"); gnd(1060, 370)
    txt(1090, 214, "świeci, dopóki na płytce", "net"); txt(1090, 228, "Onyxa jest napięcie", "net")
    # --- cewki ---
    add('<rect class="part" x="1040" y="430" width="340" height="96"/>')
    txt(1210, 456, "Cewki K1–K4 (Omron G2RL-2-DC12)", "ref", "middle")
    txt(1210, 474, "+12 V, RLY1–RLY4 ← sterowanie J2", "val", "middle")
    txt(1210, 490, "diody 1N4148 równolegle do cewek", "val", "middle")
    txt(1210, 506, "K1/K2/K4 styki równol., K3 szeregowo", "val", "middle")
    term(1040, 600); txt(1052, 604, "GND – gwiazda (płytka Onyxa, sterowanie)", "ref")
    return "\n".join(S)

AMP = amp()
PSU = psu()

open("amp.svgpart", "w").write(AMP)
open("psu.svgpart", "w").write(PSU)
open("psuw.svgpart", "w").write(psu_w())
print(len(AMP), len(PSU))
