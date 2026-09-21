#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — ronda 11: la familia del margen, a fondo.

La ronda 10 encontró la idea —texto en el margen, centro vacío— y se quedó ahí:
tres densidades elegidas a ojo y a otra cosa. Eso fue pereza. Aquí se barre la
familia de verdad, y CADA variante se prueba junto a las siglas, que es donde
un signo se cae.

Se mueve: anillos, aire entre vueltas, cuánto vacío, dónde muere la última
vuelta, proporción, aire progresivo, y el sentido de giro.
"""
import sys
sys.path.insert(0, "..")
from espiral import espiral, polilinea, U
from firma import firma

AMBAR, NEGRO, ZAFIRO, BLANCO, CREMA = "#ffb923","#171513","#332f8a","#ffffff","#fff4d6"


def N_para(anillos, gr, hu, vacio):
    """El lado en módulos que deja el vacío central pedido."""
    banda = anillos * (gr + hu)
    return max(2 * banda + 2, int(round(2 * banda / (1 - vacio))))


def cuerpo(anillos=7, gr=1, hu=4, vacio=0.62, ratio=1.0, corte_rel=0.55,
           hu_prog=1.0, espejo=False, margen=0.05, ink=NEGRO, campo=AMBAR):
    N = N_para(anillos, gr, hu, vacio)
    M = round(N * ratio)
    banda = anillos * (gr + hu)
    cr = banda + (min(N, M) - 2 * banda) * corte_rel if corte_rel is not None else None
    P, *_ , g = espiral(N=N, M=M, vueltas=anillos, gr=gr, hu=hu, corte=cr,
                        espejo=espejo, hu_prog=hu_prog)
    m = round(N * margen); CN = N + 2 * m
    H = U * (M + 2 * m) / CN
    fondo = f'<rect width="100" height="{H:.2f}" fill="{campo}"/>' if campo else ""
    return (fondo + polilinea(P, CN, g, ink, desplaza=(m, m)), H / U)


def cel(et, size=96, firma_alto=40, ink=NEGRO, campo=AMBAR, respaldo="", **kw):
    c, ratio = cuerpo(ink=ink, campo=campo, **kw)
    sv = (f'<svg viewBox="0 0 100 {100*ratio:.1f}" width="{round(size/ratio)}" '
          f'height="{size}">{c}</svg>')
    # La firma siempre sobre fondo visible: si no, tinta negra sobre la página
    # oscura desaparece y la prueba no prueba nada.
    fondo_fi = campo or (NEGRO if ink in (BLANCO, AMBAR, CREMA) else BLANCO)
    fi = firma(c, ratio, firma_alto, ink, fondo_fi, rel=1.35, aire=0.10)
    return (f'<div class="c"><span class="caja {respaldo}">{sv}</span>'
            f'<span class="caja fi">{fi}</span>'
            f'<div class="et">{et}</div></div>')


S = []
def sec(t, n, cs): S.append(f'<h2>{t}<span>{n}</span></h2><div class="fila">{"".join(cs)}</div>')

# 1 · anillos ───────────────────────────────────────────────────────────────
sec("anillos", "cuántas vueltas da la banda — aire 1:4, vacío 62 % fijos",
    [cel(f"{a} anillos", anillos=a) for a in range(3, 13)])

# 2 · aire entre vueltas ────────────────────────────────────────────────────
sec("aire entre vueltas", "1:4 es lo medido en la hoja. Menos aire aprieta; "
    "más, se deshilacha",
    [cel(f"1:{h}", hu=h) for h in (2, 2.5, 3, 3.5, 4, 5, 6, 8, 10)])

# 3 · cuánto vacío ──────────────────────────────────────────────────────────
sec("cuánto vacío", "el centro en blanco: es lo que significa estar en el margen",
    [cel(f"{int(v*100)} %", vacio=v) for v in
     (0.30, 0.40, 0.48, 0.55, 0.62, 0.68, 0.74, 0.80, 0.85)])

# 4 · dónde muere la última vuelta ──────────────────────────────────────────
sec("remate interior", "la hoja corta su vuelta interior a media altura",
    [cel("entera" if c is None else f"{int(c*100)} %", corte_rel=c)
     for c in (None, 0.0, 0.15, 0.3, 0.45, 0.55, 0.7, 0.85, 1.0)])

# 5 · proporción ────────────────────────────────────────────────────────────
sec("proporción", "0.571 es la de la hoja impresa",
    [cel(f"{1/r:.3f}" if r != 1 else "1.000", ratio=r) for r in
     (1.0, 1.15, 1.3, 1.45, 1.6, 1.75, 1.95, 2.2)])

# 6 · aire progresivo ───────────────────────────────────────────────────────
sec("aire progresivo", "el hueco se abre o se cierra hacia dentro, como un "
    "texto que gira",
    [cel(f"×{p}", hu_prog=p, anillos=6) for p in
     (0.72, 0.80, 0.88, 0.94, 1.0, 1.06, 1.14, 1.24, 1.38)])

# 7 · grosor ────────────────────────────────────────────────────────────────
sec("grosor del trazo", "con el aire proporcional, para no cambiar dos cosas",
    [cel(f"trazo {g}", gr=g, hu=4*g, anillos=6) for g in (0.5, 0.75, 1, 1.5, 2, 3)])

# 8 · sentido ───────────────────────────────────────────────────────────────
sec("sentido de giro", "por dónde abre la banda",
    [cel("normal"), cel("espejo", espejo=True)])

# 9 · tinta y campo ─────────────────────────────────────────────────────────
sec("tinta y campo", "la firma manda: ahí se ve si el signo tiene voz",
    [cel(et, ink=i, campo=b, respaldo=r) for et, i, b, r in
     (("ámbar / negro", NEGRO, AMBAR, ""),
      ("negro / ámbar", AMBAR, NEGRO, ""),
      ("sin campo, negro", NEGRO, None, "b-blanco"),
      ("sin campo, blanco", BLANCO, None, "b-negro"),
      ("rosa / zafiro", ZAFIRO, "#f8ccce", ""),
      ("zafiro / crema", CREMA, ZAFIRO, ""),
      ("blanco / zafiro", ZAFIRO, BLANCO, ""))])

# 10 · candidatas ───────────────────────────────────────────────────────────
CAND = [
  ("A", dict(anillos=7, hu=4, vacio=0.62)),
  ("B", dict(anillos=5, hu=4, vacio=0.68)),
  ("C", dict(anillos=9, hu=3, vacio=0.55)),
  ("D", dict(anillos=6, hu=5, vacio=0.70)),
  ("E", dict(anillos=4, hu=4, vacio=0.74)),
  ("F", dict(anillos=7, hu=4, vacio=0.62, ratio=1.75)),
  ("G", dict(anillos=6, hu=4, vacio=0.62, hu_prog=1.14)),
  ("H", dict(anillos=8, hu=3.5, vacio=0.58, corte_rel=0.3)),
]
sec("candidatas", "a tamaño de uso, en firma, y a 32 px",
    [f'<div class="c">{cel(k, size=116, firma_alto=40, **kw)[len(chr(60)+"div class="+chr(34)+"c"+chr(34)+chr(62)):-6]}'
     f'</div>' for k, kw in CAND])

print(f'''<!doctype html><meta charset="utf-8"><title>ronda 11 — la familia del margen</title>
<style>
@font-face{{font-family:'FuturaStd';src:url('../../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');font-display:block}}
*{{box-sizing:border-box}}body{{margin:0;padding:30px 34px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
h2{{font:400 11px/1 system-ui;letter-spacing:.2em;text-transform:uppercase;color:#e6e6ef;
   margin:34px 0 14px;border-top:1px solid #2a2a38;padding-top:14px;display:flex;
   justify-content:space-between;align-items:baseline;gap:20px}}
h2 span{{font:400 11.5px/1.4 system-ui;letter-spacing:0;text-transform:none;color:#83839b;text-align:right;max-width:500px}}
.intro{{color:#9a9ab0;max-width:920px;margin:0}} .intro b{{color:#e6e6ef;font-weight:500}}
.fila{{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}}
.c{{text-align:center;line-height:0;width:210px}}
.c svg{{display:block;margin:0 auto}}
.caja{{display:block}}
.caja{{display:block;line-height:0}}
.caja.fi{{margin-top:10px}}
.b-blanco{{background:#fff;padding:6px}} .b-negro{{background:#171513;padding:6px}}
.et{{font:400 10px/1.35 system-ui;color:#6f6f88;margin-top:8px}}
</style>
<h1>C.F.D.L. — la familia del margen, a fondo</h1>
<p class="intro">La ronda anterior encontró la idea —texto en el <b>margen</b>, centro
<b>vacío</b>— y se quedó ahí: tres densidades a ojo. Aquí se barre la familia de
verdad.<br><b>Cada variante va con su firma debajo</b>, porque es al lado de las
siglas donde un signo se cae: si el trazo es demasiado fino, la letra se lo come.</p>
{"".join(S)}
''')
