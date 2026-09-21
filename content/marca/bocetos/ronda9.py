#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — ronda 9: finalistas, en uso.

Corregido el error de medida de la ronda 8: `hueco()` leía los cinco últimos
vértices, que sólo describen el vacío cuando la espiral da pocas vueltas. Con
más vueltas devolvía el interior entero, así que la «búsqueda por cálculo»
sólo encontraba casos de 2¼ vueltas. Ahora se mide la última vuelta completa.

Y el hallazgo que sí vale: 2½–3 vueltas tienen mucha más presencia que 3½–4¾.
Lo denso se lee como textura; lo escaso, como signo. Aquí van los finalistas a
lo que miden de verdad, en círculo, y junto a las siglas.
"""
import sys
sys.path.insert(0, "..")
from espiral import espiral, polilinea, U

AMBAR, NEGRO, ZAFIRO, BLANCO, CREMA = "#ffb923","#171513","#332f8a","#ffffff","#fff4d6"
F = "FuturaStd, Helvetica, Arial"


def hueco(P, gr):
    """Vacío central: la caja que encierra la ÚLTIMA vuelta completa.

    (El fallo anterior: mirar sólo los últimos vértices devuelve el interior
    entero cuando hay muchas vueltas.)"""
    c = gr / 2
    if len(P) < 6:
        return 0.0, 0.0
    ult = P[-6:]
    xs = sorted(x for x, _ in ult); ys = sorted(y for _, y in ult)
    return max(0.0, xs[-1]-xs[0]-gr), max(0.0, ys[-1]-ys[0]-gr)


def sv(N, v, cr, size, bg=AMBAR, ink=NEGRO, margen=0, campo=None):
    P, N_, M_, g = espiral(N=N, vueltas=v, corte=cr)
    CN = campo or (N + 2*margen)
    k = U / CN
    d = (CN - N) / 2.0
    campo_r = f'<rect width="100" height="100" fill="{bg}"/>' if bg else ""
    return (f'<svg viewBox="0 0 100 100" width="{size}" height="{size}">'
            f'{campo_r}{polilinea(P, CN, g, ink, desplaza=(d, d))}</svg>')


FIN = [("A", 12, 2.75, 6), ("B", 14, 3.0, 7), ("C", 16, 3.25, 8),
       ("D", 10, 2.5, 5),  ("E", 16, 3.75, 8)]

S = []
def sec(t, n, cs): S.append(f'<h2>{t}<span>{n}</span></h2><div class="fila">{"".join(cs)}</div>')

# § los cinco, con sus medidas ──────────────────────────────────────────────
cs = []
for k, N, v, cr in FIN:
    P, _, _, g = espiral(N=N, vueltas=v, corte=cr)
    hx, hy = hueco(P, g)
    cs.append(f'<div class="c"><div class="k">{k}</div>{sv(N,v,cr,130,margen=2)}'
              f'<div class="et">{N}² · {v}v · corte {cr}<br>'
              f'hueco {hx:.0f}×{hy:.0f} de {N} mód</div></div>')
sec("los cinco", "con margen 2 dentro del campo", cs)

# § a lo que miden ──────────────────────────────────────────────────────────
for k, N, v, cr in FIN:
    sec(f"{k} · {N}² · {v}v", "tamaños de uso, y el círculo de perfil",
        [f'<div class="c">{sv(N,v,cr,s,margen=2)}<div class="et">{s} px</div></div>'
         for s in (120, 64, 48, 32, 24, 16)]
        + [f'<div class="c"><span class="circ">{sv(N,v,cr,120,margen=6)}</span>'
           f'<div class="et">círculo</div></div>',
           f'<div class="c"><span class="caja b-blanco">{sv(N,v,cr,84,bg=None,ink=NEGRO,margen=2)}</span>'
           f'<div class="et">sin campo</div></div>',
           f'<div class="c"><span class="caja b-negro">{sv(N,v,cr,84,bg=None,ink=AMBAR,margen=2)}</span>'
           f'<div class="et">en oscuro</div></div>'])

# § junto a las siglas ──────────────────────────────────────────────────────
def linea(N, v, cr, bg, ink, size=54):
    P, _, _, g = espiral(N=N, vueltas=v, corte=cr)
    CN = N + 4
    d = (CN - N) / 2.0
    campo_r = f'<rect width="340" height="100" fill="{bg}"/>' if bg else ""
    return (f'<svg viewBox="0 0 340 100" width="{round(size*3.4)}" height="{size}">'
            f'{campo_r}{polilinea(P, CN, g, ink, desplaza=(d, d))}'
            f'<text x="124" y="64" font-family="{F}" font-size="42" fill="{ink}">'
            f'C.F.D.L.</text></svg>')

cs = []
for k, N, v, cr in FIN:
    cs.append(f'<div class="c"><span class="caja b-blanco">{linea(N,v,cr,None,NEGRO)}</span>'
              f'<div class="et">{k} · sobre blanco</div></div>')
for k, N, v, cr in FIN:
    cs.append(f'<div class="c"><span class="caja b-negro">{linea(N,v,cr,None,AMBAR)}</span>'
              f'<div class="et">{k} · sobre negro</div></div>')
sec("junto a las siglas", "el caso de una firma o un pie", cs)

print(f'''<!doctype html><meta charset="utf-8"><title>ronda 9</title><style>
@font-face{{font-family:'FuturaStd';src:url('../../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');font-display:block}}
*{{box-sizing:border-box}}body{{margin:0;padding:30px 34px;background:#13131a;color:#e6e6ef;font:14px/1.6 system-ui}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 6px}}
h2{{font:400 11px/1 system-ui;letter-spacing:.2em;text-transform:uppercase;color:#e6e6ef;
   margin:32px 0 14px;border-top:1px solid #2a2a38;padding-top:14px;display:flex;
   justify-content:space-between;align-items:baseline;gap:20px}}
h2 span{{font:400 11.5px/1.4 system-ui;letter-spacing:0;text-transform:none;color:#83839b;text-align:right;max-width:500px}}
.intro{{color:#9a9ab0;max-width:900px;margin:0}} .intro b{{color:#e6e6ef;font-weight:500}}
.fila{{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end}}
.c{{text-align:center;line-height:0}} .c svg{{display:block}}
.k{{font:400 17px/1 system-ui;color:#ffb923;margin-bottom:8px}}
.et{{font:400 10px/1.4 system-ui;color:#6f6f88;margin-top:7px}}
.caja{{display:inline-block;line-height:0;padding:9px}}
.b-blanco{{background:#fff}} .b-negro{{background:#171513}}
.circ{{border-radius:50%;overflow:hidden;display:inline-block;line-height:0}}
</style>
<h1>C.F.D.L. — finalistas</h1>
<p class="intro"><b>Corregido</b> el error de medida de la ronda anterior: el hueco
se leía sólo en los últimos vértices, que describen el vacío únicamente cuando hay
pocas vueltas — por eso la «búsqueda por cálculo» sólo devolvía casos de 2¼.<br>
Y lo que sí vale: <b>2½–3 vueltas tienen mucha más presencia que 3½–4¾</b>. Lo denso
se lee como textura; lo escaso, como signo.</p>
{"".join(S)}
''')
