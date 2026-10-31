#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — bocetos de logotipo. Exploración, no producción.

Genera una hoja con varias propuestas, cada una a los tamaños en que el
logotipo va a vivir de verdad: grande, recortado en círculo (la foto de perfil
de Instagram), 48 px (pie de cartel) y 32 px (favicon).

No toca nada del módulo. `python3 bocetos.py > hoja.html`
"""
AMBAR = "#ffb923"
TINTA = "#171513"

F = "FuturaStd, Helvetica, Arial"


def campo(on, c=AMBAR):
    return f'<rect width="100" height="100" fill="{c}"/>' if on else ""


# ── A · lockup desplazado ──────────────────────────────────────────────────
def A(bg=True, ink=TINTA):
    return (campo(bg) +
      f'<text x="12" y="46" font-family="{F}" font-size="31" fill="{ink}">C.F.</text>'
      f'<text x="34" y="84" font-family="{F}" font-size="31" fill="{ink}">D.L.</text>')

# ── B · el bloque se fuga del campo ────────────────────────────────────────
def B(bg=True, ink=TINTA):
    return (campo(bg) +
      f'<text x="30" y="52" font-family="{F}" font-size="48" fill="{ink}">C.F.</text>'
      f'<text x="8" y="97" font-family="{F}" font-size="48" fill="{ink}">D.L.</text>')

# ── C · wordmark en una línea ──────────────────────────────────────────────
def C(bg=True, ink=TINTA):
    return (campo(bg) +
      f'<text x="50" y="59" text-anchor="middle" font-family="{F}" '
      f'font-size="26" fill="{ink}">C.F.D.L.</text>')

# ── D · el acordeón del manifiesto ─────────────────────────────────────────
def D(bg=True, ink=TINTA):
    z = "M10 30 L26 16 L42 30 L58 16 L74 30 L90 16"
    return (campo(bg) +
      f'<path d="{z}" fill="none" stroke="{ink}" stroke-width="7" '
      f'stroke-linejoin="miter"/>'
      f'<path d="{z}" fill="none" stroke="{ink}" stroke-width="7" '
      f'transform="translate(0,22)"/>'
      f'<text x="50" y="88" text-anchor="middle" font-family="{F}" '
      f'font-size="17" fill="{ink}">C.F.D.L.</text>')

# ── E · la C plegada — sin letra legible, sobrevive a 16 px ────────────────
def E(bg=True, ink=TINTA):
    c = ("M78 22 L50 12 L22 30 L22 70 L50 88 L78 78 "
         "L78 66 L54 74 L34 62 L34 38 L54 26 L78 34 Z")
    return campo(bg) + f'<path d="{c}" fill="{ink}"/>'

# ── F · la C fuera de lugar: el brazo alto, corrido ────────────────────────
def F_(bg=True, ink=TINTA):
    return (campo(bg) +
      f'<path d="M70 36 A26 26 0 1 0 70 64" fill="none" stroke="{ink}" '
      f'stroke-width="15" stroke-linecap="butt"/>'
      f'<rect x="62" y="21" width="26" height="15" fill="{ink}"/>')

# ── G · cuatro puntos, uno fuera de sitio ──────────────────────────────────
def G(bg=True, ink=TINTA):
    p = [(32, 32), (68, 32), (32, 68)]
    d = "".join(f'<circle cx="{x}" cy="{y}" r="11" fill="{ink}"/>' for x, y in p)
    return campo(bg) + d + f'<circle cx="82" cy="82" r="11" fill="{ink}"/>'

# ── H · dos piezas: monograma para lo pequeño, lockup para lo grande ───────
def H(bg=True, ink=TINTA):
    return (campo(bg) +
      f'<path d="M72 30 L50 22 L28 36 L28 64 L50 78 L72 70 L72 60 L53 66 '
      f'L38 57 L38 43 L53 34 L72 40 Z" fill="{ink}"/>')


PROP = [
 ("A", "lockup desplazado", "la fila de abajo no comparte eje con la de arriba", A),
 ("B", "el bloque se fuga",  "la letra se sale del campo y el borde la corta",    B),
 ("C", "wordmark",           "una línea; el campo ámbar pasa a ser opcional",     C),
 ("D", "acordeón",           "el manifiesto plegado, sobre las siglas",           D),
 ("E", "la C plegada",       "sin letra legible — aguanta a 16 px",               E),
 ("F", "la C fuera de lugar","el brazo alto, corrido fuera de la curva",          F_),
 ("G", "cuatro puntos",      "los cuatro puntos de C.F.D.L.; uno, descolocado",   G),
 ("H", "monograma",          "pieza pequeña de un sistema de dos",                H),
]

def svg(fn, size, bg, ink, extra=""):
    return (f'<svg viewBox="0 0 100 100" width="{size}" height="{size}" {extra}>'
            f'{fn(bg, ink)}</svg>')

print(f'''<!doctype html><meta charset="utf-8">
<title>C.F.D.L. — bocetos de logotipo</title>
<style>
@font-face{{font-family:'FuturaStd';
  src:url('../../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');
  font-display:block}}
*{{box-sizing:border-box}}
body{{margin:0;padding:34px 38px;background:#13131a;color:#e6e6ef;
     font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
.intro{{color:#9a9ab0;max-width:880px;margin:0 0 30px}}
.intro b{{color:#e6e6ef;font-weight:500}}
table{{border-collapse:collapse;width:100%}}
th{{font:400 10px/1 system-ui;letter-spacing:.18em;text-transform:uppercase;
   color:#6f6f88;padding:0 10px 12px;text-align:center;font-weight:400}}
th.l{{text-align:left}}
td{{padding:14px 10px;border-top:1px solid #2a2a38;text-align:center;vertical-align:middle}}
td.l{{text-align:left;width:190px}}
.k{{font:400 20px/1 system-ui;color:#ffb923}}
.n{{font-size:13px;color:#e6e6ef;margin-top:5px}}
.d{{font-size:12px;color:#83839b;margin-top:3px;line-height:1.45}}
.claro{{background:#f8ccce;padding:9px;display:inline-block;line-height:0}}
.oscuro{{background:#171513;padding:9px;display:inline-block;line-height:0}}
.circ{{border-radius:50%;overflow:hidden;display:inline-block;line-height:0;
      background:{AMBAR}}}
.mini{{background:#fff;display:inline-block;line-height:0;padding:3px}}
</style>
<h1>C.F.D.L. — bocetos de logotipo</h1>
<p class="intro">Ocho propuestas, cada una a los tamaños en que el logotipo vive
de verdad. Las dos columnas que deciden son <b>círculo 110&nbsp;px</b> (la foto de
perfil de Instagram, que recorta las esquinas) y <b>32&nbsp;px</b> (favicon).
A 32&nbsp;px cuatro letras y cuatro puntos se empastan: por eso hay propuestas
sin letra legible.<br>Exploración, no producción — el módulo sigue usando el
logotipo actual.</p>
<table>
<tr><th class="l">propuesta</th><th>color</th><th>una tinta</th>
<th>en oscuro</th><th>círculo 110</th><th>48 px</th><th>32 px</th><th>16 px</th></tr>''')

for k, nombre, desc, fn in PROP:
    print(f'''<tr>
<td class="l"><span class="k">{k}</span><div class="n">{nombre}</div>
  <div class="d">{desc}</div></td>
<td>{svg(fn,104,True,TINTA)}</td>
<td><span class="claro">{svg(fn,104,False,"#332f8a")}</span></td>
<td><span class="oscuro">{svg(fn,104,False,AMBAR)}</span></td>
<td><span class="circ">{svg(fn,110,True,TINTA)}</span></td>
<td>{svg(fn,48,True,TINTA)}</td>
<td>{svg(fn,32,True,TINTA)}</td>
<td><span class="mini">{svg(fn,16,True,TINTA)}</span></td>
</tr>''')
print('</table>')
