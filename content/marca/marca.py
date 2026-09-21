#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — la marca.

Fuente única del logotipo: todo lo que lo use lo pide aquí, para que no haya
dos versiones separándose con el tiempo.

LA IDEA. El colectivo imprime. Un registro corrido —dos planchas, y una que se
desplaza— es literalmente algo fuera de lugar, y es propio de su medio en vez
de impuesto desde fuera. De un mismo dibujo salen la versión a dos tintas (la
plancha de atrás, corrida) y la de una (esa plancha queda en contorno).

DOS PIEZAS, porque un solo dibujo no hace los dos trabajos:

  monograma  la C. Para lo pequeño: la foto de perfil —que recorta en
             círculo—, el favicon, el pie de un cartel. Sin letra que leer,
             así que aguanta a 16 px.
  lockup     las siglas apiladas, con el mismo corrimiento. Se empastan por
             debajo de 48 px: es para donde hay sitio.
  linea      monograma y siglas en horizontal, para firmas y pies.

SISTEMA. Un centro, dos radios y un grosor. La boca de la C se corta en
vertical, sobre el eje —no perpendicular al arco—, que es lo que hace que una
marca geométrica parezca dibujada y no recortada. Todo el dibujo cabe dentro
del círculo inscrito, así que el recorte circular de Instagram no se come nada.

    python3 marca.py          exporta svg/ y la hoja de muestras
    python3 marca.py --hoja   sólo la hoja
