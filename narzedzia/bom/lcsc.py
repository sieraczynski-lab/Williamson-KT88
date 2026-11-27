#!/usr/bin/env python3
"""Zamowienie LCSC (wszystko montowane recznie, bez montazu w JLCPCB).

Zrodlo: bom/lcsc_plytki_williamson.csv (pelna lista z parametrami, ilosciami i zapasem).
Wyniki:
  bom/lcsc_zamowienie.csv            - do wgrania w LCSC BOM Tool (lcsc.com/bom): wszystkie plytki + Onyx + front/tyl,
                                       pozycje 'konieczne' i 'zalecane', zsumowane po numerze LCSC (ilosc z zapasem)
  bom/lcsc_zamowienie.xlsx           - to samo + arkusze 'Opcjonalne i do decyzji' oraz 'Poza LCSC'
  pcb/<plytka>/<nazwa>_BOM_LCSC.csv  - osobno dla kazdej plytki (ten sam format)
  pcb/<plytka>/<nazwa>_BOM_LCSC.xlsx
Sprawdza tez zgodnosc ilosci z BOM-ami plytek (pcb/*/*_BOM.csv).
Uruchom: python3 narzedzia/bom/lcsc.py
"""
import csv, collections, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MASTER = os.path.join(ROOT, "bom", "lcsc_plytki_williamson.csv")
INFO = json.load(open(os.path.join(os.path.dirname(__file__), "lcsc_info.json"), encoding="utf-8"))
BOARDS = {  # sekcja -> (katalog, nazwa plikow, BOM plytki)
    "B": ("zasilacz", "zasilacz_williamson"),
    "C": ("ul", "ul_trioda_williamson"),
    "D": ("glosniki", "glosniki_williamson"),
    "E": ("sterowanie", "sterowanie"),
    "F": ("selektor", "selektor"),
}
STRIPS = {"C74252", "C2337"}           # listwy 1x40 ciete na kawalki: w BOM plytki liczone per zlacze
ORDER = ("konieczne", "zalecane")      # do koszyka; reszta osobno
HDR = ["Quantity", "LCSC Part Number", "Manufacturer Part Number", "Description", "Customer Remarks"]


def load_master():
    rows = list(csv.DictReader(open(MASTER, encoding="utf-8-sig"), delimiter=";"))
    for r in rows:
        r["sek"] = r["Sekcja"][:1]
        for k in ("Ilość", "Zapas", "Razem"):
            r[k] = int(r[k] or 0)
    return rows


def mpn(r):
    l = r["LCSC"]
    if l in INFO and INFO[l]["mpn"]:
        return INFO[l]["mpn"]
    return r["Propozycja (producent / MPN)"]


def desc(r):
    par = r["Wymagane parametry"].replace("\n", " ").strip()
    return r["Element"] if not par or par == r["Element"] else "%s: %s" % (r["Element"], par)


def remark(r, with_section=True):
    s = r["Oznaczenia"]
    if with_section:
        sek = r["Sekcja"].split(" (")[0]
        if sek.startswith("G."):
            sek = "G. Front / tył / wnętrze"
        s = "%s - %s" % (sek, s)
    return s.strip()


def group(rows, with_section=True):
    """Sumuje pozycje po numerze LCSC."""
    g = collections.OrderedDict()
    for r in rows:
        k = r["LCSC"]
        if k not in g:
            g[k] = {"q": 0, "mpn": mpn(r), "desc": desc(r), "rem": []}
        g[k]["q"] += r["Razem"]
        g[k]["rem"].append(remark(r, with_section))
    return [[v["q"], k, v["mpn"], v["desc"], "; ".join(v["rem"])] for k, v in g.items()]


