#!/usr/bin/env python3
"""Treat the Drive manifesto photos for use as shirt graphics.
Originals stay (warm/Citrina context); we add sapphire & ink duotones."""
from PIL import Image, ImageOps
import os

PH = os.path.join(os.path.dirname(__file__), "assets", "photos")

def duo(src, dst, dark, light, contrast=1.0):
    im = Image.open(os.path.join(PH, src)).convert("L")
    if contrast != 1.0:
        im = ImageOps.autocontrast(im, cutoff=1)
    out = ImageOps.colorize(im, black=dark, white=light)
    out.convert("RGB").save(os.path.join(PH, dst), quality=90)
    print("wrote", dst, out.size)

SAPPHIRE = (0x1d, 0x1b, 0x40)     # deep sapphire
CREAM    = (0xf1, 0xec, 0xe0)
INK      = (0x14, 0x12, 0x10)
AMBER    = (0xe9, 0xad, 0x51)

# sapphire duotones (website-palette context)
duo("manif_3.jpg", "manif_3_zafiro.jpg", SAPPHIRE, CREAM, contrast=1.1)
duo("manif_4.jpg", "manif_4_zafiro.jpg", SAPPHIRE, CREAM, contrast=1.1)
duo("manif_2.jpg", "manif_2_zafiro.jpg", SAPPHIRE, CREAM, contrast=1.1)
# amber-on-ink duotone (citrina / for black tees later)
duo("manif_3.jpg", "manif_3_citrina.jpg", INK, AMBER, contrast=1.1)
print("done")
