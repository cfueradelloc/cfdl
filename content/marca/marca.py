#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — la marca.

Fuente única del logotipo. Lo que lo use lo pide aquí, para que no haya dos
versiones separándose con el tiempo.

LA IDEA. El manifiesto impreso compone su texto como una ESPIRAL RECTANGULAR:
rectángulos encajados girando hacia dentro, con la vuelta interior cortada a
media altura. No cierra nunca — «cambiante y nunca cumplido». La marca es esa
espiral, estilizada hasta que aguanta a 16 px.

No hace falta inventarle un símbolo al colectivo: ya tiene uno, y está impreso.

DENSIDAD EN VEZ DE VARIANTES. Una espiral de siete anillos se empasta en un
favicon. En lugar de dibujar marcas distintas, se elige cuántas vueltas según
el tamaño: `fina` para lo grande, `gruesa` para lo diminuto. Es el mismo signo.

PIEZAS
  monograma  cuadrado. Perfil (que recorta en círculo), favicon, pie de cartel.
  hoja       proporción 0.571 — la de la hoja impresa. Vertical, para cabeceras.
  linea      la firma: monograma y siglas en horizontal, para firmas y pies.
             La construye lockup.py, que es donde viven sus reglas.

    python3 marca.py          exporta svg/ y la hoja de muestras
    python3 marca.py --hoja   sólo la hoja
"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))

AMBAR  = "#ffb923"   # el ámbar del colectivo: el del logotipo y el del manifiesto
NEGRO  = "#171513"   # la tinta impresa, negro cálido
ZAFIRO = "#332f8a"   # la tinta de la web
CREMA  = "#fff4d6"
BLANCO = "#ffffff"

TINTAS = {"negro": NEGRO, "blanco": BLANCO, "zafiro": ZAFIRO, "ambar": AMBAR,
          "crema": CREMA, "auto": "currentColor"}
FONDOS = {"ambar": AMBAR, "negro": NEGRO, "blanco": BLANCO, "ninguno": None}
FUENTE = "FuturaStd, Helvetica Neue, Helvetica, Arial, sans-serif"

from espiral import espiral as _espiral_pts, polilinea, U as W

RATIO_HOJA = 0.571          # medido sobre la hoja impresa

# LA BANDA DEL MARGEN. En la hoja impresa el texto vive en los márgenes y el
# centro queda vacío: el colectivo está fuera de lugar, en los bordes. Medido
# sobre el original (svg_espiral_frame en content/tshirts): trazo 1, hueco 4,
# siete anillos — la banda ocupa ~18 % de cada lado y deja ~65 % en blanco.
# El aire entre vueltas es CUATRO VECES el grosor, no igual.
#
# Una banda fina se cierra en cuanto se reduce, así que la densidad baja con el
# tamaño: menos anillos y menos aire, conservando el centro vacío.
#            anillos, grosor, hueco, lado en módulos  → vacío
DENSIDAD = {"fina":   (7, 1, 4, 200),   # ≥64 px — la densidad de la hoja, 65 %
            "media":  (5, 1, 3, 100),   # 32–64 px — 60 %
            "gruesa": (3, 1, 2, 40)}    # <32 px — 55 %
CORTE_REL = 0.55            # dónde muere la última vuelta, sobre su recta


def _espiral(tinta, densidad, alto_rel=1.0, margen_rel=0.0):
    """La espiral del margen, centrada en su caja."""
    anillos, gr, hu, N = DENSIDAD[densidad]
    M = round(N * alto_rel)
    banda = anillos * (gr + hu)
    corte = banda + (min(N, M) - 2 * banda) * CORTE_REL
    P, N_, M_, g = _espiral_pts(N=N, M=M, vueltas=anillos, gr=gr, hu=hu,
                                corte=corte)
    m = round(N * margen_rel)
    CN = N + 2 * m
    return polilinea(P, CN, g, tinta, desplaza=(m, m)), CN, M + 2 * m


def vacio(densidad):
    """Qué fracción del lado queda en blanco en el centro."""
    anillos, gr, hu, N = DENSIDAD[densidad]
    return (N - 2 * anillos * (gr + hu)) / N


def _siglas(tinta, x, y, size, anchor="start"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FUENTE}" '
            f'font-size="{size}" fill="{tinta}">C.F.D.L.</text>')


# Fracción del lado que se mete hacia dentro para el recorte circular. Con
# 0,11 la semidiagonal del cuadrado (55,2) superaba el radio (50) y las
# esquinas se cortaban; 0,20 la deja en 42,4 — el 85 % del radio.
MARGEN_CIRCULO = 0.20


# El símbolo solo nunca toca el límite de su caja: 0,12 de aire por lado.
def _monograma(t, d): return _espiral(t, d, 1.0, 0.12)
def _perfil(t, d):    return _espiral(t, d, 1.0, MARGEN_CIRCULO)
def _hoja(t, d):      return _espiral(t, d, 1 / RATIO_HOJA, 0.10)


