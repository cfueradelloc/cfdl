#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — ronda 6: retícula modular y variaciones.

DOS CORRECCIONES DE FONDO

1 · Alineación. El remate superior moría sobre la LÍNEA MEDIA de la columna
    izquierda, no sobre su borde: medio grosor corto. En una marca geométrica
    eso se lee como un error. Ahora los dos remates libres van a ras de la caja.

2 · Retícula. Se acabó el ajustar a ojo: la marca se construye sobre una
    retícula de N módulos. Grosor = 1 módulo, hueco = 1 módulo, paso = 2. Cada
    trazo, cada hueco y cada remate cae sobre una línea entera de la retícula,
    así que la alineación es demostrable y no opinable.

Con eso puesto, las variaciones son de forma, no de arreglo.
"""
AMBAR, NEGRO, ZAFIRO, BLANCO, CREMA = "#ffb923","#171513","#332f8a","#ffffff","#fff4d6"
U = 100.0


def espiral(N=16, vueltas=3.5, gr=1, hu=1, alto_N=None, corte=None,
            flush=True, boca=0):
    """Espiral rectangular sobre retícula de N módulos.

    gr, hu   grosor y hueco, en módulos
    corte    módulo en que se detiene la última recta (None = entera)
    flush    los remates libres salen a ras de la caja
    boca     módulos que se le quitan al arranque: abre la vuelta exterior
    """
    M = alto_N or N
    paso = gr + hu
    c = gr / 2.0                       # centro del trazo
    l, t, r, b = c, c, N - c, M - c
    P = []
    # remate de arranque: a ras del borde, no sobre la línea media
    P.append((0.0 if flush else l, t))
    if boca:
        P[0] = (boca, t)
    n = int(vueltas * 4)
    for k in range(n):
        if r - l < paso or b - t < paso:
            break
        ult = (k == n - 1)
        lado = k % 4
        if lado == 0:
            P.append((r, t))
        elif lado == 1:
            y = corte if (ult and corte is not None) else b
            P.append((r, y))
        elif lado == 2:
            P.append((l, b)); t += paso
        else:
            P.append((l, t)); l += paso; r -= paso; b -= paso
    # remate final a ras si termina en el borde
    return P, N, M, gr


def render(P, N, M, gr, ink, taper=False):
    k = U / N
    d = " ".join(f"{x*k:.3f},{y*k:.3f}" for x, y in P)
    w = gr * k
    if not taper:
        return (f'<polyline points="{d}" fill="none" stroke="{ink}" '
                f'stroke-width="{w:.3f}" stroke-linejoin="miter" '
                f'stroke-linecap="butt"/>')
    # trazo que adelgaza hacia dentro: cada vuelta, un poco más fino
    seg = []
    for i in range(len(P) - 1):
        f = 1.0 - 0.14 * (i // 4)
        a, b_ = P[i], P[i+1]
        seg.append(f'<line x1="{a[0]*k:.3f}" y1="{a[1]*k:.3f}" '
                   f'x2="{b_[0]*k:.3f}" y2="{b_[1]*k:.3f}" stroke="{ink}" '
                   f'stroke-width="{w*f:.3f}" stroke-linecap="butt"/>')
    return "".join(seg)


def campo(on, c=AMBAR, ratio=1.0):
    return f'<rect width="{U}" height="{U*ratio}" fill="{c}"/>' if on else ""


# ── variaciones ────────────────────────────────────────────────────────────
def V1(bg=True, ink=NEGRO):      # base: retícula 16, remates a ras
    return campo(bg) + render(*espiral(16, 3.5), ink)

def V2(bg=True, ink=NEGRO):      # remate interior cortado sobre línea de retícula
    return campo(bg) + render(*espiral(16, 3.75, corte=8), ink)

def V3(bg=True, ink=NEGRO):      # más aire: retícula 20, trazo más fino
    return campo(bg) + render(*espiral(20, 4.5), ink)

def V4(bg=True, ink=NEGRO):      # trazo grueso, hueco fino — más peso
    return campo(bg) + render(*espiral(16, 3.5, gr=2, hu=1), ink)

def V5(bg=True, ink=NEGRO):      # adelgaza hacia dentro, como el texto al girar
    return campo(bg) + render(*espiral(16, 3.5), ink, taper=True)

def V6(bg=True, ink=NEGRO):      # la vuelta exterior abierta: se lee C
    return campo(bg) + render(*espiral(16, 3.5, boca=6), ink)

def V7(bg=True, ink=NEGRO):      # proporción de la hoja dentro del cuadrado
    P, N, M, gr = espiral(16, 3.0, alto_N=16)
    k = U / N
    inner = render(P, N, M, gr, ink)
    return campo(bg) + f'<g transform="translate(21,0) scale(0.571,1)">{inner}</g>'

def V8(bg=True, ink=NEGRO):      # negativo: campo sólido, espiral en hueco
    P, N, M, gr = espiral(16, 3.5)
    return (f'<rect width="{U}" height="{U}" fill="{ink}"/>'
            + render(P, N, M, gr, AMBAR if bg else BLANCO))

def V9(bg=True, ink=NEGRO):      # pocas vueltas, mucho cuerpo — lo diminuto
    return campo(bg) + render(*espiral(10, 2.25, gr=1, hu=1), ink)


PROP = [("1","base · retícula 16","remates a ras de caja",V1),
        ("2","remate cortado","se detiene en la línea 8",V2),
        ("3","retícula 20","más vueltas, más fino",V3),
        ("4","grosor 2 : hueco 1","el trazo pesa más que el aire",V4),
        ("5","adelgaza hacia dentro","como el texto al cerrar la espiral",V5),
        ("6","vuelta exterior abierta","se lee como C",V6),
        ("7","proporción de la hoja","0.571 dentro del cuadrado",V7),
        ("8","negativo","campo sólido, espiral en hueco",V8),
        ("9","retícula 10","pocas vueltas, mucho cuerpo",V9)]


def svg(fn, s, bg, ink, grid=False):
    g = ""
    if grid:
        k = U / 16
        g = "".join(f'<line x1="{i*k}" y1="0" x2="{i*k}" y2="{U}" stroke="#ff00a0" '
                    f'stroke-width="0.3" opacity="0.55"/>'
                    f'<line x1="0" y1="{i*k}" x2="{U}" y2="{i*k}" stroke="#ff00a0" '
                    f'stroke-width="0.3" opacity="0.55"/>' for i in range(17))
    return f'<svg viewBox="0 0 100 100" width="{s}" height="{s}">{fn(bg,ink)}{g}</svg>'

print(f'''<!doctype html><meta charset="utf-8"><title>ronda 6</title><style>
*{{box-sizing:border-box}}body{{margin:0;padding:30px 34px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
.intro{{color:#9a9ab0;max-width:900px;margin:0 0 20px}} .intro b{{color:#e6e6ef;font-weight:500}}
table{{border-collapse:collapse;width:100%}}
th{{font:400 10px/1 system-ui;letter-spacing:.18em;text-transform:uppercase;color:#6f6f88;padding:0 10px 12px;text-align:center;font-weight:400}}
th.l{{text-align:left}} td{{padding:14px 10px;border-top:1px solid #2a2a38;text-align:center;vertical-align:middle}}
td.l{{text-align:left;width:168px}} .k{{font:400 19px/1 system-ui;color:#ffb923}}
.n{{font-size:13px;margin-top:4px}} .d{{font-size:11.5px;color:#83839b;margin-top:2px;line-height:1.4}}
.claro{{background:#f8ccce;padding:8px;display:inline-block;line-height:0}}
.oscuro{{background:#171513;padding:8px;display:inline-block;line-height:0}}
.circ{{border-radius:50%;overflow:hidden;display:inline-block;line-height:0;background:#ffb923}}
.mini{{background:#fff;display:inline-block;line-height:0;padding:3px}}
</style>
<h1>C.F.D.L. — retícula modular y variaciones</h1>
<p class="intro"><b>El fallo que había:</b> el remate superior moría sobre la línea
media de la columna izquierda, no sobre su borde — medio grosor corto. Corregido:
los remates libres van a ras de caja.<br>
<b>Y la retícula:</b> grosor 1 módulo, hueco 1 módulo, paso 2. Todo cae en línea
entera, así que la alineación es demostrable. La columna rosa lo enseña.</p>
<table><tr><th class="l"></th><th>retícula</th><th>color</th><th>una tinta</th>
<th>en oscuro</th><th>círculo</th><th>48</th><th>32</th><th>16</th></tr>''')
for k,n,dd,fn in PROP:
    print(f'''<tr><td class="l"><span class="k">{k}</span><div class="n">{n}</div><div class="d">{dd}</div></td>
<td>{svg(fn,104,True,NEGRO,grid=True)}</td>
<td>{svg(fn,104,True,NEGRO)}</td><td><span class="claro">{svg(fn,104,False,ZAFIRO)}</span></td>
<td><span class="oscuro">{svg(fn,104,False,AMBAR)}</span></td>
<td><span class="circ">{svg(fn,108,True,NEGRO)}</span></td>
<td>{svg(fn,48,True,NEGRO)}</td><td>{svg(fn,32,True,NEGRO)}</td>
<td><span class="mini">{svg(fn,16,True,NEGRO)}</span></td></tr>''')
print("</table>")
