#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — explorador de la espiral.

Barrido de parámetros: cada sección mueve UNA cosa y deja el resto quieto, que
es la única manera de ver qué hace cada parámetro. Todo sobre retícula modular
—grosor y hueco en módulos enteros, remates a ras de caja— así que ninguna
variación es un ajuste a ojo.

    python3 explorador.py > explorador.html
"""
from espiral import espiral, U

from lockup import AMBAR, NEGRO, ZAFIRO, BLANCO, CREMA, ROSA, PAPEL


def pieza(P, N, M, gr, ink, giro=0, negativo=False, bg=None):
    kx = U / N
    W, H = U, U * M / N
    d = " ".join(f"{x*kx:.3f},{y*kx:.3f}" for x, y in P)
    trazo = (f'<polyline points="{d}" fill="none" stroke="{ink}" '
             f'stroke-width="{gr*kx:.3f}" stroke-linejoin="miter" '
             f'stroke-linecap="butt"/>')
    campo = f'<rect width="{W}" height="{H}" fill="{bg}"/>' if bg else ""
    if giro:
        trazo = (f'<g transform="rotate({giro} {W/2:.2f} {H/2:.2f})">{trazo}</g>')
    return campo + trazo, W, H


def svg(args, size=84, ink=NEGRO, bg=AMBAR, giro=0, negativo=False):
    P, N, M, gr = espiral(**args)
    if negativo:
        cuerpo, W, H = pieza(P, N, M, gr, bg or AMBAR, giro, bg=ink)
    else:
        cuerpo, W, H = pieza(P, N, M, gr, ink, giro, bg=bg)
    return (f'<svg viewBox="0 0 {W:.1f} {H:.1f}" width="{round(size*W/H)}" '
            f'height="{size}">{cuerpo}</svg>')


def celda(args, et, size=84, respaldo=None, **kw):
    """`respaldo` pone un fondo detrás de la celda: sin él, un dibujo sin campo
    y en tinta oscura desaparece sobre la página."""
    r = f' style="background:{respaldo};padding:6px"' if respaldo else ""
    return (f'<div class="c"><span class="caja"{r}>{svg(args, size, **kw)}</span>'
            f'<div class="et">{et}</div></div>')


SEC = []


def seccion(titulo, nota, celdas):
    SEC.append(f'<h2>{titulo}<span>{nota}</span></h2>'
               f'<div class="fila">{"".join(celdas)}</div>')


# § vueltas ────────────────────────────────────────────────────────────────
seccion("vueltas", "retícula 16, grosor 1 : hueco 1 — cuántas veces gira",
        [celda(dict(N=16, vueltas=v), f"{v}") for v in
         (1.5, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.5, 5)])

# § retícula ───────────────────────────────────────────────────────────────
seccion("retícula", "cuántos módulos de lado — a más módulos, trazo más fino",
        [celda(dict(N=n, vueltas=max(2, n/4.6)), f"N={n}") for n in
         (8, 10, 12, 14, 16, 18, 20, 24, 28, 32)])

# § grosor : hueco ─────────────────────────────────────────────────────────
seccion("grosor : hueco", "el peso del trazo contra el aire entre vueltas",
        [celda(dict(N=n, vueltas=3.5, gr=g, hu=h), f"{g}:{h}") for g, h, n in
         ((1,1,16),(1,2,20),(1,3,24),(2,1,16),(2,3,20),(3,1,20),(3,2,20),(1,1.5,18))])

# § remate interior ────────────────────────────────────────────────────────
seccion("remate interior", "dónde se detiene la última recta — el gesto abierto",
        [celda(dict(N=16, vueltas=3.75, corte=c), f"línea {c}" if c else "entera")
         for c in (None, 6, 7, 8, 9, 10, 11, 12)])

# § boca ───────────────────────────────────────────────────────────────────
seccion("boca", "módulos que se le quitan al arranque: abre la vuelta exterior",
        [celda(dict(N=16, vueltas=3.5, boca=b), f"{b}") for b in
         (0, 1, 2, 3, 4, 5, 6, 8, 10)])

# § proporción ─────────────────────────────────────────────────────────────
seccion("proporción", "generada en retícula más alta, no aplastada — el trazo "
        "no adelgaza",
        [celda(dict(N=16, M=m, vueltas=3.5), f"{16/m:.3f}") for m in
         (16, 18, 20, 22, 24, 26, 28, 32)])

# § giro ───────────────────────────────────────────────────────────────────
seccion("giro y sentido", "por qué esquina arranca y hacia dónde cierra",
        [celda(dict(N=16, vueltas=3.5), f"{g}°", giro=g) for g in (0, 90, 180, 270)]
        + [celda(dict(N=16, vueltas=3.5, espejo=True), f"espejo {g}°", giro=g)
           for g in (0, 90, 180, 270)])

# § tinta y campo ──────────────────────────────────────────────────────────
seccion("tinta y campo", "el mismo dibujo, cada combinación",
        [celda(dict(N=16, vueltas=3.5), et, bg=bg, ink=ink) for et, bg, ink in
         (("ámbar/negro", AMBAR, NEGRO), ("negro/ámbar", NEGRO, AMBAR),
          ("blanco/negro", BLANCO, NEGRO), ("blanco/zafiro", BLANCO, ZAFIRO),
          ("rosa/zafiro", "#f8ccce", ZAFIRO), ("zafiro/ámbar", ZAFIRO, AMBAR),
          ("negro/crema", NEGRO, CREMA))]
        + [celda(dict(N=16, vueltas=3.5), "sin campo · negro", bg=None, ink=NEGRO,
                 respaldo="#ffffff"),
           celda(dict(N=16, vueltas=3.5), "sin campo · blanco", bg=None, ink=BLANCO,
                 respaldo="#171513")]
        + [celda(dict(N=16, vueltas=3.5), "negativo", negativo=True,
                 bg=AMBAR, ink=NEGRO)])

# § combinaciones ──────────────────────────────────────────────────────────
DESTACA = [
    (dict(N=16, vueltas=3.75, corte=8), "16 · 3¾ · corte 8", 0),
    (dict(N=20, vueltas=4.5, corte=10), "20 · 4½ · corte 10", 0),
    (dict(N=12, vueltas=2.75, corte=6), "12 · 2¾ · corte 6", 0),
    (dict(N=16, vueltas=3.5, boca=4), "16 · boca 4", 0),
    (dict(N=20, vueltas=4, gr=1, hu=2), "20 · 1:2", 0),
    (dict(N=16, vueltas=3.5, gr=2, hu=1), "16 · 2:1", 0),
    (dict(N=16, M=28, vueltas=3.5, corte=14), "hoja 0.571", 0),
    (dict(N=16, vueltas=3.75, corte=8), "girada 180°", 180),
    (dict(N=10, vueltas=2.25), "10 · 2¼ — favicon", 0),
    (dict(N=24, vueltas=5, corte=12), "24 · 5 — densa", 0),
    (dict(N=16, vueltas=3.25, boca=2, corte=9), "boca 2 + corte 9", 0),
    (dict(N=18, vueltas=4, gr=1, hu=1.5), "18 · 1:1½", 0),
]
seccion("combinaciones", "a tamaño de uso, y a 32 px debajo",
        [f'<div class="c dos">{svg(a, 104, giro=g)}{svg(a, 32, giro=g)}'
         f'<div class="et">{et}</div></div>' for a, et, g in DESTACA])

print(f'''<!doctype html><meta charset="utf-8"><title>C.F.D.L. — explorador</title><style>
*{{box-sizing:border-box}}
body{{margin:0;padding:32px 36px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
h2{{font:400 11px/1 system-ui;letter-spacing:.2em;text-transform:uppercase;color:#e6e6ef;
   margin:38px 0 16px;border-top:1px solid #2a2a38;padding-top:16px;display:flex;
   justify-content:space-between;align-items:baseline;gap:20px}}
h2 span{{font:400 11.5px/1.4 system-ui;letter-spacing:0;text-transform:none;
        color:#83839b;text-align:right;max-width:560px}}
.intro{{color:#9a9ab0;max-width:920px;margin:0}} .intro b{{color:#e6e6ef;font-weight:500}}
.fila{{display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end}}
.c{{text-align:center;line-height:0}} .caja{{display:inline-block;line-height:0}}
.c svg{{display:block;background:transparent}}
.c.dos svg:first-child{{margin-bottom:6px}}
.c.dos svg:nth-child(2){{margin:0 auto}}
.et{{font:400 10px/1.3 system-ui;color:#6f6f88;margin-top:7px;letter-spacing:.04em}}
</style>
<h1>C.F.D.L. — explorador de la espiral</h1>
<p class="intro">Cada sección mueve <b>un</b> parámetro y deja el resto quieto: es la
única forma de ver qué hace cada uno. Todo sobre <b>retícula modular</b> —grosor y
hueco en módulos, remates a ras de caja— así que ninguna variación es un ajuste a
ojo.<br>La proporción se <b>genera</b> en una retícula más alta en vez de aplastarse
con <code>scale(x,1)</code>: aplastar adelgaza las verticales y rompe el trazo
uniforme.</p>
{"".join(SEC)}
''')
