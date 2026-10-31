#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — ajuste de la firma: los tres parámetros, medidos.

  sep    hueco entre símbolo y pie, en anchos de símbolo
  track  interletrado dentro de C.F.D.L., en em
  rel    alto del símbolo ÷ altura de mayúscula

La regla que los ata: el hueco entre símbolo y pie tiene que leerse como MAYOR
que el hueco entre letras. Si no, el símbolo se incorpora a la cadena como un
signo más en vez de presidirla. Con sep 0,14 el hueco era 2,5 veces el
interletrado — demasiado poco para que se separen.

Cada muestra lleva debajo lo que ese hueco mide de verdad, en cuatro unidades,
para que la decisión no dependa de la impresión.
"""
from lockup import (firma, DENSIDAD, CAP_EM, ancho_siglas, AMBAR, NEGRO,
                    ZAFIRO, BLANCO, CREMA)

DENS = "medio"
TR0 = DENSIDAD[DENS]["track"]          # 0.135 em
ANCHO_C = 0.717                        # avance de la «C», en em


def medidas(rel, sep, track):
    """El hueco símbolo↔pie, en las unidades que importan."""
    S = 100.0
    cap = S / rel
    fs = cap / CAP_EM
    hueco = S * sep
    letra = track * fs                 # hueco entre letras, en unidades
    return dict(
        cap=hueco / cap,               # en alturas de mayúscula
        letras=(hueco / letra) if letra else float("inf"),   # veces el interletrado
        c=hueco / (ANCHO_C * fs),      # en anchos de «C»
        px=hueco,
    )


def et_sep(rel, sep, track):
    m = medidas(rel, sep, track)
    v = "∞" if m["letras"] == float("inf") else f"{m['letras']:.1f}×"
    return (f"sep {sep:.2f}<br><span class=n>{m['cap']:.2f} may · {v} interletra "
            f"· {m['c']:.2f} anchos de C</span>")


S = []
def sec(t, n, cuerpo): S.append(f'<section><h2>{t}<span>{n}</span></h2>{cuerpo}</section>')
def fila(cs): return f'<div class="fila">{"".join(cs)}</div>'
def c(sv, et, css="b-blanco"):
    return f'<div class="c"><span class="caja {css}">{sv}</span><div class="et">{et}</div></div>'

# ── 1 · separación símbolo ↔ pie ───────────────────────────────────────────
sec("Separación símbolo ↔ pie", "lo que se ve corto ahora — el rango va mucho "
    "más allá de lo que tenía",
  fila([c(firma(DENS, alto=62, rel=3.2, sep=s), et_sep(3.2, s, TR0))
        for s in (0.10, 0.14, 0.20, 0.26, 0.34, 0.44, 0.56, 0.70)])
  + '<p class="nota">La regla: el hueco debe leerse como <b>mayor que el que hay '
    'entre letras</b>. Por debajo de unas 4 veces el interletrado, el símbolo se '
    'incorpora a la cadena. Otra referencia clásica: el hueco ≈ el ancho de una '
    'mayúscula, o más.</p>')

# ── 2 · interletrado ───────────────────────────────────────────────────────
sec("Interletrado de C.F.D.L.", "la letra abierta es estilo de la casa; aquí "
    "se ve cuánto aguanta",
  fila([c(firma(DENS, alto=62, rel=3.2, sep=0.34, track=t),
          f"track {t:.3f} em<br><span class=n>ancho siglas {ancho_siglas(t):.2f} em</span>")
        for t in (0.0, 0.06, 0.135, 0.20, 0.28, 0.36, 0.46)]))

# ── 3 · tamaño relativo ────────────────────────────────────────────────────
sec("Tamaño relativo símbolo / letras", "alto del símbolo ÷ altura de mayúscula",
  fila([c(firma(DENS, alto=62, rel=r, sep=0.34),
          f"rel {r:.1f}<br><span class=n>mayúscula {100/r:.0f} de 100</span>")
        for r in (2.0, 2.4, 2.8, 3.2, 3.6, 4.0, 4.6, 5.2)]))

# ── 4 · matriz sep × rel ───────────────────────────────────────────────────
filas = []
for r in (2.4, 2.8, 3.2, 3.6, 4.2):
    cel = "".join(f'<td><span class="caja b-blanco">'
                  f'{firma(DENS, alto=44, rel=r, sep=s)}</span></td>'
                  for s in (0.16, 0.24, 0.34, 0.46, 0.60))
    filas.append(f'<tr><th class="lat">rel {r}</th>{cel}</tr>')
enc = "".join(f'<th>sep {s}</th>' for s in (0.16, 0.24, 0.34, 0.46, 0.60))
sec("Separación × tamaño relativo", "cómo se afectan: un pie más pequeño pide "
    "más aire, no menos",
  f'<div class="scroll"><table class="mx"><tr><th></th>{enc}</tr>'
  f'{"".join(filas)}</table></div>')

# ── 5 · matriz sep × interletrado ──────────────────────────────────────────
filas = []
for t in (0.0, 0.135, 0.24, 0.36):
    cel = "".join(f'<td><span class="caja b-blanco">'
                  f'{firma(DENS, alto=44, rel=3.2, sep=s, track=t)}</span></td>'
                  for s in (0.16, 0.24, 0.34, 0.46, 0.60))
    filas.append(f'<tr><th class="lat">track {t:.3f}</th>{cel}</tr>')
sec("Separación × interletrado", "los dos huecos compiten: si la letra va muy "
    "abierta, el hueco del símbolo tiene que abrirse más todavía",
  f'<div class="scroll"><table class="mx"><tr><th></th>{enc}</tr>'
  f'{"".join(filas)}</table></div>')

# ── 6 · candidatas ─────────────────────────────────────────────────────────
CAND = [("A", 3.2, 0.34, 0.135), ("B", 3.2, 0.44, 0.135),
        ("C", 2.8, 0.34, 0.20),  ("D", 3.6, 0.44, 0.135),
        ("E", 3.2, 0.34, 0.24),  ("F", 2.8, 0.26, 0.135)]
sec("Candidatas", "a tamaño de uso y a 34 px, sobre claro y sobre oscuro",
  fila([c(firma(DENS, alto=66, rel=r, sep=s, track=t),
          f"{k} · rel {r} · sep {s} · track {t}") for k, r, s, t in CAND])
  + fila([c(firma(DENS, alto=34, rel=r, sep=s, track=t), k) for k, r, s, t in CAND])
  + fila([c(firma(DENS, alto=52, rel=r, sep=s, track=t, tinta=AMBAR), k, "b-negro")
          for k, r, s, t in CAND]))

print(f'''<!doctype html><meta charset="utf-8"><title>C.F.D.L. — ajuste de la firma</title>
<style>
@font-face{{font-family:'FuturaStd';
  src:url('../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');font-display:block}}
*{{box-sizing:border-box}}
body{{margin:0;padding:36px 40px 80px;background:#12110f;color:#eae5dc;
  font:14px/1.6 system-ui,sans-serif}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 8px}}
h2{{font:400 12px/1 system-ui;letter-spacing:.2em;text-transform:uppercase;color:#ffb923;
  margin:0 0 18px;display:flex;justify-content:space-between;align-items:baseline;gap:24px}}
h2 span{{font:400 12px/1.4 system-ui;letter-spacing:0;text-transform:none;
  color:#8b8275;text-align:right;max-width:440px}}
section{{border-top:1px solid #2b2823;padding:26px 0 10px}}
.intro{{color:#9c9286;max-width:80ch;margin:0 0 6px}} .intro b{{color:#eae5dc;font-weight:500}}
p{{max-width:80ch;color:#9c9286}} p b{{color:#eae5dc;font-weight:500}}
.fila{{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start;margin:6px 0}}
.c{{text-align:center;line-height:0;max-width:260px}}
.caja{{display:inline-block;line-height:0;padding:11px}}
.b-blanco{{background:#fff}} .b-negro{{background:#171513}}
.et{{font:400 10.5px/1.45 system-ui;color:#a89e90;margin-top:9px}}
.et .n{{color:#6f675b;font-variant-numeric:tabular-nums}}
.scroll{{overflow-x:auto;margin:4px 0}}
table.mx{{border-collapse:collapse}}
table.mx th{{font:400 10px/1 system-ui;letter-spacing:.14em;text-transform:uppercase;
  color:#7d7568;padding:8px 10px;font-weight:400;white-space:nowrap}}
table.mx th.lat{{text-align:right}}
table.mx td{{padding:6px 8px}}
.nota{{border-top:1px solid #2b2823;margin-top:20px;padding-top:13px;font-size:13.5px}}
</style>
<h1>C.F.D.L. — ajuste de la firma</h1>
<p class="intro">Tres parámetros, y se afectan entre sí. Cada muestra lleva debajo
<b>lo que ese hueco mide de verdad</b> —en alturas de mayúscula, en veces el
interletrado y en anchos de «C»— para que la decisión no dependa de la impresión
que dé en pantalla.</p>
{"".join(S)}
''')