"""
import os, sys, math

AQUI = os.path.dirname(os.path.abspath(__file__))

AMBAR  = "#ffb923"   # el ámbar del colectivo: el del logotipo y el del manifiesto
HONDO  = "#c07d00"   # ámbar hondo — la plancha de atrás sobre campo ámbar
NEGRO  = "#171513"   # la tinta impresa, negro cálido
ZAFIRO = "#332f8a"   # la tinta de la web
CREMA  = "#fff4d6"
BLANCO = "#ffffff"

TINTAS = {"negro": NEGRO, "blanco": BLANCO, "zafiro": ZAFIRO, "ambar": AMBAR,
          "crema": CREMA, "auto": "currentColor"}
FONDOS = {"ambar": AMBAR, "negro": NEGRO, "blanco": BLANCO, "ninguno": None}

FUENTE = "FuturaStd, Helvetica Neue, Helvetica, Arial, sans-serif"

# ── el sistema ─────────────────────────────────────────────────────────────
CX = CY = 50
R, r = 36, 17          # radios → grosor 19
K = 10                 # la boca: corte vertical a 10 del eje
YO = math.sqrt(R*R - K*K)
YI = math.sqrt(r*r - K*K)
CORRIMIENTO = 8        # cuánto se desplaza la plancha de atrás


def _C():
    """La C: anillo con la boca cortada en vertical."""
    return (f"M{CX+K} {CY-YO:.2f} A{R} {R} 0 1 0 {CX+K} {CY+YO:.2f} "
            f"L{CX+K} {CY+YI:.2f} A{r} {r} 0 1 1 {CX+K} {CY-YI:.2f} Z")


def _siglas(size=41, x=13, y1=49, y2=88):
    return (f'<text x="{x}" y="{y1}" font-family="{FUENTE}" font-size="{size}">C.F.</text>'
            f'<text x="{x}" y="{y2}" font-family="{FUENTE}" font-size="{size}">D.L.</text>')


def _fantasma(tinta, fondo):
    """El color de la plancha de atrás, según sobre qué se imprima."""
    if fondo == AMBAR:  return HONDO
    if fondo == NEGRO:  return CREMA
    if tinta in (AMBAR, CREMA, BLANCO): return CREMA if tinta != CREMA else AMBAR
    return AMBAR


# ── piezas ─────────────────────────────────────────────────────────────────
def _monograma(tinta, fondo, modo):
    c = _C()
    if modo == "plano":
        return f'<path d="{c}" fill="{tinta}"/>'
    if modo == "mono":
        o = -(CORRIMIENTO + 1) / 2
        return (f'<g transform="translate({o},{o})">'
                f'<path d="{c}" fill="none" stroke="{tinta}" stroke-width="2.5" '
                f'transform="translate({CORRIMIENTO+1},{CORRIMIENTO+1})"/>'
                f'<path d="{c}" fill="{tinta}"/></g>')
    g = _fantasma(tinta, fondo)
    # Centrado óptico: con la plancha de atrás corrida, la masa del conjunto se
    # va abajo-derecha. Se devuelve el grupo medio corrimiento hacia arriba y a
    # la izquierda para que el dibujo entero quede centrado en el cuadrado — que
    # es lo que importa cuando Instagram lo recorta en círculo.
    o = -CORRIMIENTO / 2
    return (f'<g transform="translate({o},{o})">'
            f'<path d="{c}" fill="{g}" '
            f'transform="translate({CORRIMIENTO},{CORRIMIENTO})"/>'
            f'<path d="{c}" fill="{tinta}"/></g>')


def _lockup(tinta, fondo, modo):
    t = _siglas()
    if modo == "plano":
        return f'<g fill="{tinta}">{t}</g>'
    if modo == "mono":
        return (f'<g fill="none" stroke="{tinta}" stroke-width="1.4" '
                f'transform="translate(7,7)">{t}</g><g fill="{tinta}">{t}</g>')
    g = _fantasma(tinta, fondo)
    return f'<g fill="{g}" transform="translate(7,7)">{t}</g><g fill="{tinta}">{t}</g>'


def _linea(tinta, fondo, modo):
    mono = _monograma(tinta, fondo, modo)
    t = (f'<text x="120" y="68" font-family="{FUENTE}" font-size="44">C.F.D.L.</text>')
    if modo == "plano":
        letras = f'<g fill="{tinta}">{t}</g>'
    elif modo == "mono":
        letras = (f'<g fill="none" stroke="{tinta}" stroke-width="1.4" '
                  f'transform="translate(7,7)">{t}</g><g fill="{tinta}">{t}</g>')
    else:
        g = _fantasma(tinta, fondo)
        letras = (f'<g fill="{g}" transform="translate(7,7)">{t}</g>'
                  f'<g fill="{tinta}">{t}</g>')
    return mono + letras


PIEZAS = {"monograma": (_monograma, 100, 100),
          "lockup":    (_lockup,    100, 100),
          "linea":     (_linea,     340, 100)}
MODOS = ("duo", "mono", "plano")


def svg(pieza="monograma", fondo="ambar", tinta="negro", modo="duo",
        size=None, clase=""):
    """El SVG como cadena.

    pieza  monograma | lockup | linea
    fondo  ambar | negro | blanco | ninguno
    tinta  negro | blanco | zafiro | ambar | crema | auto (hereda currentColor)
    modo   duo (dos tintas) | mono (plancha en contorno) | plano (sin corrimiento)
    """
    if pieza not in PIEZAS:
        raise SystemExit(f"pieza desconocida: {pieza} (hay {', '.join(PIEZAS)})")
    if modo not in MODOS:
        raise SystemExit(f"modo desconocido: {modo} (hay {', '.join(MODOS)})")
    fn, W, H = PIEZAS[pieza]
    col = TINTAS.get(tinta, tinta)
    bg = FONDOS.get(fondo, fondo)
    campo = f'<rect width="{W}" height="{H}" fill="{bg}"/>' if bg else ""
    dim = ""
    if size:
        dim = f' width="{round(size*W/H)}" height="{size}"'
    cls = f' class="{clase}"' if clase else ""
    return (f'<svg{cls} viewBox="0 0 {W} {H}"{dim} '
            f'xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="C.F.D.L.">{campo}{fn(col, bg, modo)}</svg>')


# ── exportación ────────────────────────────────────────────────────────────
COMBOS = [
    # pieza, fondo, tinta, modo
    ("monograma", "ambar",   "negro",  "duo"),    # principal
    ("monograma", "ninguno", "negro",  "duo"),
    ("monograma", "negro",   "ambar",  "duo"),
    ("monograma", "ninguno", "zafiro", "duo"),
    ("monograma", "ninguno", "negro",  "mono"),
    ("monograma", "ninguno", "blanco", "mono"),
    ("monograma", "ambar",   "negro",  "plano"),
    ("monograma", "ninguno", "negro",  "plano"),
    ("monograma", "ninguno", "blanco", "plano"),
    ("lockup",    "ambar",   "negro",  "duo"),
    ("lockup",    "ninguno", "negro",  "duo"),
    ("lockup",    "negro",   "ambar",  "duo"),
    ("lockup",    "ninguno", "negro",  "plano"),
    ("lockup",    "ninguno", "blanco", "plano"),
    ("linea",     "ninguno", "negro",  "duo"),
    ("linea",     "ninguno", "blanco", "plano"),
    ("linea",     "ambar",   "negro",  "duo"),
]


def exportar():
    d = os.path.join(AQUI, "svg")
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        if f.endswith(".svg"):
            os.remove(os.path.join(d, f))
    for pieza, fondo, tinta, modo in COMBOS:
        nom = f"cfdl-{pieza}-{modo}-{fondo}-{tinta}.svg"
        with open(os.path.join(d, nom), "w", encoding="utf-8") as fh:
            fh.write(svg(pieza, fondo, tinta, modo))
    print(f"{len(COMBOS)} SVG → content/marca/svg/")


def hoja():
    def caja(pieza, fondo, tinta, modo, size, css, et, circ=False):
        s = svg(pieza, fondo, tinta, modo, size)
        if circ:
            s = f'<span class="circ">{s}</span>'
        return (f'<div class="c"><span class="caja {css}">{s}</span>'
                f'<div class="et">{et}</div></div>')

    p = []
    p.append('<h2>monograma · principal — dos tintas</h2><div class="fila">')
    p.append(caja("monograma","ambar","negro","duo",112,"b-cuadros","círculo · perfil",True))
    p.append(caja("monograma","ambar","negro","duo",104,"b-cuadros","104"))
    p.append(caja("monograma","ambar","negro","duo",48,"b-cuadros","48 · pie"))
    p.append(caja("monograma","ambar","negro","duo",32,"b-cuadros","32 · favicon"))
    p.append(caja("monograma","ambar","negro","duo",16,"b-blanco","16"))
    p.append("</div>")

    p.append('<h2>monograma · sobre cada fondo</h2><div class="fila">')
    for f_, t, m, css, et in [("ambar","negro","duo","b-cuadros","campo ámbar"),
                              ("ninguno","negro","duo","b-blanco","sin campo"),
                              ("ninguno","zafiro","duo","b-rosa","zafiro sobre rosa"),
                              ("negro","ambar","duo","b-cuadros","campo negro"),
                              ("ninguno","blanco","mono","b-negro","una tinta, blanco")]:
        p.append(caja("monograma", f_, t, m, 96, css, et))
    p.append("</div>")

    p.append('<h2>monograma · los tres modos</h2><div class="fila">')
    for m, et in [("duo","duo — dos planchas"), ("mono","mono — contorno"),
                  ("plano","plano — sin corrimiento")]:
        p.append(caja("monograma","ambar","negro",m,96,"b-cuadros",et))
        p.append(caja("monograma","ambar","negro",m,32,"b-cuadros",f"{et.split(' ')[0]} a 32"))
    p.append("</div>")

    p.append('<h2>lockup — para donde hay sitio</h2><div class="fila">')
    for f_, t, m, css, et in [("ambar","negro","duo","b-cuadros","campo ámbar"),
                              ("ninguno","negro","duo","b-blanco","sin campo"),
                              ("negro","ambar","duo","b-cuadros","campo negro"),
                              ("ninguno","blanco","plano","b-negro","plano, blanco")]:
        p.append(caja("lockup", f_, t, m, 104, css, et))
    p.append(caja("lockup","ambar","negro","duo",48,"b-cuadros","48 — se empasta"))
    p.append("</div>")

    p.append('<h2>línea — firmas y pies</h2><div class="fila">')
    for f_, t, m, css, et in [("ninguno","negro","duo","b-blanco","negro"),
                              ("ninguno","blanco","plano","b-negro","blanco, plano"),
                              ("ambar","negro","duo","b-cuadros","con campo")]:
        p.append(caja("linea", f_, t, m, 62, css, et))
    p.append("</div>")

    doc = HOJA.format(cuerpo="".join(p))
    with open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("hoja → content/marca/index.html")


HOJA = """<!doctype html><meta charset="utf-8"><title>C.F.D.L. — la marca</title>
<style>
@font-face{{font-family:'FuturaStd';
  src:url('../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');
  font-display:block}}
