#!/usr/bin/env python3
"""
tratar.py — tratamiento de las fotografías de la galería de cfdl.site.

Lee los másteres de `studio/gallery/originales/` (las copias de `Seleccion/`
en Drive, ya con su balance de blancos) y escribe, para cada uno:

    docs/gallery/<nombre>.jpg          1600 px de lado mayor   (visor)
    docs/gallery/sm/<nombre>.jpg       900 px                  (retícula)
    docs/gallery/sm/<nombre>.webp      900 px

Nunca se trabaja sobre lo ya tratado: siempre desde el máster, así se puede
volver a pasar (o ajustar la receta) sin acumular correcciones.

Receta — sobria, igual para todas, pensada para que el conjunto se vea como
una sola serie y no como fotos de móvil sueltas:

  1. Niveles por luminancia (no por canal: no cambia el color). Punto negro
     en el 0,4 % más oscuro; punto blanco en el 99,6 %, con la ganancia
     limitada (×1,25) para no quemar ni aplastar las fotos de escenario de
     fondo negro.
  2. Medios tonos: gamma suave hacia una luminancia media de 0,46, con la
     corrección limitada a 0,85–1,15 (no se «arregla» la noche).
  3. Curva en S leve (contraste +8 %), simétrica en 0,5.
  4. Saturación hacia un objetivo común (0,30), factor limitado a 0,90–1,12:
     baja las fotos chillonas (neón, focos) y sube un poco las apagadas.
  5. Reescalado Lanczos y enfoque de salida (máscara de enfoque suave),
     después de reducir.

    python3 studio/gallery/tratar.py              # todas
    python3 studio/gallery/tratar.py 14-4-sani-1  # una o varias
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps

RAIZ = Path(__file__).resolve().parents[2]
ORIGENES = RAIZ / "studio" / "gallery" / "originales"
SALIDA = RAIZ / "docs" / "gallery"
SM = SALIDA / "sm"

# Receta
NEGRO_PCT, BLANCO_PCT = 0.4, 99.6
GANANCIA_MAX = 1.25
MEDIA_OBJETIVO = 0.46
GAMMA_MIN, GAMMA_MAX = 0.85, 1.15
CONTRASTE = 0.08
SAT_OBJETIVO = 0.30
SAT_MIN, SAT_MAX = 0.90, 1.12


def luminancia(rgb):
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def tratar(im):
    rgb = np.asarray(im.convert("RGB"), dtype=np.float32) / 255.0
    Y = luminancia(rgb)

    # 1 · niveles por luminancia (mismo factor a los tres canales)
    lo, hi = np.percentile(Y, [NEGRO_PCT, BLANCO_PCT])
    hi = max(hi, lo + 1e-3)
    escala = min(1.0 / (hi - lo), GANANCIA_MAX / max(1e-3, 1.0 - lo))
    rgb = np.clip((rgb - lo) * escala, 0.0, 1.0)

    # 2 · medios tonos
    Y = luminancia(rgb)
    media = float(np.clip(np.median(Y), 0.02, 0.98))
    g = np.log(MEDIA_OBJETIVO) / np.log(media)
    g = float(np.clip(g, GAMMA_MIN, GAMMA_MAX))
    rgb = np.power(rgb, g)

    # 3 · curva en S suave
    rgb = rgb + CONTRASTE * (rgb - 0.5) * (1.0 - np.abs(2.0 * rgb - 1.0)) * 2.0
    rgb = np.clip(rgb, 0.0, 1.0)

    # 4 · saturación hacia un objetivo común
    Y = luminancia(rgb)[..., None]
    sat_actual = float(np.mean(np.max(rgb, -1) - np.min(rgb, -1)))
    f = float(np.clip(SAT_OBJETIVO / max(sat_actual, 1e-3), SAT_MIN, SAT_MAX))
    rgb = np.clip(Y + (rgb - Y) * f, 0.0, 1.0)

    return Image.fromarray((rgb * 255.0 + 0.5).astype(np.uint8), "RGB")


def a_tamano(im, lado):
    im = im.copy()
    im.thumbnail((lado, lado), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=55, threshold=2))


def procesar(origen):
    nombre = origen.stem
    im = ImageOps.exif_transpose(Image.open(origen)).convert("RGB")
    t = tratar(im)
    grande = a_tamano(t, 1600)
    grande.save(SALIDA / f"{nombre}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
    peq = a_tamano(t, 900)
    peq.save(SM / f"{nombre}.jpg", "JPEG", quality=78, optimize=True, progressive=True)
    peq.save(SM / f"{nombre}.webp", "WEBP", quality=74, method=6)
    return nombre, grande.size


if __name__ == "__main__":
    SM.mkdir(parents=True, exist_ok=True)
    pedidos = sys.argv[1:]
    fuentes = sorted(ORIGENES.glob("*.jpg"))
    if pedidos:
        fuentes = [f for f in fuentes if f.stem in pedidos]
    for f in fuentes:
        n, (w, h) = procesar(f)
        print(f"{n:28s} {w}×{h}")