def write_csv(path, lines):
    with open(path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(HDR)
        w.writerows(lines)


def write_xlsx(path, title, lines, other, outside):
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment
    except ImportError:
        print("  (brak openpyxl - pomijam", os.path.basename(path), ")")
        return
    wb = openpyxl.Workbook()
    bold = Font(bold=True)
    head = PatternFill("solid", fgColor="DDE6F0")

    def sheet(ws, note, hdr, data, widths):
        ws.append([note])
        ws["A1"].font = bold
        ws.append(hdr)
        for c in ws[2]:
            c.font, c.fill = bold, head
        for d in data:
            ws.append(d)
        for i, wd in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = wd
        for row in ws.iter_rows(min_row=3):
            for c in row:
                c.alignment = Alignment(vertical="top", wrap_text=True)
        ws.freeze_panes = "A3"

    ws = wb.active
    ws.title = "Zamowienie LCSC"
    sheet(ws, title, HDR, lines, [10, 14, 28, 60, 60])
    if other:
        sheet(wb.create_sheet("Opcjonalne i do decyzji"),
              "Nie wchodza do koszyka. Dopisz recznie, jesli zdecydujesz.",
              ["Ilosc", "LCSC", "MPN", "Opis", "Gdzie", "Priorytet / uwagi"], other, [8, 14, 28, 60, 40, 50])
    if outside:
        sheet(wb.create_sheet("Poza LCSC"),
              "Tego nie ma w LCSC (albo kupujesz gdzie indziej): TME, Allegro, AliExpress, sklep lampowy.",
              ["Ilosc", "Element", "Wymagane parametry", "Propozycja", "Gdzie kupic", "Oznaczenia / uwagi"],
              outside, [8, 34, 50, 34, 22, 50])
    wb.save(path)


def split(rows):
    buy = [r for r in rows if r["LCSC"] and r["Razem"] > 0 and r["Priorytet"] in ORDER]
    other = [[r["Razem"] or r["Ilość"], r["LCSC"], mpn(r), desc(r), r["Gdzie kupić"], "%s. %s %s" % (r["Priorytet"], remark(r), r["Uwagi"])]
             for r in rows if r["LCSC"] and (r["Priorytet"] not in ORDER + ("masz",)) ]
    outside = [[r["Razem"], r["Element"], r["Wymagane parametry"], r["Propozycja (producent / MPN)"], r["Gdzie kupić"],
                "%s %s" % (remark(r), r["Uwagi"])]
               for r in rows if not r["LCSC"] and r["Razem"] > 0 and r["Priorytet"] in ORDER]
    return buy, other, outside


def check(rows):
    """Porownanie ilosci (bez zapasu) z BOM-ami plytek."""
    bad = 0
    for sek, (d, name) in BOARDS.items():
        path = os.path.join(ROOT, "pcb", d, name + "_BOM.csv")
        pcb = collections.Counter()
        for r in csv.DictReader(open(path, encoding="utf-8-sig"), delimiter=";"):
            if r.get("LCSC") and "NIE MONTOWA" not in r.get("Uwagi", "").upper():
                pcb[r["LCSC"]] += 1
        lst = collections.Counter()
        for r in rows:
            if r["sek"] == sek and r["LCSC"]:
                lst[r["LCSC"]] += r["Ilość"]
        for k in sorted(set(pcb) | set(lst)):
            if k in STRIPS and lst[k] > 0 and pcb[k] > 0:
                continue                       # listwa: 1 szt. na kilka zlaczy
            if pcb[k] != lst[k] and pcb[k] > 0:
                print("  UWAGA %s %s: na plytce %d, na liscie %d" % (d, k, pcb[k], lst[k]))
                bad += 1
    return bad


def main():
    rows = load_master()
    bad = check(rows)
    buy, other, outside = split(rows)
    lines = group(buy)
    write_csv(os.path.join(ROOT, "bom", "lcsc_zamowienie.csv"), lines)
    write_xlsx(os.path.join(ROOT, "bom", "lcsc_zamowienie.xlsx"),
               "Williamson KT88 - zamowienie LCSC (plytki, Onyx, front/tyl; montaz reczny). Ilosci z zapasem. "
               "LCSC BOM Tool sam podniesie ilosci do minimum / wielokrotnosci (kolumna Min/Mult).",
               lines, other, outside)
    print("bom/lcsc_zamowienie: %d pozycji, %d szt.; opcjonalne/do decyzji %d; poza LCSC %d" %
          (len(lines), sum(l[0] for l in lines), len(other), len(outside)))
    for sek, (d, name) in BOARDS.items():
        sub = [r for r in rows if r["sek"] == sek]
        b, o, out = split(sub)
        ln = group(b, with_section=False)
        write_csv(os.path.join(ROOT, "pcb", d, name + "_BOM_LCSC.csv"), ln)
        write_xlsx(os.path.join(ROOT, "pcb", d, name + "_BOM_LCSC.xlsx"),
                   "Williamson KT88 - plytka %s (1 szt.): czesci z LCSC, montaz reczny. Ilosci z zapasem." % d,
                   ln, o, out)
        print("  %-11s %2d pozycji LCSC, %d poza LCSC" % (d, len(ln), len(out)))
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
