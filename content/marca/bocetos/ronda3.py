#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — finalistas. Corregidos los fallos de la ronda 2."""
import math
AMBAR, NEGRO, ZAFIRO, BLANCO, CREMA = "#ffb923", "#171513", "#332f8a", "#ffffff", "#fff4d6"
AMBAR_HONDO = "#c07d00"
F = "FuturaStd, Helvetica, Arial"

CX = CY = 50
R, r, K = 36, 17, 10
YO = math.sqrt(R*R - K*K); YI = math.sqrt(r*r - K*K)

def _c(): return (f"M{CX+K} {CY-YO} A{R} {R} 0 1 0 {CX+K} {CY+YO} "
                  f"L{CX+K} {CY+YI} A{r} {r} 0 1 1 {CX+K} {CY-YI} Z")
def _pieza(): return (f"M{CX+K} {CY-YO} A{R} {R} 0 0 1 {CX+K} {CY+YO} "
                      f"L{CX+K} {CY+YI} A{r} {r} 0 0 0 {CX+K} {CY-YI} Z")
def campo(on, c=AMBAR): return f'<rect width="100" height="100" fill="{c}"/>' if on else ""

# A · vuelta del revés — la pieza regresa girada y no encaja
def A(bg=True, ink=NEGRO):
    return (campo(bg) + f'<path d="{_c()}" fill="{ink}"/>'
      f'<path d="{_pieza()}" fill="{ink}" '
      f'transform="translate(72,86) rotate(180) translate(-50,-50)"/>')

# B · registro corrido a dos tintas — el fantasma ya no se pierde sobre ámbar
def B(bg=True, ink=NEGRO):
    ghost = AMBAR_HONDO if bg else (AMBAR if ink != AMBAR else CREMA)
    return (campo(bg) +
      f'<path d="{_c()}" fill="{ghost}" transform="translate(8,8)"/>'
      f'<path d="{_c()}" fill="{ink}"/>')

# C · registro a una tinta — la plancha desplazada, en contorno
def C(bg=True, ink=NEGRO):
    return (campo(bg) +
      f'<path d="{_c()}" fill="none" stroke="{ink}" stroke-width="2.5" '
      f'transform="translate(9,9)"/>'
      f'<path d="{_c()}" fill="{ink}"/>')

# D · boca desplazada — con el contrapunzón recortado dentro del disco
def D(bg=True, ink=NEGRO):
    hueco = AMBAR if bg else BLANCO
    return (campo(bg) +
      f'<defs><clipPath id="disco"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath></defs>'
      f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="{ink}"/>'
      f'<g clip-path="url(#disco)" fill="{hueco}">'
      f'<circle cx="{CX+8}" cy="{CY-6}" r="{r}"/>'
      f'<rect x="{CX+8}" y="{CY-6-YI}" width="40" height="{2*YI}"/></g>')

# E · C plegada, con el doble de facetas y la boca más cerrada
def E(bg=True, ink=NEGRO):
    n, ext = 12, 150
    o = [(CX + R*math.cos(math.radians(-ext + i*(2*ext/n))),
          CY + R*math.sin(math.radians(-ext + i*(2*ext/n)))) for i in range(n+1)]
    i_ = [(CX + r*math.cos(math.radians(-ext + i*(2*ext/n))),
           CY + r*math.sin(math.radians(-ext + i*(2*ext/n)))) for i in range(n, -1, -1)]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in o + i_) + " Z"
    return campo(bg) + f'<path d="{d}" fill="{ink}"/>'

# ── lockups, para comparar pareja ──────────────────────────────────────────
def L_registro(bg=True, ink=NEGRO):
    t = (f'<text x="13" y="49" font-family="{F}" font-size="41">C.F.</text>'
         f'<text x="13" y="88" font-family="{F}" font-size="41">D.L.</text>')
    ghost = AMBAR_HONDO if bg else (AMBAR if ink != AMBAR else CREMA)
    return (campo(bg) + f'<g fill="{ghost}" transform="translate(7,7)">{t}</g>'
            f'<g fill="{ink}">{t}</g>')

def L_fuga(bg=True, ink=NEGRO):
    return (campo(bg) +
      f'<text x="30" y="52" font-family="{F}" font-size="48" fill="{ink}">C.F.</text>'
      f'<text x="8" y="97" font-family="{F}" font-size="48" fill="{ink}">D.L.</text>')

