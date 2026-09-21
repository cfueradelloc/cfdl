#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — ronda 8: el remate y el hueco.

La hoja (0.571) se ha probado y NO funciona: en una caja alta las vueltas dejan
de leerse como giro y se convierten en rectángulos concéntricos —un marco de
puerta—, el hueco central se vuelve una ranura, y a 32 px es una astilla. El
cuadrado gana. Queda dicho.

Así que el cuadrado se queda, y el trabajo es hacerlo específico en vez de
genérico. La palanca es el REMATE y el HUECO CENTRAL —el ojo de la letra, en
términos tipográficos—: es lo único que distingue una espiral dibujada de una
greca cualquiera.

Este barrido busca, por cálculo, los remates que dejan el hueco limpio.
"""
import sys
sys.path.insert(0, "..")
from espiral import espiral, polilinea, U

AMBAR, NEGRO = "#ffb923", "#171513"


def hueco(P, gr):
    """La caja de aire que queda dentro de la última vuelta."""
    c = gr / 2
    if len(P) < 5:
        return 0, 0, None
    # los cuatro últimos vértices encierran el vacío final
    ult = P[-5:]
    xs = [x for x, _ in ult]; ys = [y for _, y in ult]
    return (max(xs)-min(xs)) - gr, (max(ys)-min(ys)) - gr, (min(xs), min(ys))


def candidatos(N, gr=1, hu=1):
    """Remates que dejan el hueco cuadrado, calculados en vez de tanteados."""
    out = []
    for vt in [x/4 for x in range(8, 21)]:
        for cr in [None] + list(range(2, N)):
            P, N_, M_, g = espiral(N=N, vueltas=vt, gr=gr, hu=hu, corte=cr)
            hx, hy, _ = hueco(P, g)
            if hx <= 0 or hy <= 0:
                continue
            if abs(hx - hy) < 0.01:                    # hueco cuadrado
                out.append((vt, cr, hx, hy))
    return out


def marca(N, vueltas, corte=None, gr=1, hu=1, size=130, bg=AMBAR, ink=NEGRO):
    P, N_, M_, g = espiral(N=N, vueltas=vueltas, gr=gr, hu=hu, corte=corte)
    return (f'<svg viewBox="0 0 100 100" width="{size}" height="{size}">'
            f'<rect width="100" height="100" fill="{bg}"/>'
            f'{polilinea(P, N, g, ink)}</svg>')


S = []
def sec(t, n, cs): S.append(f'<h2>{t}<span>{n}</span></h2><div class="fila">{"".join(cs)}</div>')

def c(et, **kw):
    return (f'<div class="c">{marca(**kw)}'
            f'<div class="mini">{marca(size=32, **{k:v for k,v in kw.items() if k!="size"})}</div>'
            f'<div class="et">{et}</div></div>')

# § remates que dejan el hueco cuadrado ─────────────────────────────────────
cands = candidatos(16)
vistos, cs = set(), []
for vt, cr, hx, hy in cands:
    clave = (round(hx, 1), cr)
    if clave in vistos: continue
    vistos.add(clave)
    cs.append(c(f"{vt}v · corte {cr} · hueco {hx:.0f}", N=16, vueltas=vt, corte=cr))
sec("hueco cuadrado · retícula 16", f"{len(cs)} remates que cierran limpio, "
    f"hallados por cálculo", cs[:10])

# § el hueco contra el paso ─────────────────────────────────────────────────
sec("tamaño del hueco", "el ojo del signo: contra un paso de 2 módulos",
    [c(f"{n}² · {v}v · corte {cr}", N=n, vueltas=v, corte=cr)
     for n, v, cr in ((12,2.75,6),(14,3,7),(16,3.25,8),(16,3.75,8),
                      (18,4,9),(20,4.25,10),(20,4.75,10))])

# § menos vueltas, más presencia ────────────────────────────────────────────
sec("menos vueltas, más presencia", "la textura uniforme es pasiva; pocas "
    "vueltas mandan más",
    [c(f"{n}² · {v}v", N=n, vueltas=v, corte=cr)
     for n, v, cr in ((10,2.25,5),(10,2.5,5),(12,2.5,6),(12,2.75,6),
                      (14,2.75,7),(14,3,7))])

# § grosor contra hueco, sobre el mejor candidato ───────────────────────────
sec("peso del trazo", "sobre 12² · 2¾v · corte 6",
    [c(f"{g}:{h}", N=12, vueltas=2.75, corte=6, gr=g, hu=h)
     for g, h in ((1,1),(1,1.5),(1,2),(1.5,1),(2,1),(2,1.5),(3,2))])

print(f'''<!doctype html><meta charset="utf-8"><title>ronda 8</title><style>
*{{box-sizing:border-box}}body{{margin:0;padding:30px 34px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
h2{{font:400 11px/1 system-ui;letter-spacing:.2em;text-transform:uppercase;color:#e6e6ef;
   margin:34px 0 14px;border-top:1px solid #2a2a38;padding-top:14px;display:flex;
   justify-content:space-between;align-items:baseline;gap:20px}}
h2 span{{font:400 11.5px/1.4 system-ui;letter-spacing:0;text-transform:none;color:#83839b;text-align:right;max-width:520px}}
.intro{{color:#9a9ab0;max-width:900px;margin:0}} .intro b{{color:#e6e6ef;font-weight:500}}
.fila{{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}}
.c{{text-align:center;line-height:0;width:132px}} .c svg{{display:block;margin:0 auto}}
.mini{{margin-top:7px}}
.et{{font:400 10px/1.35 system-ui;color:#6f6f88;margin-top:7px}}
</style>
<h1>C.F.D.L. — el remate y el hueco</h1>
<p class="intro"><b>La hoja 0.571 se ha probado y no funciona:</b> en caja alta las
vueltas dejan de leerse como giro y se vuelven rectángulos concéntricos; el hueco
se convierte en ranura y a 32&nbsp;px es una astilla. El cuadrado gana.<br>
Lo que queda por resolver es el <b>remate</b> y el <b>hueco central</b> — el ojo del
signo. Es lo único que separa una espiral dibujada de una greca cualquiera. Los
remates de la primera fila están <b>calculados</b>, no tanteados: son los que dejan
el hueco cuadrado.</p>
{"".join(S)}
''')
