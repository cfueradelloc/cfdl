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
  linea      monograma y siglas en horizontal, para firmas y pies.
  lockup     monograma sobre las siglas, apilado.

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

W = 100
RATIO_HOJA = 0.571          # medido de la hoja impresa

# vueltas, grosor, hueco — elegidos para que el trazo siga viéndose al reducir
DENSIDAD = {"fina":   (3.5, 6.5, 7.5),
            "media":  (2.5, 10.0, 10.0),
            "gruesa": (2.0, 13.0, 12.0)}
CORTE = 0.45                # cuánto dibuja la última recta: el gesto abierto


def _puntos(vueltas, w, g, alto, corte, margen=0.0):
    """Espiral rectangular hacia dentro, desde la esquina superior izquierda."""
    p, o = w + g, w / 2 + margen
    l, t, r, b = o, o, W - o, alto - o
    P = [(l, t)]
    n = int(vueltas * 4)
    for k in range(n):
        if r - l < p * 0.6 or b - t < p * 0.6:
            break
        f = corte if k == n - 1 else 1.0
        lado = k % 4
        if lado == 0:    P.append((l + (r - l) * f, t))
        elif lado == 1:  P.append((r, t + (b - t) * f))
        elif lado == 2:  P.append((r - (r - l) * f, b)); t += p
        else:            P.append((l, b - (b - t) * f)); l += p; r -= p; b -= p
    return P


def _espiral(tinta, densidad, alto=W, corte=CORTE, margen=0.0):
    """La espiral, centrada ópticamente dentro de su caja.

    Una espiral hacia dentro carga su masa hacia un lado; sin corregirlo, el
    avatar se ve descolgado.

    `margen` mete el dibujo hacia dentro. Con 15 el cuadrado entero cabe en el
    círculo inscrito (la semidiagonal de un cuadrado de lado 70 es 49,5 < 50),
    así que el recorte circular de Instagram no se come ninguna esquina — y a
    una espiral rectangular perder las esquinas no le sienta como un recorte,
    le sienta como una avería."""
    vueltas, w, g = DENSIDAD[densidad]
    P = _puntos(vueltas, w, g, alto, corte, margen)
    xs = [x for x, _ in P]; ys = [y for _, y in P]
    dx = W / 2 - (min(xs) + max(xs)) / 2
    dy = alto / 2 - (min(ys) + max(ys)) / 2
    d = " ".join(f"{x:.2f},{y:.2f}" for x, y in P)
    return (f'<polyline points="{d}" fill="none" stroke="{tinta}" '
            f'stroke-width="{w}" stroke-linejoin="miter" stroke-linecap="butt" '
            f'transform="translate({dx:.2f},{dy:.2f})"/>')


def _siglas(tinta, x, y, size, anchor="start"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FUENTE}" '
            f'font-size="{size}" fill="{tinta}">C.F.D.L.</text>')


MARGEN_CIRCULO = 15   # para que el cuadrado quepa entero en el círculo inscrito


# ── piezas ─────────────────────────────────────────────────────────────────
def _monograma(t, densidad): return _espiral(t, densidad, margen=6)
def _perfil(t, densidad):    return _espiral(t, densidad, margen=MARGEN_CIRCULO)

def _hoja(t, densidad):
    return _espiral(t, densidad, alto=round(W / RATIO_HOJA))

def _linea(t, densidad):
    # El signo ocupa el cuadrado de la izquierda; las siglas arrancan a una
    # distancia igual a un cuarto del signo, que es lo que impide que se lean
    # como una sola pieza.
    return (f'<g transform="translate(6,6) scale(0.88)">{_espiral(t, densidad)}</g>'
            + _siglas(t, 124, 63, 40))

def _lockup(t, densidad):
    return (f'<g transform="translate(28,6) scale(0.44)">{_espiral(t, densidad)}</g>'
            + _siglas(t, 50, 88, 23, "middle"))


PIEZAS = {"monograma": (_monograma, W, W),
          "perfil":    (_perfil,    W, W),
          "hoja":      (_hoja,      W, round(W / RATIO_HOJA)),
          "linea":     (_linea,     340, W),
          "lockup":    (_lockup,    W, W)}