# La firma no se dibuja aquí: la construye lockup.py, que es donde viven sus
# reglas (gris, separación, tamaño relativo). Tenerla en dos sitios es como
# acaban divergiendo dos versiones de la misma marca.
def _linea(t, d):
    from lockup import firma as _firma
    sv = _firma(d, tinta=t, alto=100)
    import re as _re
    m = _re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', sv)
    W, H = float(m.group(1)), float(m.group(2))
    cuerpo = sv[sv.index(">", sv.index("<svg")) + 1: sv.rindex("</svg>")]
    return cuerpo, W, H


PIEZAS = ("monograma", "perfil", "hoja", "linea")
_FN = {"monograma": _monograma, "perfil": _perfil, "hoja": _hoja,
       "linea": _linea}


def svg(pieza="monograma", fondo="ambar", tinta="negro", densidad="fina",
        size=None, clase=""):
    """El SVG como cadena.

    pieza     monograma | perfil (a prueba de círculo) | hoja | linea
    fondo     ambar | negro | blanco | ninguno
    tinta     negro | blanco | zafiro | ambar | crema | auto (currentColor)
    densidad  fina (≥64 px) | media (32–64) | gruesa (<32)
    """
    if pieza not in PIEZAS:
        raise SystemExit(f"pieza desconocida: {pieza} (hay {', '.join(PIEZAS)})")
    if densidad not in DENSIDAD:
        raise SystemExit(f"densidad desconocida: {densidad} (hay {', '.join(DENSIDAD)})")
    col = TINTAS.get(tinta, tinta)
    bg = FONDOS.get(fondo, fondo)
    r = _FN[pieza](col, densidad)
    if pieza == "linea":
        cuerpo, VW, VH = r
        escala = ""
    else:
        cuerpo, CN, CM = r
        VW, VH = W, W * CM / CN
        escala = ""
    campo = f'<rect width="{VW}" height="{VH:.2f}" fill="{bg}"/>' if bg else ""
    dim = f' width="{round(size*VW/VH)}" height="{size}"' if size else ""
    cls = f' class="{clase}"' if clase else ""
    return (f'<svg{cls} viewBox="0 0 {VW} {VH:.2f}"{dim} '
            f'xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="C.F.D.L.">{campo}{escala}{cuerpo}</svg>')


COMBOS = [
    ("monograma", "ambar",   "negro",  "fina"),     # principal
    ("perfil",    "ambar",   "negro",  "fina"),     # foto de perfil, a prueba de círculo
    ("monograma", "ninguno", "negro",  "fina"),
    ("monograma", "negro",   "ambar",  "fina"),
    ("monograma", "ninguno", "zafiro", "fina"),
    ("monograma", "ninguno", "blanco", "fina"),
    ("monograma", "ambar",   "negro",  "media"),
    ("monograma", "ambar",   "negro",  "gruesa"),   # favicon
    ("monograma", "ninguno", "negro",  "gruesa"),
    ("monograma", "ninguno", "blanco", "gruesa"),
    ("monograma", "negro",   "blanco", "media"),
    ("monograma", "ninguno", "zafiro", "media"),
    ("hoja",      "ambar",   "negro",  "fina"),
    ("hoja",      "ninguno", "negro",  "fina"),
    ("hoja",      "negro",   "ambar",  "fina"),
    ("linea",     "ninguno", "negro",  "media"),
    ("linea",     "ninguno", "zafiro", "media"),
    ("linea",     "negro",   "blanco", "media"),
    ("linea",     "ninguno", "blanco", "media"),
    ("linea",     "ambar",   "negro",  "media"),
]


def exportar():
    d = os.path.join(AQUI, "svg")
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        if f.endswith(".svg"):
            os.remove(os.path.join(d, f))
    for pieza, fondo, tinta, dens in COMBOS:
        with open(os.path.join(d, f"cfdl-{pieza}-{dens}-{fondo}-{tinta}.svg"),
                  "w", encoding="utf-8") as fh:
            fh.write(svg(pieza, fondo, tinta, dens))
    print(f"{len(COMBOS)} SVG → content/marca/svg/")


GROUNDS = [
    ("b-blanco", "blanco", "#ffffff", ["negro", "zafiro"]),
    ("b-negro",  "negro",  "#171513", ["ambar", "blanco", "crema"]),
    ("b-ambar",  "ámbar",  "#ffb923", ["negro"]),
    ("b-rosa",   "rosa",   "#f8ccce", ["zafiro", "negro"]),
    ("b-zafiro", "zafiro", "#332f8a", ["ambar", "crema"]),
]


def hoja_muestras():
    """La página vive en hoja.py, que es donde se decide qué se enseña."""
    from hoja import pagina
    pagina()


if __name__ == "__main__":
    if "--hoja" not in sys.argv:
        exportar()
    hoja_muestras()
