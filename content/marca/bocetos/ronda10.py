#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — ronda 10: el margen.

LO QUE ESTABA HACIENDO MAL. Venía enrollando la espiral hacia el centro hasta
dejar un hueco pequeño. Es lo contrario de lo que significa: en la hoja
impresa el texto vive en los MÁRGENES y el centro queda VACÍO — el colectivo
está fuera de lugar, en los bordes.

Medido sobre el original (svg_espiral_frame en content/tshirts): trazo 1, hueco
4, siete anillos. La banda ocupa ~15 % de cada lado y deja el ~70 % central en
blanco. El hueco entre vueltas es CUATRO VECES el grosor, no igual.

Así que los parámetros se invierten: trazo fino, hueco ancho, muchos anillos,
banda estrecha pegada al borde, vacío grande en medio.
"""
import sys
sys.path.insert(0, "..")
from espiral import espiral, polilinea, U

AMBAR, NEGRO, ZAFIRO, BLANCO, CREMA = "#ffb923","#171513","#332f8a","#ffffff","#fff4d6"


def marca(anillos, hu, gr=1, N=None, corte=None, size=130, bg=AMBAR, ink=NEGRO,
          M=None, margen=0):
    """N se calcula para que quede el vacío pedido, no al revés."""
    paso = gr + hu
    N = N or int(2 * anillos * paso + 2 * paso)
    P, N_, M_, g = espiral(N=N, M=M, vueltas=anillos, gr=gr, hu=hu, corte=corte)
    CN = N + 2 * margen
    d = margen
    alto = (M or N)
    H = U * (alto + 2*margen) / CN
    campo = f'<rect width="100" height="{H:.2f}" fill="{bg}"/>' if bg else ""
    return (f'<svg viewBox="0 0 100 {H:.2f}" width="{round(size*100/H)}" '
            f'height="{size}">{campo}'
            f'{polilinea(P, CN, g, ink, desplaza=(d, d))}</svg>')


def vacio(anillos, hu, gr=1):
    paso = gr + hu
    N = int(2 * anillos * paso + 2 * paso)
    return 100.0 * (N - 2 * anillos * paso) / N


S = []
def sec(t, n, cs): S.append(f'<h2>{t}<span>{n}</span></h2><div class="fila">{"".join(cs)}</div>')

def c(et, **kw):
    kw2 = {k: v for k, v in kw.items() if k != "size"}
    return (f'<div class="c">{marca(**kw)}'
            f'<div class="mini">{marca(size=30, **kw2)}</div>'
            f'<div class="et">{et}</div></div>')

# § hueco contra grosor ─────────────────────────────────────────────────────
sec("hueco : grosor", "en el original es 4:1 — el aire entre vueltas es cuatro "
    "veces el trazo",
    [c(f"1:{h} · vacío {vacio(6,h):.0f}%", anillos=6, hu=h) for h in (1,2,3,4,5,6,8)])

# § número de anillos ───────────────────────────────────────────────────────
sec("anillos", "cuántas vueltas da la banda del margen — hueco 4:1 fijo",
    [c(f"{a} anillos · vacío {vacio(a,4):.0f}%", anillos=a, hu=4)
     for a in (3,4,5,6,7,8,9,10)])

# § cuánto vacío ────────────────────────────────────────────────────────────
sec("cuánto vacío", "N crece y la banda se queda igual: el centro manda",
    [c(f"vacío {100*(N-2*7*5)/N:.0f}%", anillos=7, hu=4, N=N)
     for N in (80, 90, 100, 120, 140, 170, 200)])

# § el remate, sobre banda fina ─────────────────────────────────────────────
sec("remate interior", "la última vuelta cortada, como en la hoja",
    [c("entera" if cr is None else f"corte {cr}", anillos=7, hu=4, N=120, corte=cr)
     for cr in (None, 20, 30, 40, 50, 60)])

# § proporción de hoja, ahora que la banda es fina ──────────────────────────
sec("proporción de hoja", "con banda fina la caja alta sí aguanta — es una hoja",
    [c(f"{n}×{m}", anillos=6, hu=4, N=n, M=m)
     for n, m in ((70,70),(70,90),(70,110),(70,123),(70,140))])

# § tinta y campo ───────────────────────────────────────────────────────────
sec("tinta y campo", "banda fina, vacío grande",
    [f'<div class="c"><span class="caja {css}">'
     f'{marca(anillos=7, hu=4, N=120, corte=40, size=120, bg=bg, ink=ink)}</span>'
     f'<div class="et">{et}</div></div>'
     for et, css, bg, ink in
     (("ámbar/negro","", AMBAR, NEGRO), ("negro/ámbar","", NEGRO, AMBAR),
      ("sin campo, negro","b-blanco", None, NEGRO),
      ("sin campo, blanco","b-negro", None, BLANCO),
      ("rosa/zafiro","", "#f8ccce", ZAFIRO), ("zafiro/crema","", ZAFIRO, CREMA))])

# § los tamaños ─────────────────────────────────────────────────────────────
for et, kw in (("7 anillos · 1:4 · vacío 42 %", dict(anillos=7, hu=4, N=120, corte=40)),
               ("5 anillos · 1:4 · vacío 55 %", dict(anillos=5, hu=4, N=110, corte=36)),
               ("9 anillos · 1:3 · vacío 40 %", dict(anillos=9, hu=3, N=120, corte=40))):
    sec(f"tamaños · {et}", "una banda fina se cierra pronto: aquí está el límite",
        [f'<div class="c">{marca(size=s, **kw)}<div class="et">{s} px</div></div>'
         for s in (150, 96, 64, 48, 32, 24, 16)]
        + [f'<div class="c"><span class="circ">{marca(size=130, margen=6, **kw)}</span>'
           f'<div class="et">círculo</div></div>'])

print(f'''<!doctype html><meta charset="utf-8"><title>ronda 10 — el margen</title><style>
*{{box-sizing:border-box}}body{{margin:0;padding:30px 34px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
h2{{font:400 11px/1 system-ui;letter-spacing:.2em;text-transform:uppercase;color:#e6e6ef;
   margin:34px 0 14px;border-top:1px solid #2a2a38;padding-top:14px;display:flex;
   justify-content:space-between;align-items:baseline;gap:20px}}
h2 span{{font:400 11.5px/1.4 system-ui;letter-spacing:0;text-transform:none;color:#83839b;text-align:right;max-width:520px}}
.intro{{color:#9a9ab0;max-width:920px;margin:0}} .intro b{{color:#e6e6ef;font-weight:500}}
.fila{{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}}
.c{{text-align:center;line-height:0;min-width:120px}} .c svg{{display:block;margin:0 auto}}
.mini{{margin-top:8px}} .mini svg{{margin:0 auto}}
.et{{font:400 10px/1.4 system-ui;color:#6f6f88;margin-top:7px}}
.caja{{display:inline-block;line-height:0;padding:9px}}
.b-blanco{{background:#fff}} .b-negro{{background:#171513}}
.circ{{border-radius:50%;overflow:hidden;display:inline-block;line-height:0}}
</style>
<h1>C.F.D.L. — el margen</h1>
<p class="intro"><b>Lo estaba haciendo al revés.</b> Venía enrollando la espiral hacia
el centro hasta dejar un hueco pequeño — lo contrario de lo que significa. En la hoja
impresa el texto vive en los <b>márgenes</b> y el centro queda <b>vacío</b>: el
colectivo está fuera de lugar, en los bordes.<br>
Medido sobre el original: <b>trazo 1, hueco 4, siete anillos</b>. La banda ocupa un
15 % de cada lado y deja el 70 % central en blanco. El aire entre vueltas es
<b>cuatro veces</b> el grosor, no igual.</p>
{"".join(S)}
''')
