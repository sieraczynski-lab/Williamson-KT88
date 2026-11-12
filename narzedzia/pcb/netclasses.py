# Klasy sieci (net classes) plytki zasilacza Williamson - zapisywane w .kicad_pcb, EasyEDA importuje je razem z PCB.
# (klasa, szerokosc mm, odstep mm, odstep specjalny, sieci, uwagi) - miedz 1 oz
import csv, os

CLASSES = {
    "zasilacz_williamson": [
        ("SIEC_230", 2.0, 3.0, "6,0 do CEWKI", "L_SW L_K1 L_TR N_SW L_TR2", "230 V, ok. 1,8 A + udar; izolacja wzmocniona do 12 V"),
        ("HT_AC", 1.5, 3.0, "6,0 do CEWKI", "HT_TR HT_F K3_MID HT_K3 HT_IN HT_B", "S1 360 V AC (510 V szczyt), ok. 0,65 A + impulsy ladowania"),
        ("HV_DC", 0.6, 3.0, "", "UA", "Ua 465 V z plytki Onyxa, ok. 1 mA"),
        ("HV_MID", 0.6, 2.0, "", "HVS1 HVS2 LED_M", "155-310 V, dzielnik pomiarowy i LED"),
        ("BIAS_AC", 0.6, 1.0, "", "B_AC1 B_AC2 B_F", "S4 58 V AC, ok. 30 mA"),
        ("POMIAR", 0.4, 0.5, "3,0 do HV_DC/HT_AC", "HV_SENSE LED_A", "HV_SENSE ok. 2,3 V do ADS1115"),
        ("CEWKI", 0.5, 0.3, "6,0 do SIEC_230/HT_AC", "+12V RLY1 RLY2 RLY3 RLY4", "ok. 35 mA na cewke"),
        ("GND", 1.0, 0.3, "", "GND", ""),
    ],
}
DEFAULT = (0.4, 0.3)


def check(board):
    nets = set(board.nets())
    for cl in CLASSES[board.name]:
        for n in cl[4].split():
            assert n in nets, (board.name, cl[0], n)


def write_csv(board, dirpath):
    check(board)
    p = os.path.join(dirpath, board.name + "_klasy_sieci.csv")
    with open(p, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["Klasa", "Szerokosc sciezki [mm]", "Odstep [mm]", "Odstep specjalny", "Sieci", "Uwagi"])
        for k, tw, cl, sp, nets, note in CLASSES[board.name]:
            w.writerow([k, tw, cl, sp, nets, note])
    return p
