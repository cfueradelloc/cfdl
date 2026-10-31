#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — ronda 4: la espiral del manifiesto.

El manifiesto impreso compone su texto como una ESPIRAL RECTANGULAR: rectángulos
encajados que giran hacia dentro, y la vuelta interior cortada a media altura.
No cierra nunca — «cambiante y nunca cumplido».

Aquí se estiliza para que sirva de marca. Siete anillos se empastan a 32 px, así
que la pregunta de oficio es cuántas vueltas bastan para que siga leyéndose como
espiral. Y hay una idea dentro: una espiral cuadrada con la vuelta exterior
abierta SE LEE COMO UNA C.
"""
import math
AMBAR, NEGRO, ZAFIRO, BLANCO, CREMA, HONDO = ("#ffb923","#171513","#332f8a",
                                              "#ffffff","#fff4d6","#c07d00")
W = 100


def espiral(vueltas=2.5, w=9, g=9, corte=0.0, abierta=0.0, alto=W):
    """Polilínea de espiral rectangular hacia dentro.

    vueltas  cuántas da
    w,g      grosor de trazo y hueco entre vueltas (iguales = máxima vibración)
    corte    fracción de la última recta que se dibuja (el remate cortado del
             manifiesto). 0 = completa.
    abierta  hueco que se deja en el arranque, en unidades — es lo que convierte
             la espiral en una C.
    """
    p = w + g
    o = w / 2
    l, t, r, b = o, o, W - o, alto - o
    pts = [(l + abierta, t)]
    n = int(vueltas * 4)
    for k in range(n):
        lado = k % 4
        if r - l < p * 0.5 or b - t < p * 0.5:
            break
        ultimo = (k == n - 1)
        if lado == 0:                       # arriba, hacia la derecha
            x = r if not (ultimo and corte) else l + (r - l) * corte
            pts.append((x, t))
        elif lado == 1:                     # derecha, hacia abajo
            y = b if not (ultimo and corte) else t + (b - t) * corte
            pts.append((r, y)); 
        elif lado == 2:                     # abajo, hacia la izquierda
            x = l if not (ultimo and corte) else r - (r - l) * corte
            pts.append((x, b))
            t += p
        else:                               # izquierda, hacia arriba
            y = t if not (ultimo and corte) else b - (b - t) * corte
            pts.append((l, y))
            l += p; r -= p; b -= p
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def marco(on, c=AMBAR, alto=W):
    return f'<rect width="{W}" height="{alto}" fill="{c}"/>' if on else ""


def trazo(d, ink, w, alto=W, extra=""):
    return (f'<polyline points="{d}" fill="none" stroke="{ink}" stroke-width="{w}" '
            f'stroke-linejoin="miter" stroke-linecap="butt" {extra}/>')


# 1 · dos vueltas y media, trazo = hueco
def P1(bg=True, ink=NEGRO):
    return marco(bg) + trazo(espiral(2.5, 9, 9), ink, 9)

# 2 · dos vueltas, trazo más grueso — para lo pequeño
def P2(bg=True, ink=NEGRO):
    return marco(bg) + trazo(espiral(2.0, 13, 11), ink, 13)

# 3 · tres vueltas y media, fina — la densidad del manifiesto
def P3(bg=True, ink=NEGRO):
    return marco(bg) + trazo(espiral(3.5, 6, 7), ink, 6)

# 4 · abierta a la izquierda: la espiral leída como C
def P4(bg=True, ink=NEGRO):
    return marco(bg) + trazo(espiral(2.5, 11, 10, abierta=34), ink, 11)

# 5 · con el remate interior cortado, como la hoja impresa
def P5(bg=True, ink=NEGRO):
    return marco(bg) + trazo(espiral(2.75, 10, 10, corte=0.45), ink, 10)

# 6 · una vuelta fuera de registro
def P6(bg=True, ink=NEGRO):
    g = HONDO if bg else AMBAR
    return (marco(bg) +
      trazo(espiral(2.5, 9, 9), g, 9, extra='transform="translate(7,7)"') +
      trazo(espiral(2.5, 9, 9), ink, 9))

# 7 · proporción del manifiesto (0.571) — la pieza vertical
def P7(bg=True, ink=NEGRO):
    alto = round(W / 0.571)
    return (f'<svg viewBox="0 0 {W} {alto}" width="60" height="{round(60*alto/W)}">'
            + marco(bg, AMBAR, alto)
            + trazo(espiral(3.5, 7, 8, corte=0.4, alto=alto), ink, 7, alto) + '</svg>')

# 8 · maciza: bandas alternas en vez de líneas
def P8(bg=True, ink=NEGRO):
    return marco(bg) + trazo(espiral(2.0, 15, 9), ink, 15)


PROP = [("1","2½ vueltas","trazo = hueco; máxima vibración",P1),
        ("2","2 vueltas, grueso","menos vueltas, más cuerpo",P2),
        ("3","3½ vueltas, fina","la densidad de la hoja impresa",P3),
        ("4","abierta — se lee C","la vuelta exterior no cierra",P4),
        ("5","remate cortado","como el interior del manifiesto",P5),
        ("6","fuera de registro","una vuelta corrida",P6),
        ("7","proporción manifiesto","0.571, la hoja — pieza vertical",P7),
        ("8","maciza","bandas anchas, para lo diminuto",P8)]


def svg(fn, s, bg, ink):
    if fn is P7:
        return fn(bg, ink)
    return f'<svg viewBox="0 0 100 100" width="{s}" height="{s}">{fn(bg,ink)}</svg>'

print(f'''<!doctype html><meta charset="utf-8"><title>C.F.D.L. — la espiral</title><style>
*{{box-sizing:border-box}}body{{margin:0;padding:32px 36px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
.intro{{color:#9a9ab0;max-width:900px;margin:0 0 22px}} .intro b{{color:#e6e6ef;font-weight:500}}
table{{border-collapse:collapse;width:100%}}
th{{font:400 10px/1 system-ui;letter-spacing:.18em;text-transform:uppercase;color:#6f6f88;padding:0 10px 12px;text-align:center;font-weight:400}}
th.l{{text-align:left}} td{{padding:14px 10px;border-top:1px solid #2a2a38;text-align:center;vertical-align:middle}}
td.l{{text-align:left;width:180px}} .k{{font:400 19px/1 system-ui;color:#ffb923}}
.n{{font-size:13px;margin-top:4px}} .d{{font-size:11.5px;color:#83839b;margin-top:2px;line-height:1.4}}
.claro{{background:#f8ccce;padding:8px;display:inline-block;line-height:0}}
.oscuro{{background:#171513;padding:8px;display:inline-block;line-height:0}}
.circ{{border-radius:50%;overflow:hidden;display:inline-block;line-height:0;background:#ffb923}}
.mini{{background:#fff;display:inline-block;line-height:0;padding:3px}}
</style>
<h1>C.F.D.L. — la espiral del manifiesto</h1>
<p class="intro">La hoja impresa compone el texto como una <b>espiral rectangular</b>:
rectángulos encajados girando hacia dentro, con la vuelta interior cortada a media
altura. <b>No cierra nunca.</b><br>Siete anillos se empastan a 32&nbsp;px, así que
aquí se prueba con cuántas vueltas sigue leyéndose. Y una espiral con la vuelta
exterior abierta <b>se lee como una C</b>.</p>
<table><tr><th class="l"></th><th>color</th><th>una tinta</th><th>en oscuro</th>
<th>círculo</th><th>48</th><th>32</th><th>16</th></tr>''')
for k,n,d,fn in PROP:
    print(f'''<tr><td class="l"><span class="k">{k}</span><div class="n">{n}</div><div class="d">{d}</div></td>
<td>{svg(fn,104,True,NEGRO)}</td><td><span class="claro">{svg(fn,104,False,ZAFIRO)}</span></td>
<td><span class="oscuro">{svg(fn,104,False,AMBAR)}</span></td>
<td><span class="circ">{svg(fn,108,True,NEGRO)}</span></td>
<td>{svg(fn,48,True,NEGRO)}</td><td>{svg(fn,32,True,NEGRO)}</td>
<td><span class="mini">{svg(fn,16,True,NEGRO)}</span></td></tr>''')
print("</table>")
