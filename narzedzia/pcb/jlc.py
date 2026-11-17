"""Numery czesci LCSC/JLCPCB (sprawdzone 25.10.2026) i BOM w formacie JLCPCB."""
import csv, os
from pcbgen import FOOT

# (wartosc, footprint) -> (opis / MPN, LCSC)
PARTS = {
    ("ULN2803G-S18-R", "SOIC-18W_7.5x11.6mm_P1.27mm"): ("ULN2803G-S18-R (UTC)", "C33924"),
    ("ADS1115IDGSR 0x48", "MSOP-10_3x3mm_P0.5mm"): ("ADS1115IDGSR", "C37593"),
    ("ADS1115IDGSR 0x49", "MSOP-10_3x3mm_P0.5mm"): ("ADS1115IDGSR", "C37593"),
    ("MCP4728-E/UN", "MSOP-10_3x3mm_P0.5mm"): ("MCP4728-E/UN", "C108207"),
    ("LM324DR", "SOIC-14_3.9x8.7mm_P1.27mm"): ("LM324DR", "C7943"),
    ("10k", "R_0805_2012Metric"): ("10k 1% 0805", "C17414"),
    ("20k", "R_0805_2012Metric"): ("20k 1% 0805", "C4328"),
    ("4k7", "R_0805_2012Metric"): ("4,7k 1% 0805", "C17673"),
    ("1k 1206", "R_1206_3216Metric"): ("1k 1% 1206", "C4410"),
    ("330k 1206", "R_1206_3216Metric"): ("330k 1% 1206 (1206W4F3303T5E)", "C17929"),
    ("68k", "R_0805_2012Metric"): ("68k 1% 0805", "C17801"),
    ("33k", "R_0805_2012Metric"): ("33k 1% 0805", "C17633"),
    ("1k", "R_0805_2012Metric"): ("1k 1% 0805", "C17513"),
    ("1u", "C_0805_2012Metric"): ("1uF 50V X7R 0805", "C28323"),
    ("100n", "C_0805_2012Metric"): ("100nF 50V X7R 0805", "C49678"),
    ("1N4148W", "D_SOD-123"): ("1N4148W SOD-123", "C81598"),
    ("G2RL-2-DC12", "Relay_DPDT_Omron_G2RL"): ("Omron G2RL-2-DC12", "C61458"),
    # --- elementy przewlekane plytek Williamsona (sprawdzone 17.11.2026, baza yaqwsx/jlcparts) ---
    ("1N4148", "D_DO-35_P7.62"): ("1N4148 DO-35", "C402212"),
    ("BAT85", "D_DO-35_P7.62"): ("BAT42 DO-35 (zamiennik BAT85, 30 V; BAT85 brak w LCSC)", "C2798198"),
    ("47R 10W", "R_Cement_10W_P55.88"): ("EWWR0010J47R0T9 drutowy 10 W 47R, 9 x 36,5 mm (cementowego 10 W brak)", "C349125"),
    ("100R 10W", "R_Cement_10W_P55.88"): ("EWWR0010J100RT9 drutowy 10 W 100R, 9 x 36,5 mm", "C349082"),
    ("1M 1% 1600V", "R_Axial_1W_P15.24"): ("Vishay VR37 1M 1% (VR37000001004FR500)", "C1365660"),
    ("220k 1W", "R_Axial_1W_P15.24"): ("220k 1% 1 W 350 V (MFR01SF2203A10)", "C82511"),
    ("15k 1%", "R_Axial_0.5W_P12.7"): ("15k 1% 0,5 W 350 V (MF1/2W-15K)", "C601895"),
    ("100k 1%", "R_Axial_0.5W_P12.7"): ("100k 1% 0,25 W 50 ppm (MFR-25FTE52-100K)", "C172965"),
    ("5k1 1%", "R_Axial_0.5W_P12.7"): ("5,1k 1% 0,25 W 50 ppm (MFR-25FTE52-5K1)", "C173033"),
    ("1k", "R_Axial_0.5W_P12.7"): ("1k 1% 0,25 W (MFR-25FTE52-1K)", "C172978"),
    ("1n C0G", "C_Box_P5_7x4"): ("1 nF 50 V C0G raster 5 mm (K102J15C0GF5TH5)", "C2170624"),
    ("10u 16V", "CP_Radial_D6.3_P2.5"): ("10 uF 16 V 5 x 11, raster 2 mm (RL1C100MC110A00CV0)", "C216288"),
    ("LED HV czerwona", "LED_D3.0_P2.54"): ("LED 3 mm czerwona, jasna 600 mcd (dobrze swieci przy 1 mA)", "C779429"),
    ("T500mA 250V", "Fuseholder_5x20_Closed_P22.5"): ("oprawka 5x20 z pokrywka Littelfuse 64800001009, 250 V, raster 22,7", "C187509"),
    ("T100mA 250V", "Fuseholder_5x20_Closed_P22.5"): ("oprawka 5x20 z pokrywka Littelfuse 64800001009, 250 V, raster 22,7", "C187509"),
    ("T1A 500V", "Fuseholder_5x20_Closed_P22.5"): ("UWAGA: oprawki 5x20 >= 400 V do PCB brak w LCSC; ta ma 250 V (Littelfuse 648)", "C187509"),
}

# zlacza: po footprincie (wartosc to nazwa sygnalu)
FP_PARTS = {
    "TerminalBlock_1x02_P5.08": ("WJ500V-5.08-2P 250 V 18 A", "C8465"),
    "TerminalBlock_1x02_P7.62": ("DG636-7.62-02P 630 V 32 A", "C581337"),
    "TerminalBlock_1x03_P7.62": ("Phoenix 1731734 7,62 mm 3P 500 V", "C480591"),
    "PinHeader_1x02_P2.54": ("goldpin 1x2 prosty", "C492401"),
    "PinHeader_1x03_P2.54": ("goldpin 1x3 prosty", "C49257"),
    "PinHeader_1x04_P2.54_H": ("goldpin 1x4 katowy", "C492412"),
}


def lookup(c):
    n = FOOT[c.fp].name
    if n.endswith("_V"):
        n = n[:-2]
    return PARTS.get((c.value, n)) or FP_PARTS.get(n) or FP_PARTS.get(FOOT[c.fp].name, ("", ""))


def is_smd(c):
    f = FOOT[c.fp]
    return bool(f.pads) and all(p["drill"] == 0 for p in f.pads)


def write_bom(board, dirpath):
    """BOM do montazu SMD w JLCPCB (tylko elementy SMD). Zwraca liczbe pozycji."""
    groups = {}
    for c in board.comps:
        if not is_smd(c):
            continue
        desc, lcsc = lookup(c)
        fp = FOOT[c.fp].name
        key = (desc or c.value, fp[:-2] if fp.endswith("_V") else fp, lcsc)
        groups.setdefault(key, []).append(c.ref)
    if not groups:
        return 0
    p = os.path.join(dirpath, board.name + "_BOM_JLCPCB.csv")
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
        for (desc, fp, lcsc), refs in sorted(groups.items(), key=lambda kv: kv[1][0]):
            refs.sort(key=lambda r: (r.rstrip("0123456789"), int(r[len(r.rstrip("0123456789")):] or 0)))
            w.writerow([desc, ",".join(refs), fp, lcsc])
    return len(groups)