MONO = [("A","vuelta del revés","la pieza regresa girada y no encaja",A),
        ("B","registro · dos tintas","la plancha de atrás, corrida",B),
        ("C","registro · una tinta","la plancha corrida queda en contorno",C),
        ("D","boca desplazada","el contrapunzón se ha corrido",D),
        ("E","C plegada","doce facetas, boca cerrada",E)]
LOCK = [("L1","siglas · registro corrido","mismo mecanismo que B y C",L_registro),
        ("L2","siglas · se fugan del campo","el borde las corta",L_fuga)]

def svg(fn,s,bg,ink): return f'<svg viewBox="0 0 100 100" width="{s}" height="{s}">{fn(bg,ink)}</svg>'

print(f'''<!doctype html><meta charset="utf-8"><title>C.F.D.L. — finalistas</title><style>
@font-face{{font-family:'FuturaStd';src:url('../../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');font-display:block}}
*{{box-sizing:border-box}}body{{margin:0;padding:32px 36px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
h2{{font:400 11px/1 system-ui;letter-spacing:.2em;text-transform:uppercase;color:#6f6f88;margin:30px 0 4px}}
.intro{{color:#9a9ab0;max-width:900px;margin:0 0 6px}} .intro b{{color:#e6e6ef;font-weight:500}}
table{{border-collapse:collapse;width:100%}}
th{{font:400 10px/1 system-ui;letter-spacing:.18em;text-transform:uppercase;color:#6f6f88;padding:10px 10px 12px;text-align:center;font-weight:400}}
th.l{{text-align:left}} td{{padding:14px 10px;border-top:1px solid #2a2a38;text-align:center;vertical-align:middle}}
td.l{{text-align:left;width:186px}} .k{{font:400 19px/1 system-ui;color:#ffb923}}
.n{{font-size:13px;margin-top:4px}} .d{{font-size:11.5px;color:#83839b;margin-top:2px;line-height:1.4}}
.claro{{background:#f8ccce;padding:8px;display:inline-block;line-height:0}}
.oscuro{{background:#171513;padding:8px;display:inline-block;line-height:0}}
.circ{{border-radius:50%;overflow:hidden;display:inline-block;line-height:0;background:#ffb923}}
.mini{{background:#fff;display:inline-block;line-height:0;padding:3px}}
</style>
<h1>C.F.D.L. — finalistas</h1>
<p class="intro">Corregido lo que fallaba: el fantasma ya no se pierde sobre el campo
ámbar, el contrapunzón va recortado dentro del disco, y la C plegada tiene doce
facetas en vez de seis.</p>
<h2>monograma — para el círculo, el favicon y el pie</h2>
<table><tr><th class="l"></th><th>color</th><th>una tinta</th><th>en oscuro</th>
<th>círculo</th><th>48</th><th>32</th><th>16</th></tr>''')
for k,n,d,fn in MONO:
    print(f'''<tr><td class="l"><span class="k">{k}</span><div class="n">{n}</div><div class="d">{d}</div></td>
<td>{svg(fn,104,True,NEGRO)}</td><td><span class="claro">{svg(fn,104,False,ZAFIRO)}</span></td>
<td><span class="oscuro">{svg(fn,104,False,AMBAR)}</span></td>
<td><span class="circ">{svg(fn,108,True,NEGRO)}</span></td>
<td>{svg(fn,48,True,NEGRO)}</td><td>{svg(fn,32,True,NEGRO)}</td>
<td><span class="mini">{svg(fn,16,True,NEGRO)}</span></td></tr>''')
print('</table><h2>lockup — para donde hay sitio</h2><table>'
      '<tr><th class="l"></th><th>color</th><th>una tinta</th><th>en oscuro</th>'
      '<th>96</th><th>64</th><th>48 — el límite</th></tr>')
for k,n,d,fn in LOCK:
    print(f'''<tr><td class="l"><span class="k">{k}</span><div class="n">{n}</div><div class="d">{d}</div></td>
<td>{svg(fn,104,True,NEGRO)}</td><td><span class="claro">{svg(fn,104,False,ZAFIRO)}</span></td>
<td><span class="oscuro">{svg(fn,104,False,AMBAR)}</span></td>
<td>{svg(fn,96,True,NEGRO)}</td><td>{svg(fn,64,True,NEGRO)}</td>
<td>{svg(fn,48,True,NEGRO)}</td></tr>''')
print("</table>")
