import sys, os
sys.path.insert(0, "/home/claude/williamson-kt88/narzedzia/obudowa"); os.chdir("/home/claude/williamson-kt88/narzedzia/obudowa")
import model
from zrender import render
skip = ("REF_galka", "REF_przycisk", "REF_LED", "REF_wyswietl")
allp = [p for p in model.parts + model.ref if not p.name.startswith(skip)]
render(allp, sys.argv[1], azim=-62, elev=12, title=sys.argv[2])
