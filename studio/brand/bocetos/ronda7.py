#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — ronda 7: la hoja, no el cuadrado.

Crítica de la ronda anterior, en tres puntos:

  · el remate interior no resolvía — la espiral simplemente se acababa y
    dejaba un hueco en L. Se lee como quedarse sin sitio, no como una decisión.
  · el hueco central medía 4×2 módulos sin relación declarada con el paso.
  · y lo de fondo: una espiral CUADRADA es la greca griega. Es de todos. La
    conexión con el manifiesto era conceptual, invisible para quien mira.

De ahí la propuesta: la marca no es un cuadrado, es la PROPORCIÓN DE LA HOJA
impresa (0.571). Una espiral cuadrada es un patrón; una hoja con el texto
girando alrededor es suya.
"""
import sys
sys.path.insert(0, "..")
from espiral import espiral, polilinea, U

AMBAR, NEGRO, ZAFIRO, BLANCO, CREMA = "#ffb923","#171513","#332f8a","#ffffff","#fff4d6"


def marca(N, M, vueltas, gr=1, hu=1, corte=None, bg=AMBAR, ink=NEGRO,
          campo_N=None, campo_M=None, size=120):
    """Dibuja la espiral, opcionalmente centrada dentro de un campo mayor."""
    P, N_, M_, gr_ = espiral(N=N, M=M, vueltas=vueltas, gr=gr, hu=hu, corte=corte)
    CN = campo_N or N
    CM = campo_M or M
    k = U / CN
    dx = (CN - N) / 2.0
    dy = (CM - M) / 2.0
    W, H = U, U * CM / CN
    cuerpo = polilinea(P, CN, gr_, ink, desplaza=(dx, dy))
    campo = f'<rect width="{W}" height="{H:.2f}" fill="{bg}"/>' if bg else ""
    return (f'<svg viewBox="0 0 {W} {H:.2f}" width="{round(size*W/H)}" '
            f'height="{size}">{campo}{cuerpo}</svg>')


def c(et, **kw):
    return f'<div class="c">{marca(**kw)}<div class="et">{et}</div></div>'


S = []
def sec(t, n, cs): S.append(f'<h2>{t}<span>{n}</span></h2><div class="fila">{"".join(cs)}</div>')


# § la hoja sola, distintas densidades ──────────────────────────────────────
sec("la hoja · 0.571", "N×M en módulos — la proporción de la hoja impresa",
    [c(f"{n}×{m} · {v}v", N=n, M=m, vueltas=v, corte=cr, size=150)
     for n, m, v, cr in ((8,14,2.25,None),(8,14,2.5,7),(10,18,2.75,9),
                         (10,18,3,9),(12,21,3.25,11),(12,21,3.5,11),
                         (14,25,3.75,13),(16,28,4,14))])

# § la hoja dentro de un campo cuadrado — avatar y favicon ──────────────────
sec("la hoja en campo cuadrado", "para el círculo y el favicon: el campo es "
    "cuadrado, la hoja no",
    [c(f"hoja {n}×{m} en {cn}²", N=n, M=m, vueltas=v, corte=cr,
       campo_N=cn, campo_M=cn, size=120)
     for n, m, v, cr, cn in ((8,14,2.5,7,18),(10,18,3,9,22),(10,18,3,9,24),
                             (12,21,3.25,11,26),(8,14,2.25,None,16))])

# § remate interior: dónde muere la espiral ─────────────────────────────────
sec("remate interior", "dónde se detiene — que parezca decidido y no que se "
    "acabó el sitio",
    [c(f"corte {cr}" if cr else "entera", N=10, M=18, vueltas=3, corte=cr, size=150)
     for cr in (None, 7, 8, 9, 10, 11, 12)])

# § el cuadrado, para comparar ──────────────────────────────────────────────
sec("el cuadrado, para comparar", "lo que había: legible, pero es la greca de "
    "todo el mundo",
    [c(f"{n}² · {v}v", N=n, M=n, vueltas=v, corte=cr, size=150)
     for n, v, cr in ((16,3.5,None),(16,3.75,8),(20,4.5,10),(12,2.75,6))])

# § tamaños de uso ──────────────────────────────────────────────────────────
for et, kw in (("hoja 10×18 · 3v · corte 9", dict(N=10, M=18, vueltas=3, corte=9)),
               ("hoja en campo 22²", dict(N=10, M=18, vueltas=3, corte=9,
                                          campo_N=22, campo_M=22))):
    sec(f"tamaños · {et}", "el mismo dibujo a lo que mide de verdad",
        [c(f"{s} px", size=s, **kw) for s in (150, 96, 64, 48, 32, 24, 16)])

print(f'''<!doctype html><meta charset="utf-8"><title>ronda 7</title><style>
*{{box-sizing:border-box}}body{{margin:0;padding:30px 34px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
h2{{font:400 11px/1 system-ui;letter-spacing:.2em;text-transform:uppercase;color:#e6e6ef;
   margin:34px 0 14px;border-top:1px solid #2a2a38;padding-top:14px;display:flex;
   justify-content:space-between;align-items:baseline;gap:20px}}
h2 span{{font:400 11.5px/1.4 system-ui;letter-spacing:0;text-transform:none;color:#83839b;text-align:right;max-width:520px}}
.intro{{color:#9a9ab0;max-width:900px;margin:0}} .intro b{{color:#e6e6ef;font-weight:500}}
.fila{{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end}}
.c{{text-align:center;line-height:0}} .c svg{{display:block}}
.et{{font:400 10px/1.3 system-ui;color:#6f6f88;margin-top:7px}}
</style>
<h1>C.F.D.L. — la hoja, no el cuadrado</h1>
<p class="intro">Una espiral <b>cuadrada</b> es la greca griega: es de todos, y la
conexión con el manifiesto se queda en lo conceptual. La hoja impresa tiene una
proporción concreta —<b>0.571</b>— y con ella el signo deja de ser un patrón y pasa
a ser una hoja con el texto girando alrededor.<br>Donde hace falta cuadrado
—círculo de perfil, favicon— el <b>campo</b> es cuadrado y la hoja va centrada
dentro.</p>
{"".join(S)}
''')
