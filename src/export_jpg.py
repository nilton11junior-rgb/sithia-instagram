#!/usr/bin/env python3
"""Cria slide-NN.jpg ao lado de cada slide-NN.png (a API do Instagram aceita só JPEG).
Uso: python3 src/export_jpg.py            # todos os posts em criativos/gerados/
     python3 src/export_jpg.py <pasta>   # uma pasta"""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

def main(base):
    n = 0
    for png in sorted(Path(base).rglob("slide-*.png")):
        jpg = png.with_suffix(".jpg")
        Image.open(png).convert("RGB").save(jpg, "JPEG", quality=92, optimize=True)
        n += 1
    print(f"{n} slide(s) convertido(s) para JPEG")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT / "criativos" / "gerados")
