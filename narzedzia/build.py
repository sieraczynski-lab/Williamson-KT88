"""Generuje schematy (SVG) i stronę HTML z opisem.

Użycie (z katalogu głównego repozytorium):
    python3 narzedzia/build.py
"""
import os, runpy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.join(ROOT, "narzedzia"))
runpy.run_path("gen_schemat.py")  # tworzy amp.svgpart i psu.svgpart

amp = open("amp.svgpart").read()
psu = open("psu.svgpart").read()

STYLE = """<style>
.w{fill:none;stroke:#22343a;stroke-width:1.6;stroke-linejoin:round;stroke-linecap:round}
.part{fill:#f8faf6;stroke:#22343a;stroke-width:1.6}
.chgp{stroke:#b4560f;fill:#f6e5d6}
.plate{stroke:#22343a;stroke-width:2.4;fill:none}
.plate.chgp{stroke:#b4560f}
.dot{fill:#22343a}
.tube{fill:none;stroke:#22343a;stroke-width:1.6}
.el{fill:none;stroke:#22343a;stroke-width:2}
.grid{stroke-dasharray:3 3;stroke-width:1.6}
.coil{fill:none;stroke:#22343a;stroke-width:1.8}
.chgc{stroke:#b4560f}
.core{stroke:#22343a;stroke-width:2.4}
.flagm{fill:#22343a}
.term{fill:#f8faf6;stroke:#22343a;stroke-width:1.6}
text{font-family:"JetBrains Mono",Consolas,monospace;fill:#1c282b}
.ref{font-size:12px;font-weight:600}
.val{font-size:11.5px;fill:#56656a}
.ref.chg,.val.chg,.rail.chg,.tref.chg,.ttyp.chg{fill:#b4560f}
.tref{font-family:"Arial Narrow",sans-serif;font-size:16px;font-weight:700}
.ttyp{font-size:11.5px;fill:#56656a}
.rail{font-size:12px;font-weight:600}
.op{font-size:11px;fill:#1f6b6f}
.net{font-size:11px;fill:#56656a;font-style:italic}
.pol{font-size:13px;fill:#22343a}
</style>"""

def svg(body, w, h):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">\n'
            '%s\n<rect width="100%%" height="100%%" fill="#f8faf6"/>\n%s\n</svg>\n') % (w, h, w, h, STYLE, body)

open(os.path.join(ROOT, "schematy", "kanal.svg"), "w").write(svg(amp, 1400, 960))
open(os.path.join(ROOT, "schematy", "zasilacz.svg"), "w").write(svg(psu, 1400, 700))

page = ('<!doctype html>\n<html lang="pl">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        + open("szablon_strony.html").read().replace("%%AMP%%", amp).replace("%%PSU%%", psu))
open(os.path.join(ROOT, "schematy", "williamson-kt88.html"), "w").write(page)

for f in ("amp.svgpart", "psu.svgpart"):
    os.remove(f)
print("OK: schematy/kanal.svg, schematy/zasilacz.svg, schematy/williamson-kt88.html")
