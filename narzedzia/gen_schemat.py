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

# ===================== AMPLIFIER (one channel) =====================
def amp():
    S.clear()
    # --- input ---
    term(30, 500); txt(30, 485, "WE", "ref", "middle")
    wire((35, 500), (90, 500))
    pot_v(90, 500, 620, 560, 120, "P1", "100 k log", side="l")
    gnd(90, 620)
    res_h(120, 176, 560, "R100", "1 k", above=True)
    # V1A
    triode(210, 560); txt(196, 610, "V1a", "tref chg", "end"); txt(196, 625, "½ 6SL7 (6N9S)", "ttyp chg", "end")
    op(250, 548, ["Ua ≈ 133 V", "Ia 1,0 mA", "Uk 1,0 V"])
    wire((210, 526), (210, 470)); dot(210, 470)
    res_v(210, 380, 470, "R102", "220 k 1 W", side="l", chg=True)
    dot(210, 380)
    res_v(210, 280, 380, "R105", "47 k 1 W", side="l", chg=True)
    flag(210, 280, "+400 V")
    wire((210, 380), (115, 380)); cap_v(115, 380, 450, "C102", "47 µ / 550 V*", side="l", polar=True, chg=True)
    gnd(115, 450)
    txt(222, 375, "≈ +353 V", "op")
    # V1A cathode / feedback
    wire((210, 594), (210, 640)); dot(210, 640)
    res_v(210, 640, 720, "R103", "1 k", side="l", chg=True)
    gnd(210, 720)
    wire((210, 640), (260, 640), (260, 840), (275, 840)); dot(275, 840)
    res_h(275, 405, 840, "R127", "22 k*  (dobrać)", above=True, chg=True)
    wire((275, 840), (275, 885)); cap_h(275, 405, 885, "C100", "180 p*  (dobrać)", above=False, chg=True)
    wire((405, 885), (405, 840)); dot(405, 840)
    wire((405, 840), (1320, 840), (1320, 370))
    txt(860, 832, "pętla NFB z odczepu 4 Ω (ok. 21 dB)", "net", "middle")
    # cathodyne V1B
    wire((210, 470), (300, 470), (300, 420), (336, 420))
    triode(370, 420); txt(330, 505, "V1b", "tref chg", "end"); txt(330, 520, "½ 6SL7 (6N9S)", "ttyp chg", "end")
    op(410, 352, ["katodyna", "Ua ≈ 266 V", "Uk ≈ 134 V", "Ia 1,2 mA"])
    wire((370, 386), (370, 250)); dot(370, 250)
    res_v(370, 150, 250, "R104", "110 k 1 W", side="l", chg=True)
    flag(370, 150, "+400 V")
    wire((370, 454), (370, 590)); dot(370, 590)
    res_v(370, 590, 690, "R106", "110 k 1 W", side="l", chg=True)
    gnd(370, 690)
    # coupling to driver
    cap_h(370, 520, 250, "C103", "470 n / 630 V", above=True, chg=True)
    dot(520, 250); wire((520, 250), (556, 250))
    res_v(520, 250, 340, "R107", "470 k", side="r", chg=True)
    gnd(520, 340)
    cap_h(370, 520, 590, "C104", "470 n / 630 V", above=True, chg=True)
    dot(520, 590); wire((520, 590), (556, 590))
    res_v(520, 590, 680, "R108", "470 k", side="r", chg=True)
    gnd(520, 680)
    # driver
    triode(590, 250); txt(640, 300, "V2a", "tref chg"); txt(640, 315, "½ 6SN7 (6N8S)", "ttyp chg")
    triode(590, 590, inv=True); txt(640, 548, "V2b", "tref chg"); txt(640, 563, "½ 6SN7 (6N8S)", "ttyp chg")
    op(640, 336, ["Ua ≈ 234 V", "Ia 8 mA"])
    wire((590, 216), (590, 170)); dot(590, 170)
    res_v(590, 60, 170, "R113", "22 k 3 W", side="l", chg=True)
    flag(590, 60, "+410 V")
    wire((590, 624), (590, 670)); dot(590, 670)
    res_v(590, 670, 780, "R114", "22 k 3 W", side="l", chg=True)
    flag(590, 780, "+410 V", d="down")
    wire((590, 284), (590, 370)); wire((590, 556), (590, 470))
    pot_v(590, 370, 470, 420, 630, "P100", "100 Ω  balans AC", side="l")
    res_h(630, 700, 420, "R112", "390 Ω 1 W", above=False, chg=True)
    wire((700, 420), (710, 420)); gnd(710, 420)
    txt(578, 450, "Uk ≈ 7,5 V", "op", "end")
    # coupling to output
    cap_h(590, 720, 170, "C105", "100 n / 630 V", above=True, chg=True)
    wire((720, 170), (720, 226), (750, 226)); dot(750, 226)
    cap_h(590, 720, 670, "C106", "100 n / 630 V", above=False, chg=True)
    wire((720, 670), (720, 614), (750, 614)); dot(750, 614)
    res_h(750, 840, 226, "R123", "1 k", above=False)
    res_h(750, 840, 614, "R124", "1 k", above=True)
    res_v(750, 110, 226, "R119", "220 k", side="r", chg=True)
    res_v(750, 614, 730, "R120", "220 k", side="r", chg=True)
    # --- bias V3 (gora) ---
    wire((750, 110), (750, 40), (1200, 40), (1200, 165), (1240, 165))
    dot(1220, 165)
    cap_v(1220, 165, 235, "C107", "10 µ / 100 V", side="l"); gnd(1220, 235)
    flag(1290, 75, "−90 V", chg=True)
    res_v(1290, 75, 125, "R130", "10 k", side="rr", chg=True, body=34)
    pot_v(1290, 125, 205, 165, 1240, "P201", "10 k cermet", side="rr", chg=True, body=40)
    res_v(1290, 205, 255, "R131", "15 k", side="rr", chg=True, body=34)
    gnd(1290, 255)
    txt(1245, 152, "BIAS V3", "ref chg", "middle")
    op(1210, 60, ["−39 … −64 V"], "end")
    # --- bias V4 (dol) ---
    wire((750, 730), (750, 800), (1200, 800), (1200, 695), (1240, 695))
    dot(1220, 695)
    cap_v(1220, 695, 765, "C108", "10 µ / 100 V", side="l"); gnd(1220, 765)
    flag(1290, 610, "−90 V", chg=True)
    res_v(1290, 610, 655, "R132", "10 k", side="rr", chg=True, body=34)
    pot_v(1290, 655, 735, 695, 1240, "P202", "10 k cermet", side="rr", chg=True, body=40)
    res_v(1290, 735, 780, "R133", "15 k", side="rr", chg=True, body=34)
    gnd(1290, 780)
    txt(1245, 682, "BIAS V4", "ref chg", "middle")
    op(1190, 815, ["−39 … −64 V"], "end")
    # output tubes
    tetrode(880, 220)
    tetrode(880, 620, inv=True)
    txt(898, 147, "V3", "tref chg"); txt(926, 147, "KT88", "ttyp chg")
    txt(898, 702, "V4", "tref chg"); txt(926, 702, "KT88", "ttyp chg")
    # anodes
    wire((880, 180), (880, 120), (1040, 120))
    wire((880, 660), (880, 720), (1040, 720))
    # screens via stoppers to UL taps
    res_h(920, 1000, 212, "R128", "220 Ω 1 W", above=True, chg=True, body=40)
    wire((1000, 212), (1010, 212), (1010, 291), (1040, 291))
    res_h(920, 1000, 628, "R129", "220 Ω 1 W", above=False, chg=True, body=40)
    wire((1000, 628), (1010, 628), (1010, 549), (1040, 549))
    # cathodes
    res_v(880, 260, 410, "R125", "10 Ω 1% 1 W", side="l", chg=True)
    res_v(880, 430, 580, "R126", "10 Ω 1% 1 W", side="l", chg=True)
    wire((880, 410), (880, 430)); dot(880, 420)
    wire((880, 420), (845, 420)); gnd(845, 420)
    dot(880, 272); txt(888, 284, "TP-A", "net")
    dot(880, 568); txt(888, 562, "TP-B", "net")
    op(896, 316, ["Ua ≈ 445 V", "Ik 50 mA", "(0,50 V na 10 Ω)", "Ug1 ≈ −45…−55 V"])
    # OPT
    coil_v(1040, [120, 291, 420, 549, 720], bulge=1, cls="coil chgc")
    add('<line class="core" x1="1062" y1="110" x2="1062" y2="730"/>')
    add('<line class="core" x1="1072" y1="110" x2="1072" y2="730"/>')
    coil_v(1094, [300, 370, 540], bulge=-1, cls="coil chgc")
    wire((1040, 420), (970, 420)); dot(1040, 420)
    flag(970, 420, "+450 V", stub=26, chg=True)
    txt(1032, 412, "CT", "net", "end")
    # secondary
    wire((1094, 300), (1240, 300)); wire((1094, 370), (1240, 370)); wire((1094, 540), (1240, 540))
    term(1245, 300); term(1245, 370); term(1245, 540)
    txt(1258, 286, "8 Ω", "ref"); txt(1258, 360, "4 Ω", "ref"); txt(1258, 530, "COM", "ref")
    wire((1250, 370), (1320, 370)); dot(1320, 370)
    txt(1258, 400, "← kolumny 4 Ω", "net")
    wire((1180, 540), (1180, 560)); dot(1180, 540); gnd(1180, 560, stub=4)
    txt(1067, 762, "TR-OUT  toroidy.pl TTG-KT88PP", "ref chg", "middle")
    txt(1067, 777, "Raa 4 kΩ · UL 43% · 80 W · 4/8 Ω", "val chg", "middle")
    return "\n".join(S)

