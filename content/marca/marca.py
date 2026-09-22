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

DENSIDAD EN VEZ DE VARIANTES. Una espiral de muchos anillos se empasta en un
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

# De lockup, que a su vez los toma de content/paleta/. Una sola fuente.
from lockup import AMBAR, NEGRO, ZAFIRO, CREMA, BLANCO, ROSA, PAPEL

TINTAS = {"negro": NEGRO, "blanco": BLANCO, "zafiro": ZAFIRO, "ambar": AMBAR,
          "crema": CREMA, "rosa": ROSA, "papel": PAPEL,
          "auto": "currentColor"}
FONDOS = {"ambar": AMBAR, "negro": NEGRO, "blanco": BLANCO,
          "papel": PAPEL, "ninguno": None}
FUENTE = "FuturaStd, Helvetica Neue, Helvetica, Arial, sans-serif"

from espiral import espiral as _espiral_pts, polilinea, U as W
import lockup

RATIO_HOJA = 0.571          # medido sobre la hoja impresa

# LA BANDA DEL MARGEN. En la hoja impresa el texto vive en los márgenes y el
# centro queda vacío: el colectivo está fuera de lugar, en los bordes. Medido
# sobre el original (svg_espiral_frame en content/tshirts): trazo 1, hueco 4,
# siete anillos — la banda ocupa ~18 % de cada lado y deja ~65 % en blanco.
# El aire entre vueltas es CUATRO VECES el grosor, no igual.
#
# Una banda fina se cierra en cuanto se reduce, así que la densidad baja con el
# tamaño: menos anillos y menos aire, conservando el centro vacío.
# La tabla vive en lockup.py y se deriva aquí: tenerla dos veces ya provocó
# una deriva antes.
#          anillos, grosor, hueco, lado en módulos  → vacío
DENSIDAD = {d: (a["anillos"], 1, a["hu"],
                round(2 * a["anillos"] * (1 + a["hu"]) / (1 - a["vacio"])))
            for d, a in lockup.DENSIDAD.items()}
#  grande 104 px — 6 anillos, aire 1:3, vacío 55 %
#  medio   60 px — 5 anillos, 60 %   ·   pequeno 30 px — 3 cerrados, 55 %
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
def _desmonta(sv):
    """Saca el cuerpo y el viewBox de un SVG ya armado por lockup."""
    import re as _re
    m = _re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', sv)
    cuerpo = sv[sv.index(">", sv.index("<svg")) + 1: sv.rindex("</svg>")]
    return cuerpo, float(m.group(1)), float(m.group(2))


def _linea(t, d):
    return _desmonta(lockup.firma(d, tinta=t, alto=100))


# El nombre desplegado, en tres líneas a la izquierda. No baja de 60 px de
# alto: por debajo la mayúscula cae de 13 px y las tres líneas dejan de
# leerse — ahí es la firma corta la que toca.
def _nombre(t, d):
    return _desmonta(lockup.firma_nombre(d, tinta=t, alto=100))


PIEZAS = ("monograma", "perfil", "hoja", "linea", "nombre")
_FN = {"monograma": _monograma, "perfil": _perfil, "hoja": _hoja,
       "linea": _linea, "nombre": _nombre}
_ARMADAS = ("linea", "nombre")   # las que ya vienen con su viewBox hecho


def svg(pieza="monograma", fondo="ambar", tinta="negro", densidad="grande",
        size=None, clase=""):
    """El SVG como cadena.

    pieza     monograma | perfil (a prueba de círculo) | hoja |
              linea (símbolo + C.F.D.L.) | nombre (+ el nombre entero)
    fondo     ambar | negro | blanco | ninguno
    tinta     negro | blanco | zafiro | ambar | crema | auto (currentColor)
    densidad  grande (104 px) | medio (60) | pequeno (30)
    """
    if pieza not in PIEZAS:
        raise SystemExit(f"pieza desconocida: {pieza} (hay {', '.join(PIEZAS)})")
    if densidad not in DENSIDAD:
        raise SystemExit(f"densidad desconocida: {densidad} (hay {', '.join(DENSIDAD)})")
    col = TINTAS.get(tinta, tinta)
    bg = FONDOS.get(fondo, fondo)
    r = _FN[pieza](col, densidad)
    if pieza in _ARMADAS:
        cuerpo, VW, VH = r
        escala = ""
    else:
        cuerpo, CN, CM = r
        VW, VH = W, W * CM / CN
        escala = ""
    campo = f'<rect width="{VW}" height="{VH:.2f}" fill="{bg}"/>' if bg else ""
    dim = f' width="{round(size*VW/VH)}" height="{size}"' if size else ""
    cls = f' class="{clase}"' if clase else ""
    etq = "Colectivo Fuera de Lugar" if pieza == "nombre" else "C.F.D.L."
    return (f'<svg{cls} viewBox="0 0 {VW} {VH:.2f}"{dim} '
            f'xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="{etq}">{campo}{escala}{cuerpo}</svg>')


COMBOS = [
    ("monograma", "ambar",   "negro",  "grande"),     # principal
    ("perfil",    "ambar",   "negro",  "grande"),     # foto de perfil, a prueba de círculo
    ("monograma", "ninguno", "negro",  "grande"),
    ("monograma", "negro",   "ambar",  "grande"),
    ("monograma", "ninguno", "zafiro", "grande"),
    ("monograma", "ninguno", "blanco", "grande"),
    ("monograma", "ambar",   "negro",  "medio"),
    ("monograma", "ambar",   "negro",  "pequeno"),   # favicon
    ("monograma", "ninguno", "negro",  "pequeno"),
    ("monograma", "ninguno", "blanco", "pequeno"),
    ("monograma", "negro",   "blanco", "medio"),
    ("monograma", "ninguno", "zafiro", "medio"),
    ("hoja",      "ambar",   "negro",  "grande"),
    ("hoja",      "ninguno", "negro",  "grande"),
    ("hoja",      "negro",   "ambar",  "grande"),
    ("linea",     "ninguno", "negro",  "medio"),
    ("linea",     "ninguno", "zafiro", "medio"),
    ("linea",     "negro",   "blanco", "medio"),
    ("linea",     "ninguno", "rosa",   "medio"),
    ("linea",     "ninguno", "blanco", "medio"),
    ("linea",     "ambar",   "negro",  "medio"),
    ("nombre",    "ninguno", "negro",  "medio"),
    ("nombre",    "ninguno", "zafiro", "medio"),
    ("nombre",    "negro",   "blanco", "medio"),
    ("nombre",    "negro",   "ambar",  "medio"),
    ("nombre",    "ambar",   "negro",  "medio"),
    ("nombre",    "ninguno", "blanco", "medio"),
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
    ("b-papel",  "papel",  PAPEL,  ["negro", "zafiro"]),
    ("b-negro",  "negro",  NEGRO,  ["ambar", "blanco", "crema"]),
    ("b-ambar",  "ámbar",  AMBAR,  ["negro"]),
    ("b-rosa",   "rosa",   ROSA,   ["zafiro", "negro"]),
    ("b-zafiro", "zafiro", ZAFIRO, ["ambar", "crema"]),
]


def hoja_muestras():
    """La página vive en hoja.py, que es donde se decide qué se enseña."""
    from hoja import pagina
    pagina()


if __name__ == "__main__":
    if "--hoja" not in sys.argv:
        exportar()
    hoja_muestras()
