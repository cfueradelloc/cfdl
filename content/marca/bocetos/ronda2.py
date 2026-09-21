#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — logotipo, segunda ronda.

La primera ronda era un arco con un rectángulo al lado: dos primitivas
compartiendo lienzo, sin sistema y sin relación entre ellas. Esta parte de tres
correcciones:

  · la pieza que falta y la pieza que se ha movido son LA MISMA, dibujada una
    sola vez. Así el ojo reconoce que eso estaba ahí.
  · los remates se cortan en vertical, sobre el eje, no perpendiculares al
    arco. Es lo que hace que una marca geométrica parezca dibujada y no
    recortada.
  · todo sale de un módulo y un grosor únicos.

Y un concepto nuevo: el colectivo IMPRIME. Un registro corrido —dos planchas y
una que se desplaza— es literalmente algo fuera de lugar, es propio de su
medio, y regala la versión a dos tintas.
"""
import math

AMBAR, NEGRO, ZAFIRO, BLANCO = "#ffb923", "#171513", "#332f8a", "#ffffff"
F = "FuturaStd, Helvetica, Arial"

# ── sistema ────────────────────────────────────────────────────────────────
CX = CY = 50          # centro
R, r = 36, 17         # radios exterior e interior → grosor 19
K = 10                # la boca: corte vertical a 10 del eje
YO = math.sqrt(R*R - K*K)
YI = math.sqrt(r*r - K*K)


def _c(cx=CX, cy=CY):
    """La C: anillo con la boca cortada en vertical."""
    return (f"M{cx+K} {cy-YO} A{R} {R} 0 1 0 {cx+K} {cy+YO} "
            f"L{cx+K} {cy+YI} A{r} {r} 0 1 1 {cx+K} {cy-YI} Z")


def _pieza(cx=CX, cy=CY):
    """La pieza que falta — exactamente el hueco de la C, como forma propia."""
    return (f"M{cx+K} {cy-YO} A{R} {R} 0 0 1 {cx+K} {cy+YO} "
            f"L{cx+K} {cy+YI} A{r} {r} 0 0 0 {cx+K} {cy-YI} Z")


def campo(on, c=AMBAR):
    return f'<rect width="100" height="100" fill="{c}"/>' if on else ""


# 1 · el anillo partido: la pieza se ha ido, y se ve de dónde
def P1(bg=True, ink=NEGRO):
    return (campo(bg) +
      f'<path d="{_c()}" fill="{ink}"/>'
      f'<path d="{_pieza()}" fill="{ink}" transform="translate(16,-24)"/>')

# 2 · la misma, con la pieza girada: se fue y volvió mal
def P2(bg=True, ink=NEGRO):
    return (campo(bg) +
      f'<path d="{_c()}" fill="{ink}"/>'
      f'<path d="{_pieza()}" fill="{ink}" '
      f'transform="translate(70,84) rotate(180) translate(-50,-50)"/>')

# 3 · registro corrido: dos planchas, una desplazada
def P3(bg=True, ink=NEGRO, plancha=None):
    p2 = plancha or (AMBAR if ink == NEGRO else AMBAR)
    return (campo(bg, NEGRO if bg and ink != NEGRO else AMBAR) if bg else "") + (
      f'<path d="{_c()}" fill="{p2}" transform="translate(7,7)"/>'
      f'<path d="{_c()}" fill="{ink}"/>')

# 4 · registro corrido a una tinta: la plancha desplazada queda en contorno
def P4(bg=True, ink=NEGRO):
    return (campo(bg) +
      f'<path d="{_c()}" fill="none" stroke="{ink}" stroke-width="2.5" '
      f'transform="translate(8,8)"/>'
      f'<path d="{_c()}" fill="{ink}"/>')

# 5 · la C plegada, con facetas iguales
def P5(bg=True, ink=NEGRO):
    pts_o, pts_i = [], []
    for i in range(7):                      # 7 vértices de -140° a +140°
        a = math.radians(-140 + i * (280/6))
        pts_o.append((CX + R*math.cos(a), CY + R*math.sin(a)))
    for i in range(6, -1, -1):
        a = math.radians(-140 + i * (280/6))
        pts_i.append((CX + r*math.cos(a), CY + r*math.sin(a)))
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts_o + pts_i) + " Z"
    return campo(bg) + f'<path d="{d}" fill="{ink}"/>'

# 6 · siglas con registro corrido
def P6(bg=True, ink=NEGRO):
    t = (f'<text x="14" y="50" font-family="{F}" font-size="40">C.F.</text>'
         f'<text x="14" y="88" font-family="{F}" font-size="40">D.L.</text>')
    return (campo(bg) +
      f'<g fill="{BLANCO if bg else AMBAR}" transform="translate(6,6)">{t}</g>'
      f'<g fill="{ink}">{t}</g>')

# 7 · el hueco es la marca: sólo la pieza, sin la C
def P7(bg=True, ink=NEGRO):
    return (campo(bg) +
      f'<path d="{_pieza()}" fill="{ink}" transform="translate(4,0)"/>'
      f'<path d="{_pieza()}" fill="{ink}" opacity="0.28" '
      f'transform="translate(-28,0)"/>')

# 8 · C sólida, la boca desplazada hacia dentro
def P8(bg=True, ink=NEGRO):
    return (campo(bg) +
      f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="{ink}"/>'
      f'<circle cx="{CX+9}" cy="{CY-7}" r="{r}" fill="{AMBAR if bg else BLANCO}"/>'
      f'<rect x="{CX+K}" y="{CY-YI-7}" width="40" height="{2*YI}" '
      f'fill="{AMBAR if bg else BLANCO}"/>')


PROP = [
 ("1", "anillo partido", "la pieza que falta es la que se ha ido", P1),
 ("2", "vuelta del revés", "la misma pieza, girada 180°", P2),
 ("3", "registro corrido", "dos planchas, una desplazada — a dos tintas", P3),
 ("4", "registro, una tinta", "la plancha desplazada queda en contorno", P4),
 ("5", "C plegada", "facetas iguales, como el acordeón impreso", P5),
 ("6", "siglas descuadradas", "el registro corrido aplicado a las letras", P6),
 ("7", "sólo el hueco", "la pieza sola; la C se intuye por su ausencia", P7),
 ("8", "boca desplazada", "C sólida cuyo contrapunzón se ha corrido", P8),
]

def svg(fn, size, bg, ink):
    return (f'<svg viewBox="0 0 100 100" width="{size}" height="{size}">'
            f'{fn(bg, ink)}</svg>')

print(f'''<!doctype html><meta charset="utf-8"><title>C.F.D.L. — ronda 2</title>
<style>
@font-face{{font-family:'FuturaStd';
  src:url('../../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');
  font-display:block}}
*{{box-sizing:border-box}}
body{{margin:0;padding:32px 36px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
.intro{{color:#9a9ab0;max-width:900px;margin:0 0 26px}}
.intro b{{color:#e6e6ef;font-weight:500}}
table{{border-collapse:collapse;width:100%}}
th{{font:400 10px/1 system-ui;letter-spacing:.18em;text-transform:uppercase;
   color:#6f6f88;padding:0 10px 12px;text-align:center;font-weight:400}}
th.l{{text-align:left}}
td{{padding:13px 10px;border-top:1px solid #2a2a38;text-align:center;vertical-align:middle}}
td.l{{text-align:left;width:184px}}
.k{{font:400 19px/1 system-ui;color:#ffb923}}
.n{{font-size:13px;margin-top:4px}}
.d{{font-size:11.5px;color:#83839b;margin-top:2px;line-height:1.4}}
.claro{{background:#f8ccce;padding:8px;display:inline-block;line-height:0}}
.oscuro{{background:#171513;padding:8px;display:inline-block;line-height:0}}
.circ{{border-radius:50%;overflow:hidden;display:inline-block;line-height:0;background:#ffb923}}
.mini{{background:#fff;display:inline-block;line-height:0;padding:3px}}
</style>
<h1>C.F.D.L. — logotipo, ronda 2</h1>
<p class="intro">La ronda anterior eran primitivas sueltas. Estas salen todas del
mismo sistema —un centro, dos radios, un grosor— y la <b>pieza que falta es la
misma que se ha movido</b>, dibujada una vez. Los remates se cortan en vertical,
sobre el eje.<br>Las tres últimas columnas mandan: <b>círculo</b> (foto de perfil),
<b>32&nbsp;px</b> (favicon) y <b>16&nbsp;px</b>.</p>
<table><tr><th class="l">propuesta</th><th>color</th><th>una tinta</th>
<th>en oscuro</th><th>círculo</th><th>48</th><th>32</th><th>16</th></tr>''')

for k, n, d, fn in PROP:
    print(f'''<tr><td class="l"><span class="k">{k}</span><div class="n">{n}</div>
<div class="d">{d}</div></td>
<td>{svg(fn,100,True,NEGRO)}</td>
<td><span class="claro">{svg(fn,100,False,ZAFIRO)}</span></td>
<td><span class="oscuro">{svg(fn,100,False,AMBAR)}</span></td>
<td><span class="circ">{svg(fn,104,True,NEGRO)}</span></td>
<td>{svg(fn,48,True,NEGRO)}</td>
<td>{svg(fn,32,True,NEGRO)}</td>
<td><span class="mini">{svg(fn,16,True,NEGRO)}</span></td></tr>''')
print("</table>")
