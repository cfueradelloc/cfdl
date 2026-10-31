#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — ronda 5: la espiral, afinada.

Correcciones sobre la ronda 4:
  · el arranque exterior queda a ras de la esquina, sin el rabito suelto
  · el remate interior es el único gesto abierto, y se controla
  · centrado óptico: la espiral hacia dentro carga su masa a un lado
  · la variante «C» abre por el costado derecho, a media altura, que es donde
    el ojo espera la boca de una C
"""
AMBAR, NEGRO, ZAFIRO, BLANCO, HONDO = "#ffb923","#171513","#332f8a","#ffffff","#c07d00"
W = 100


def pts_espiral(vueltas, w, g, alto=W, corte=1.0, boca=0.0):
    """Espiral rectangular hacia dentro.

    corte  fracción de la ÚLTIMA recta que se dibuja (1 = entera)
    boca   hueco a media altura del costado derecho, en unidades: la C
    """
    p, o = w + g, w / 2
    l, t, r, b = o, o, W - o, alto - o
    P = []
    if boca:
        # arranca a media altura del lado derecho y sube: la boca queda abierta
        P.append((r, alto / 2 - boca / 2))
        P.append((r, t))
        orden = [2, 3, 0, 1]
    else:
        P.append((l, t))
        orden = [0, 1, 2, 3]
    n = int(vueltas * 4)
    for k in range(n):
        lado = orden[k % 4]
        if r - l < p * 0.6 or b - t < p * 0.6:
            break
        ult = (k == n - 1)
        f = corte if ult else 1.0
        if lado == 0:      P.append((l + (r - l) * f, t))
        elif lado == 1:    P.append((r, t + (b - t) * f))
        elif lado == 2:
            P.append((r - (r - l) * f, b)); t += p
        else:
            P.append((l, b - (b - t) * f)); l += p; r -= p; b -= p
    return P


def d(P):
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in P)


def centrado(P, alto=W):
    """Devuelve el desplazamiento que centra ópticamente el dibujo."""
    xs = [x for x, _ in P]; ys = [y for _, y in P]
    cx = (min(xs) + max(xs)) / 2; cy = (min(ys) + max(ys)) / 2
    return (W / 2 - cx, alto / 2 - cy)


def pieza(vueltas, w, g, corte=1.0, boca=0.0, alto=W, bg=True, ink=NEGRO,
          fantasma=None):
    P = pts_espiral(vueltas, w, g, alto, corte, boca)
    dx, dy = centrado(P, alto)
    campo = f'<rect width="{W}" height="{alto}" fill="{AMBAR}"/>' if bg else ""
    gh = ""
    if fantasma:
        gh = (f'<polyline points="{d(P)}" fill="none" stroke="{fantasma}" '
              f'stroke-width="{w}" stroke-linejoin="miter" stroke-linecap="butt" '
              f'transform="translate({dx+6:.2f},{dy+6:.2f})"/>')
    return (campo + gh +
            f'<polyline points="{d(P)}" fill="none" stroke="{ink}" stroke-width="{w}" '
            f'stroke-linejoin="miter" stroke-linecap="butt" '
            f'transform="translate({dx:.2f},{dy:.2f})"/>')


A = lambda bg=True, ink=NEGRO: pieza(3.5, 6.5, 7.5, bg=bg, ink=ink)
B = lambda bg=True, ink=NEGRO: pieza(3.5, 6.5, 7.5, corte=0.45, bg=bg, ink=ink)
C = lambda bg=True, ink=NEGRO: pieza(2.5, 10, 10, bg=bg, ink=ink)
D = lambda bg=True, ink=NEGRO: pieza(2.0, 13, 12, bg=bg, ink=ink)
E = lambda bg=True, ink=NEGRO: pieza(2.5, 10, 10, boca=26, bg=bg, ink=ink)
F = lambda bg=True, ink=NEGRO: pieza(3.5, 6.5, 7.5, corte=0.45, bg=bg, ink=ink,
                                     fantasma=HONDO if bg else AMBAR)

PROP = [("A","3½ vueltas","la densidad de la hoja impresa",A),
        ("B","3½ + remate cortado","el gesto abierto del manifiesto",B),
        ("C","2½ vueltas","misma idea, más cuerpo",C),
        ("D","2 vueltas","para lo diminuto",D),
        ("E","boca a la derecha","la espiral leída como C",E),
        ("F","B + fuera de registro","espiral y plancha corrida",F)]

def svg(fn,s,bg,ink): return f'<svg viewBox="0 0 100 100" width="{s}" height="{s}">{fn(bg,ink)}</svg>'

print(f'''<!doctype html><meta charset="utf-8"><title>espiral afinada</title><style>
*{{box-sizing:border-box}}body{{margin:0;padding:30px 34px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
.intro{{color:#9a9ab0;max-width:880px;margin:0 0 20px}} .intro b{{color:#e6e6ef;font-weight:500}}
table{{border-collapse:collapse;width:100%}}
th{{font:400 10px/1 system-ui;letter-spacing:.18em;text-transform:uppercase;color:#6f6f88;padding:0 10px 12px;text-align:center;font-weight:400}}
th.l{{text-align:left}} td{{padding:14px 10px;border-top:1px solid #2a2a38;text-align:center;vertical-align:middle}}
td.l{{text-align:left;width:176px}} .k{{font:400 19px/1 system-ui;color:#ffb923}}
.n{{font-size:13px;margin-top:4px}} .d{{font-size:11.5px;color:#83839b;margin-top:2px;line-height:1.4}}
.claro{{background:#f8ccce;padding:8px;display:inline-block;line-height:0}}
.oscuro{{background:#171513;padding:8px;display:inline-block;line-height:0}}
.circ{{border-radius:50%;overflow:hidden;display:inline-block;line-height:0;background:#ffb923}}
.mini{{background:#fff;display:inline-block;line-height:0;padding:3px}}
</style>
<h1>C.F.D.L. — la espiral, afinada</h1>
<p class="intro">Arranque a ras de esquina (fuera el rabito suelto), remate interior
controlado, y <b>centrado óptico</b> — una espiral hacia dentro carga su masa a un
lado y sin corregirlo el avatar se ve descolgado.</p>
<table><tr><th class="l"></th><th>color</th><th>una tinta</th><th>en oscuro</th>
<th>círculo</th><th>48</th><th>32</th><th>16</th></tr>''')
for k,n,dd,fn in PROP:
    print(f'''<tr><td class="l"><span class="k">{k}</span><div class="n">{n}</div><div class="d">{dd}</div></td>
<td>{svg(fn,104,True,NEGRO)}</td><td><span class="claro">{svg(fn,104,False,ZAFIRO)}</span></td>
<td><span class="oscuro">{svg(fn,104,False,AMBAR)}</span></td>
<td><span class="circ">{svg(fn,108,True,NEGRO)}</span></td>
<td>{svg(fn,48,True,NEGRO)}</td><td>{svg(fn,32,True,NEGRO)}</td>
<td><span class="mini">{svg(fn,16,True,NEGRO)}</span></td></tr>''')
print("</table>")