def svg(pieza="monograma", fondo="ambar", tinta="negro", densidad="fina",
        size=None, clase=""):
    """El SVG como cadena.

    pieza     monograma | perfil (recorte circular) | hoja | linea | lockup
    fondo     ambar | negro | blanco | ninguno
    tinta     negro | blanco | zafiro | ambar | crema | auto (currentColor)
    densidad  fina (grande) | media | gruesa (diminuto)
    """
    if pieza not in PIEZAS:
        raise SystemExit(f"pieza desconocida: {pieza} (hay {', '.join(PIEZAS)})")
    if densidad not in DENSIDAD:
        raise SystemExit(f"densidad desconocida: {densidad} (hay {', '.join(DENSIDAD)})")
    fn, VW, VH = PIEZAS[pieza]
    col = TINTAS.get(tinta, tinta)
    bg = FONDOS.get(fondo, fondo)
    campo = f'<rect width="{VW}" height="{VH}" fill="{bg}"/>' if bg else ""
    dim = f' width="{round(size*VW/VH)}" height="{size}"' if size else ""
    cls = f' class="{clase}"' if clase else ""
    return (f'<svg{cls} viewBox="0 0 {VW} {VH}"{dim} '
            f'xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="C.F.D.L.">{campo}{fn(col, densidad)}</svg>')


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
    ("hoja",      "ambar",   "negro",  "fina"),
    ("hoja",      "ninguno", "negro",  "fina"),
    ("hoja",      "negro",   "ambar",  "fina"),
    ("linea",     "ninguno", "negro",  "media"),
    ("linea",     "ninguno", "blanco", "media"),
    ("linea",     "ambar",   "negro",  "media"),
    ("lockup",    "ambar",   "negro",  "media"),
    ("lockup",    "ninguno", "negro",  "media"),
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
    def c(pieza, fondo, tinta, dens, size, css, et, circ=False):
        sv = svg(pieza, fondo, tinta, dens, size)
        if circ: sv = f'<span class="circ">{sv}</span>'
        return (f'<div class="c"><span class="caja {css}">{sv}</span>'
                f'<div class="et">{et}</div></div>')

    def parrilla(pieza, size, dens="fina", nota=""):
        """La pieza sobre cada fondo, con cada tinta que le sirve."""
        out = ['<div class="fila">']
        for css, nom, _hex, tintas in GROUNDS:
            for t in tintas:
                out.append(c(pieza, "ninguno", t, dens, size, css, f"{nom} · {t}"))
        out.append("</div>")
        return "".join(out)

    p = []
    p.append('<h2>monograma · principal</h2><div class="fila">')
    p.append(c("perfil","ambar","negro","fina",112,"b-cuadros","círculo · pieza «perfil»",True))
    p.append(c("monograma","ambar","negro","fina",112,"b-cuadros","«monograma» pierde esquinas",True))
    p.append(c("monograma","ambar","negro","fina",104,"b-cuadros","104 · fina"))
    p.append(c("monograma","ambar","negro","media",48,"b-cuadros","48 · media"))
    p.append(c("monograma","ambar","negro","gruesa",32,"b-cuadros","32 · gruesa"))
    p.append(c("monograma","ambar","negro","gruesa",16,"b-blanco","16 · gruesa"))
    p.append("</div>")

    p.append('<h2>la densidad se elige por tamaño — es el mismo signo</h2><div class="fila">')
    for dens in ("fina", "media", "gruesa"):
        p.append(c("monograma","ambar","negro",dens,104,"b-cuadros",dens))
        p.append(c("monograma","ambar","negro",dens,32,"b-cuadros",f"{dens} a 32"))
    p.append("</div>")

    p.append("<h2>el signo solo · sobre cada fondo, con cada tinta</h2>")
    p.append(parrilla("monograma", 84))

    p.append("<h2>con las siglas al lado · el caso de un pie o una firma</h2>")
    p.append(parrilla("linea", 54, "media"))

    p.append("<h2>apilado · cuando manda el eje vertical</h2>")
    p.append(parrilla("lockup", 92, "media"))

    p.append("<h2>con campo propio · el signo se lleva su fondo encima</h2><div class="
             "'fila'>")
    for pieza, size in (("monograma", 92), ("linea", 54), ("lockup", 92)):
        p.append(c(pieza,"ambar","negro","media",size,"b-blanco","campo ámbar sobre blanco"))
        p.append(c(pieza,"negro","ambar","media",size,"b-blanco","campo negro sobre blanco"))
        p.append(c(pieza,"ambar","negro","media",size,"b-negro","campo ámbar sobre negro"))
    p.append("</div>")

    p.append("<h2>hoja — proporción de la hoja impresa (0.571)</h2>")
    p.append(parrilla("hoja", 120))

    return_doc = HOJA.format(cuerpo="".join(p))
    with open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(return_doc)
    print("hoja → content/marca/index.html")


HOJA = """<!doctype html><meta charset="utf-8"><title>C.F.D.L. — la marca</title>
<style>
@font-face{{font-family:'FuturaStd';
  src:url('../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');font-display:block}}
*{{box-sizing:border-box}}
body{{margin:0;padding:34px 38px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
h2{{font:400 11px/1 system-ui;letter-spacing:.2em;text-transform:uppercase;color:#6f6f88;
   margin:34px 0 14px;border-top:1px solid #2a2a38;padding-top:16px}}
.intro{{color:#9a9ab0;max-width:920px;margin:0}} .intro b{{color:#e6e6ef;font-weight:500}}
.fila{{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end}}
.c{{text-align:center}} .c .et{{font-size:10px;color:#6f6f88;margin-top:7px;letter-spacing:.05em}}
.caja{{line-height:0;display:inline-block;padding:10px}}
.b-rosa{{background:#f8ccce}} .b-blanco{{background:#fff}}
.b-negro{{background:#171513}} .b-ambar{{background:#ffb923}}
.b-zafiro{{background:#332f8a}}
.b-cuadros{{background:
  linear-gradient(45deg,#3a3a48 25%,transparent 25%,transparent 75%,#3a3a48 75%),
  linear-gradient(45deg,#3a3a48 25%,#2a2a34 25%,#2a2a34 75%,#3a3a48 75%);
  background-size:14px 14px;background-position:0 0,7px 7px}}
.circ{{border-radius:50%;overflow:hidden;display:inline-block;line-height:0}}
a{{color:#ffb923}}
</style>
<h1>C.F.D.L. — la marca</h1>
<p class="intro">El manifiesto impreso compone su texto como una <b>espiral
rectangular</b>: rectángulos encajados girando hacia dentro, con la vuelta interior
cortada a media altura. <b>No cierra nunca</b> — «cambiante y nunca cumplido».
La marca es esa espiral, estilizada hasta que aguanta a 16&nbsp;px.<br>
No hacía falta inventarle un símbolo al colectivo: ya tenía uno, y está impreso.<br>
<a href="explorador.html">explorador de variantes →</a> barrido de parámetros:
vueltas, retícula, grosor, remate, boca, proporción, giro, tinta.</p>
{cuerpo}
"""

if __name__ == "__main__":
    if "--hoja" not in sys.argv:
        exportar()
    hoja_muestras()