*{{box-sizing:border-box}}
body{{margin:0;padding:34px 38px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
h2{{font:400 11px/1 system-ui;letter-spacing:.2em;text-transform:uppercase;color:#6f6f88;
   margin:34px 0 14px;border-top:1px solid #2a2a38;padding-top:16px}}
.intro{{color:#9a9ab0;max-width:900px;margin:0}} .intro b{{color:#e6e6ef;font-weight:500}}
.fila{{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-end}}
.c{{text-align:center}} .c .et{{font-size:10px;color:#6f6f88;margin-top:7px;letter-spacing:.05em}}
.caja{{line-height:0;display:inline-block;padding:10px}}
.b-rosa{{background:#f8ccce}} .b-blanco{{background:#fff}} .b-negro{{background:#171513}}
.b-cuadros{{background:
  linear-gradient(45deg,#3a3a48 25%,transparent 25%,transparent 75%,#3a3a48 75%),
  linear-gradient(45deg,#3a3a48 25%,#2a2a34 25%,#2a2a34 75%,#3a3a48 75%);
  background-size:14px 14px;background-position:0 0,7px 7px}}
.circ{{border-radius:50%;overflow:hidden;display:inline-block;line-height:0}}
</style>
<h1>C.F.D.L. — la marca</h1>
<p class="intro">El colectivo imprime. Un <b>registro corrido</b> —dos planchas, y
una que se desplaza— es literalmente algo fuera de lugar, y es propio de su medio
en vez de impuesto desde fuera. Del mismo dibujo salen la versión a dos tintas y
la de una.<br>El <b>monograma</b> lleva lo pequeño: perfil, favicon, pie de cartel.
El <b>lockup</b>, lo grande. Por debajo de 48&nbsp;px las siglas se empastan; por eso
son dos piezas y no una.</p>
{cuerpo}
"""

if __name__ == "__main__":
    if "--hoja" not in sys.argv:
        exportar()
    hoja()
