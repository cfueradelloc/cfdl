#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — las rondas, y la prueba que de verdad decide.

Un signo puede ser bonito solo y no servir: lo que decide es cómo se comporta
JUNTO A LAS SIGLAS. Ahí se ve si el peso óptico casa con el de la letra, si la
altura está bien puesta y si compiten o se acompañan.

Esta página pone cada ronda a esa prueba, sobre blanco y sobre negro, más los
tamaños pequeños.

    python3 rondas.py > rondas.html
"""
import math
from espiral import espiral, polilinea, U

AMBAR, HONDO, NEGRO, ZAFIRO, BLANCO, CREMA = ("#ffb923","#c07d00","#171513",
                                              "#332f8a","#ffffff","#fff4d6")
F = "FuturaStd, Helvetica Neue, Helvetica, Arial, sans-serif"


# ── las marcas de cada ronda, redibujadas para poder compararlas ───────────
def r1_original(ink, bg):
    """El logotipo real del colectivo: cuadrado ámbar, C.F./D.L., doble filete
    con las esquinas sin cerrar."""
    t = NEGRO if bg else ink
    return (f'<rect width="100" height="100" fill="{AMBAR if bg else "none"}"/>'
            f'<path d="M20 5 H95 V95 H5 V5 H11" fill="none" stroke="{t}" '
            f'stroke-width="1.9"/>'
            f'<rect x="10.5" y="10.5" width="79" height="79" fill="none" '
            f'stroke="{t}" stroke-width="1.9"/>'
            f'<path d="M7 64 V95" stroke="{t}" stroke-width="1.9" fill="none"/>'
            f'<text x="51" y="48" text-anchor="middle" fill="{t}" font-family="{F}" '
            f'font-size="35">C.F.</text>'
            f'<text x="51" y="84" text-anchor="middle" fill="{t}" font-family="{F}" '
            f'font-size="35">D.L.</text>')


_CX = _CY = 50; _R, _r, _K = 36, 17, 10
_YO = math.sqrt(_R*_R - _K*_K); _YI = math.sqrt(_r*_r - _K*_K)
def _Cpath():
    return (f"M{_CX+_K} {_CY-_YO:.2f} A{_R} {_R} 0 1 0 {_CX+_K} {_CY+_YO:.2f} "
            f"L{_CX+_K} {_CY+_YI:.2f} A{_r} {_r} 0 1 1 {_CX+_K} {_CY-_YI:.2f} Z")


def r2_brazo(ink, bg):
    """La C a la que se le ha ido el brazo alto."""
    t = NEGRO if bg else ink
    return (f'<rect width="100" height="100" fill="{AMBAR if bg else "none"}"/>'
            f'<path d="M70 36 A26 26 0 1 0 70 64" fill="none" stroke="{t}" '
            f'stroke-width="15"/><rect x="62" y="21" width="26" height="15" fill="{t}"/>')


def r3_registro(ink, bg):
    """Registro corrido: dos planchas, una desplazada."""
    t = NEGRO if bg else ink
    g = HONDO if bg else (AMBAR if t != AMBAR else CREMA)
    o = -4
    return (f'<rect width="100" height="100" fill="{AMBAR if bg else "none"}"/>'
            f'<g transform="translate({o},{o})">'
            f'<path d="{_Cpath()}" fill="{g}" transform="translate(8,8)"/>'
            f'<path d="{_Cpath()}" fill="{t}"/></g>')


def _banda(ink, bg, N, anillos, gr, hu, M=None, margen=0.04, corte_rel=0.55):
    P, N_, M_, g = espiral(N=N, M=M, vueltas=anillos, gr=gr, hu=hu,
                           corte=anillos*(gr+hu) +
                                 (min(N, M or N) - 2*anillos*(gr+hu))*corte_rel)
    m = round(N*margen); CN = N + 2*m
    H = U * ((M or N) + 2*m) / CN
    campo = f'<rect width="100" height="{H:.2f}" fill="{AMBAR}"/>' if bg else ""
    return campo + polilinea(P, CN, g, NEGRO if bg else ink, desplaza=(m, m)), H


def r6_cuadrada(ink, bg):
    """La espiral enrollada hacia dentro: trazo = hueco, hueco central pequeño."""
    c, _ = _banda(ink, bg, 16, 3.5, 1, 1, corte_rel=0.45)
    return c

def r7_hoja_gruesa(ink, bg):
    """La hoja 0.571 con trazo grueso — no funcionaba."""
    c, _ = _banda(ink, bg, 12, 3, 1, 1, M=21, corte_rel=0.45)
    return c

def r10_fina(ink, bg):   c, _ = _banda(ink, bg, 200, 7, 1, 4); return c
def r10_media(ink, bg):  c, _ = _banda(ink, bg, 100, 5, 1, 3); return c
def r10_gruesa(ink, bg): c, _ = _banda(ink, bg, 40, 3, 1, 2);  return c
def r10_hoja(ink, bg):
    c, _ = _banda(ink, bg, 140, 6, 1, 4, M=245); return c


RONDAS = [
  ("original", "el logotipo actual del colectivo", r1_original, 1.0),
  ("r2 · el brazo", "la C a la que se le fue el brazo", r2_brazo, 1.0),
  ("r3 · registro", "dos planchas, una corrida", r3_registro, 1.0),
  ("r6 · espiral cuadrada", "enrollada hacia dentro, trazo = hueco", r6_cuadrada, 1.0),
  ("r7 · hoja gruesa", "0.571 con trazo grueso — falló", r7_hoja_gruesa, 21/12),
  ("r10 · margen fina", "banda fina, 65 % vacío — la actual", r10_fina, 1.0),
  ("r10 · margen media", "5 anillos, 60 % vacío", r10_media, 1.0),
  ("r10 · margen gruesa", "3 anillos, 55 % vacío", r10_gruesa, 1.0),
  ("r10 · hoja fina", "0.571 con banda fina", r10_hoja, 245/140),
]


def solo(fn, ratio, size, ink=NEGRO, bg=True):
    H = 100*ratio
    return (f'<svg viewBox="0 0 100 {H:.1f}" width="{round(size/ratio)}" '
            f'height="{size}">{fn(ink, bg)}</svg>')


from firma import firma as _firma


def junto(fn, ratio, alto=58, ink=NEGRO, bg=True, rel=1.35):
    cuerpo = fn(ink, bg)
    return _firma(cuerpo, ratio, alto, NEGRO if bg else ink,
                  AMBAR if bg else (BLANCO if ink == NEGRO else NEGRO),
                  rel, aire=0.10)


filas = []
for nom, desc, fn, ratio in RONDAS:
    solos = "".join(
      f'<div class="c"><span class="caja {css}">{solo(fn, ratio, s, ink, bg)}</span>'
      f'<div class="et">{et}</div></div>'
      for s, css, ink, bg, et in
      ((104, "b-cuadros", NEGRO, True, "104"),
       (104, "b-blanco", NEGRO, False, "sin campo"),
       (104, "b-negro", AMBAR, False, "en oscuro"),
       (48, "b-cuadros", NEGRO, True, "48"),
       (32, "b-cuadros", NEGRO, True, "32"),
       (20, "b-cuadros", NEGRO, True, "20")))
    juntos = "".join(
      f'<div class="c"><span class="caja {css}">{junto(fn, ratio, 58, ink, bg, rel)}</span>'
      f'<div class="et">{et}</div></div>'
      for css, ink, bg, rel, et in
      (("b-blanco", NEGRO, False, 1.0, "rel 1.0 — la letra se lo come"),
       ("b-blanco", NEGRO, False, 1.35, "rel 1.35 — equilibrado"),
       ("b-blanco", NEGRO, False, 1.6, "rel 1.6 — manda el signo"),
       ("b-negro", AMBAR, False, 1.35, "en oscuro"),
       ("b-cuadros", NEGRO, True, 1.35, "con campo")))
    filas.append(
      f'<section><h2>{nom}<span>{desc}</span></h2>'
      f'<div class="rot">el signo solo</div><div class="fila">{solos}</div>'
      f'<div class="rot">junto a las siglas — <b>la prueba que decide</b></div>'
      f'<div class="fila">{juntos}</div></section>')

print(f'''<!doctype html><meta charset="utf-8"><title>C.F.D.L. — las rondas</title>
<style>
@font-face{{font-family:'FuturaStd';
  src:url('../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');font-display:block}}
*{{box-sizing:border-box}}
body{{margin:0;padding:34px 38px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
h2{{font:400 12px/1 system-ui;letter-spacing:.2em;text-transform:uppercase;color:#ffb923;
   margin:0 0 14px;display:flex;justify-content:space-between;align-items:baseline;gap:20px}}
h2 span{{font:400 11.5px/1.4 system-ui;letter-spacing:0;text-transform:none;
        color:#83839b;text-align:right}}
section{{border-top:1px solid #2a2a38;padding:22px 0 6px}}
.intro{{color:#9a9ab0;max-width:920px;margin:0 0 8px}} .intro b{{color:#e6e6ef;font-weight:500}}
.rot{{font:400 10px/1 system-ui;letter-spacing:.2em;text-transform:uppercase;
     color:#6f6f88;margin:16px 0 10px}} .rot b{{color:#ffb923;font-weight:400}}
.fila{{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end}}
.c{{text-align:center;line-height:0}}
.caja{{display:inline-block;line-height:0;padding:9px}}
.b-blanco{{background:#fff}} .b-negro{{background:#171513}}
.b-cuadros{{background:
  linear-gradient(45deg,#3a3a48 25%,transparent 25%,transparent 75%,#3a3a48 75%),
  linear-gradient(45deg,#3a3a48 25%,#2a2a34 25%,#2a2a34 75%,#3a3a48 75%);
  background-size:14px 14px;background-position:0 0,7px 7px}}
.et{{font:400 10px/1.3 system-ui;color:#6f6f88;margin-top:7px}}
</style>
<h1>C.F.D.L. — las rondas</h1>
<p class="intro">Un signo puede ser bonito solo y no servir. Lo que decide es cómo
se comporta <b>junto a las siglas</b>: si el peso óptico casa con el de la letra, si
la altura está bien puesta, si se acompañan o compiten.<br>
Cada ronda, sola y en firma, sobre blanco y sobre negro. Las tres primeras
casillas mueven <b>rel</b> —la altura del signo dividida por la altura de
mayúscula— y enseñan lo de siempre: <b>un signo de línea fina al lado de una
versaleta maciza se queda sin voz</b>. A 1.0 la letra se lo come; 1.35 equilibra.
<br>Las medidas de la firma salen del OTF, no de una estimación: altura de
mayúscula <b>0,754 em</b> y ancho de «C.F.D.L.» <b>3,48 em</b>. Estimarlas a ojo
—0,70 y 4,06— sacaba las mayúsculas de la caja y recortaba la firma a «C.F.D».</p>
{"".join(filas)}
''')