# ===================== POWER SUPPLY =====================
def psu():
    S.clear()
    term(30, 120); txt(30, 104, "L", "ref", "middle")
    term(30, 300); txt(30, 326, "N", "ref", "middle")
    wire((35, 120), (70, 120))
    res_h(70, 150, 120, "F1", "T 2 A", above=True, body=40)
    # switch
    wire((150, 120), (170, 120)); add('<circle class="dot" cx="170" cy="120" r="2.6"/>')
    add('<line class="w" x1="170" y1="120" x2="198" y2="106"/>')
    add('<circle class="dot" cx="200" cy="120" r="2.6"/>')
    txt(185, 94, "S1", "ref", "middle")
    wire((200, 120), (220, 120))
    res_h(220, 310, 120, "NTC", "10 Ω / 5 A (soft-start)", above=True, body=40)
    wire((310, 120), (350, 120))
    wire((35, 300), (350, 300))
    coil_v(350, [120, 300], bulge=1)
    add('<line class="core" x1="374" y1="80" x2="374" y2="640"/>')
    add('<line class="core" x1="384" y1="80" x2="384" y2="640"/>')
    txt(379, 670, "TR1  sieciowy ≈ 300 VA", "ref", "middle")
    txt(379, 685, "350 V/0,5 A · 70 V/0,1 A · 6,3 V/7 A · 6,3 V/3 A", "val", "middle")
    # HV secondary
    coil_v(408, [80, 190], bulge=-1)
    txt(420, 140, "350 V", "op")
    wire((408, 80), (470, 80), (470, 95), (480, 95))
    wire((408, 190), (470, 190), (470, 175), (480, 175))
    add('<rect class="part" x="480" y="80" width="90" height="110"/>')
    txt(525, 122, "D1–D4", "ref", "middle"); txt(525, 137, "UF4007", "val", "middle"); txt(525, 152, "mostek", "val", "middle")
    txt(490, 99, "~", "val"); txt(490, 179, "~", "val"); txt(560, 104, "+", "val", "end"); txt(560, 179, "−", "val", "end")
    wire((570, 175), (590, 175)); gnd(590, 175)
    wire((570, 100), (620, 100)); dot(620, 100)
    cap_v(620, 100, 200, "C1", "100 µ / 550 V*", side="r", polar=True); gnd(620, 200)
    wire((620, 100), (650, 100))
    coil_h(650, 760, 100, "L1", "5 H / 400 mA")
    wire((760, 100), (790, 100)); dot(790, 100)
    cap_v(790, 100, 200, "C2", "220 µ / 550 V*", side="r", polar=True); gnd(790, 200)
    wire((790, 100), (990, 100)); dot(930, 100)
    res_v(930, 100, 200, "R301", "220 k 2 W", side="r"); gnd(930, 200)
    dot(960, 100); flag(960, 100, "+450 V → TR-OUT", stub=22)
    res_h(990, 1070, 100, "R201", "2k2 2 W", above=False)
    wire((1070, 100), (1110, 100)); dot(1110, 100)
    cap_v(1110, 100, 200, "C3", "47 µ / 550 V*", side="r", polar=True); gnd(1110, 200)
    flag(1110, 100, "+410 V driver", stub=22)
    wire((1110, 100), (1150, 100))
    res_h(1150, 1240, 100, "R202", "4k7 1 W", above=False)
    wire((1240, 100), (1270, 100)); dot(1270, 100)
    cap_v(1270, 100, 200, "C4", "47 µ / 550 V*", side="r", polar=True); gnd(1270, 200)
    flag(1270, 100, "+400 V wejście", stub=22)
    txt(1170, 250, "R201 … C4: osobny łańcuch dla każdego kanału", "net", "middle")
    # bias secondary
    coil_v(408, [250, 330], bulge=-1)
    txt(420, 296, "70 V", "op")
    wire((408, 330), (440, 330)); gnd(440, 330)
    wire((408, 250), (470, 250))
    diode_h(470, 560, 250, "D5", "1N4007")
    wire((560, 250), (600, 250)); dot(600, 250)
    cap_v(600, 250, 330, "C5", "100 µ / 160 V", side="r", polar=False); gnd(600, 330)
    res_h(600, 700, 250, "R203", "1 k", above=True)
    wire((700, 250), (720, 250)); dot(720, 250)
    cap_v(720, 250, 330, "C6", "100 µ / 160 V", side="r"); gnd(720, 330)
    txt(760, 242, "−90 V", "op")
    wire((720, 250), (830, 250))
    flag(830, 250, "−90 V → R130/R132 (regulacja biasu przy lampach)", d="right", stub=20, chg=True)
    txt(873, 272, "4 dzielniki: P201, P202 w każdym kanale", "net")
    # heater 1: KT88
    coil_v(408, [400, 470], bulge=-1)
    txt(420, 440, "6,3 V", "op")
    wire((408, 400), (650, 400)); wire((408, 470), (650, 470))
    res_v(540, 400, 435, "", "", body=20); res_v(540, 435, 470, "", "", body=20)
    txt(552, 425, "2× 100 Ω", "val")
    dot(540, 400); dot(540, 470); dot(540, 435)
    wire((540, 435), (510, 435)); gnd(510, 435, stub=6)
    txt(660, 430, "→ żarzenie 4× KT88", "net"); txt(660, 445, "6,4 A, AC", "net")
    # heater 2: small tubes, elevated
    coil_v(408, [540, 610], bulge=-1)
    txt(420, 580, "6,3 V", "op")
    wire((408, 540), (640, 540)); wire((408, 610), (640, 610))
    res_v(540, 540, 575, "", "", body=20); res_v(540, 575, 610, "", "", body=20)
    txt(552, 566, "2× 100 Ω", "val")
    dot(540, 540); dot(540, 610); dot(540, 575)
    txt(432, 530, "→ żarzenie 6SL7, 6SN7 · 1,8 A", "net")
    wire((540, 575), (760, 575)); dot(760, 575)
    res_v(760, 495, 575, "R206", "470 k", side="r", body=36)
    flag(760, 495, "+450 V", stub=10)
    res_v(760, 575, 645, "R207", "82 k", side="l", body=30); gnd(760, 645, stub=6)
    wire((760, 575), (860, 575)); dot(860, 575)
    cap_v(860, 575, 640, "C8", "47 µ / 100 V", side="r", polar=True); gnd(860, 640, stub=6)
    txt(870, 560, "≈ +67 V podniesienie żarzenia", "op")
    return "\n".join(S)

AMP = amp()
PSU = psu()

open("amp.svgpart", "w").write(AMP)
open("psu.svgpart", "w").write(PSU)
print(len(AMP), len(PSU))
