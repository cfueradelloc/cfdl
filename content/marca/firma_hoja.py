#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — la firma: hoja de normas y variantes."""
from lockup import (firma, simbolo, gris_simbolo, ancho_siglas, DENSIDAD,
                    CAP_EM, ASTA_EM, AMBAR, NEGRO, ZAFIRO, BLANCO, CREMA)

S = []
def sec(t, n, cuerpo):
    S.append(f'<section><h2>{t}<span>{n}</span></h2>{cuerpo}</section>')
def fila(cs): return f'<div class="fila">{"".join(cs)}</div>'
def c(sv, et, css=""):
    return f'<div class="c"><span class="caja {css}">{sv}</span><div class="et">{et}</div></div>'

GROUNDS = [("b-blanco", BLANCO, NEGRO, "blanco"), ("b-negro", NEGRO, AMBAR, "negro"),
           ("b-ambar", AMBAR, NEGRO, "ámbar"), ("b-rosa", "#f8ccce", ZAFIRO, "rosa"),
           ("b-zafiro", ZAFIRO, CREMA, "zafiro")]

# ── 1 · el gris ────────────────────────────────────────────────────────────
tabla = "".join(
  f'<tr><td>{k}</td><td>{DENSIDAD[k]["anillos"]} anillos 1:{DENSIDAD[k]["hu"]}</td>'
  f'<td class="n">{100*gris_simbolo(k):.1f}&nbsp;%</td>'
  f'<td class="n">{DENSIDAD[k]["track"]:.3f} em</td>'
  f'<td class="n">{ancho_siglas(DENSIDAD[k]["track"]):.2f} em</td></tr>'
  for k in DENSIDAD)
sec("El gris manda", "igualar grosores es imposible; igualar el gris, no",
  f'''<p>El asta de Futura Book mide <b>0,084&nbsp;em</b> y la mayúscula
  <b>0,754&nbsp;em</b>: el asta es el <b>11,1&nbsp;%</b> de la mayúscula. Para que
  la línea de la espiral pesara eso harían falta 2–3 anillos, no siete — la banda
  fina, que es la que significa algo, es forzosamente más ligera que la letra.</p>
  <p>Así que no se igualan los grosores: se iguala el <b>gris</b>. Se mide qué
  fracción de su caja ocupa de tinta cada uno y se abre el interletrado de las
  siglas hasta que coinciden. Abrir las versalitas ya era el estilo de la casa
  para las etiquetas; ahora tiene un número detrás.</p>
  <table><thead><tr><th>densidad</th><th>símbolo</th><th class="n">gris</th>
  <th class="n">interletrado</th><th class="n">ancho siglas</th></tr></thead>
  <tbody>{tabla}</tbody></table>
  <div class="fila comp">
    {c(firma("grande", alto=58, rel=3.2, alinea="centro"), "pie pequeño — la jerarquía clara", "b-blanco")}
    {c(firma("grande", alto=58, rel=1.3), "rel 1,3 — compiten como iguales", "b-blanco mal")}
  </div>''')

# ── 2 · la firma principal ─────────────────────────────────────────────────
sec("La firma", "media · rel 3,20 · pie centrado · separación 0,14",
  fila([c(firma(d, alto=68, rel=3.2, alinea="centro"),
          f"{d} · {DENSIDAD[d]['anillos']} anillos", "b-blanco")
        for d in DENSIDAD]))

# ── 3 · proporción símbolo / mayúscula ─────────────────────────────────────
sec("Alto del símbolo", "el símbolo dividido por la altura de mayúscula — la "
    "decisión de jerarquía",
  fila([c(firma("grande", alto=54, rel=r, alinea="base"), f"rel {r}", "b-blanco")
        for r in (1.0, 1.3, 1.8, 2.2, 2.6, 3.0, 3.2, 3.6, 4.0, 4.6)])
  + '''<p class="nota">Por debajo de ~2,5 los dos elementos compiten como
  iguales y el ojo tiene que decidir cuál es el logotipo. Por encima, la
  jerarquía es inequívoca: <b>el símbolo es la marca y las siglas son su
  pie</b> — que es lo que corresponde cuando el significado lo carga el
  símbolo. Más cerca de un colofón que de un lockup.</p>''')

# ── 3b · dónde se apoya el pie ─────────────────────────────────────────────
sec("Dónde se apoya el pie", "con la letra pequeña, centrarla la deja flotando",
  fila([c(firma("grande", alto=60, rel=3.2, alinea=a), et, "b-blanco")
        for a, et in (("centro","centro — flota"),
                      ("base","base — se asienta en la línea que cierra la espiral"),
                      ("alto","alto — cuelga del borde superior"))]))

# ── 4 · separación ─────────────────────────────────────────────────────────
sec("Separación", "aire entre símbolo y siglas, en ANCHOS DE SÍMBOLO — en alturas de mayúscula encogía con el pie",
  fila([c(firma("grande", alto=60, rel=3.2, alinea="centro", sep=s), f"sep {s}", "b-blanco")
        for s in (0.06, 0.10, 0.14, 0.18, 0.24, 0.32)]))

# ── 4b · interletrado del pie ──────────────────────────────────────────────
sec("Interletrado del pie", "a este tamaño ya no iguala grises: ahora es "
    "legibilidad y estilo de la casa",
  fila([c(firma("grande", alto=60, rel=3.2, alinea="centro", track=t),
          f"{t:.2f} em", "b-blanco")
        for t in (0.0, 0.10, 0.18, 0.26, 0.32, 0.42)]))

# ── 5 · el símbolo solo ────────────────────────────────────────────────────
sec("El símbolo solo", "sin siglas — avatar, favicon, sello",
  fila([c(firma(d, alto=96, con_siglas=False), d, "b-blanco") for d in DENSIDAD]
     + [c(f'<span class="circ">{firma("grande", alto=104, con_siglas=False, campo=AMBAR, respiro=0.11)}</span>',
          "círculo · respiro 0,11")]
     + [c(f'<span class="circ">{firma("grande", alto=104, con_siglas=False, campo=AMBAR)}</span>',
          "sin respiro — pierde esquinas", "mal")]))

# ── 7 · escala ─────────────────────────────────────────────────────────────
esc = []
for a, d in ((132,"grande"),(96,"grande"),(64,"grande"),(48,"medio"),(34,"medio"),(24,"pequeno")):
    esc.append(c(firma(d, alto=a, rel=3.2, alinea="centro"), f"{a} px · {d}", "b-blanco"))
sec("Escala", "la densidad baja con el tamaño — es el mismo signo",
    fila(esc) + '<p class="nota">Por debajo de ~24&nbsp;px con siglas, y de ~16&nbsp;px '
    'sólo símbolo, la espiral deja de leerse como espiral y queda un marco. '
    'Se conserva el centro vacío, que es lo que significa.</p>')

# ── 8 · área de respeto ────────────────────────────────────────────────────
sec("Área de respeto", "nada entra a menos de media altura de símbolo",
  fila([c(f'<span class="respeto">{firma("grande", alto=58, rel=3.2, alinea="centro", respeto=r)}</span>',
          f"respeto {r}", "b-blanco") for r in (0.0, 0.25, 0.50)]))

# ── 9 · color ──────────────────────────────────────────────────────────────
sec("Color", "cada fondo con la tinta que le sirve",
  fila([c(firma("grande", alto=56, rel=3.2, alinea="centro", tinta=ink), nom, css)
        for css, bg, ink, nom in GROUNDS])
  + fila([c(firma("grande", alto=56, rel=3.2, alinea="centro", tinta=NEGRO, campo=AMBAR, fondo_firma=AMBAR),
            "con campo ámbar", "b-blanco"),
          c(firma("grande", alto=56, rel=3.2, alinea="centro", tinta=AMBAR, campo=NEGRO, fondo_firma=NEGRO),
            "con campo negro", "b-blanco"),
          c(firma("grande", alto=56, rel=3.2, alinea="centro", tinta=ZAFIRO), "zafiro sobre rosa", "b-rosa")]))

# ── 10 · usos incorrectos ──────────────────────────────────────────────────
sec("Lo que no",
  "cada uno rompe una de las reglas de arriba",
  fila([
    c(firma("grande", alto=52, rel=3.2, alinea="centro"), "pie flotando a media altura", "b-blanco mal"),
    c(firma("grande", alto=52, rel=5.5, alinea="base"), "rel 5,5 — el pie desaparece", "b-blanco mal"),
    c(firma("grande", alto=52, rel=1.0), "rel 1,0 — la letra se come al símbolo", "b-blanco mal"),
    c(firma("grande", alto=52, rel=3.2, alinea="centro", sep=0.12), "sin aire: se leen como una pieza", "b-blanco mal"),
    c(firma("grande", alto=24, rel=3.2, alinea="centro"), "fina a 24 px: se empasta", "b-blanco mal"),
  ]))

print(f'''<!doctype html><meta charset="utf-8"><title>C.F.D.L. — la firma</title>
<style>
@font-face{{font-family:'FuturaStd';
  src:url('../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');font-display:block}}
*{{box-sizing:border-box}}
body{{margin:0;padding:36px 40px 80px;background:#12110f;color:#eae5dc;
  font:14px/1.6 system-ui,sans-serif}}
h1{{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;margin:0 0 8px}}
h2{{font:400 12px/1 system-ui;letter-spacing:.2em;text-transform:uppercase;color:#ffb923;
  margin:0 0 16px;display:flex;justify-content:space-between;align-items:baseline;gap:24px}}
h2 span{{font:400 12px/1.4 system-ui;letter-spacing:0;text-transform:none;
  color:#8b8275;text-align:right;max-width:420px}}
section{{border-top:1px solid #2b2823;padding:26px 0 10px}}
.intro{{color:#9c9286;max-width:78ch;margin:0 0 6px}} .intro b{{color:#eae5dc;font-weight:500}}
p{{max-width:78ch;color:#9c9286}} p b{{color:#eae5dc;font-weight:500}}
.fila{{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-end;margin:6px 0 4px}}
.fila.comp{{gap:26px}}
.c{{text-align:center;line-height:0}}
.caja{{display:inline-block;line-height:0;padding:11px}}
.b-blanco{{background:#fff}} .b-negro{{background:#171513}} .b-ambar{{background:#ffb923}}
.b-rosa{{background:#f8ccce}} .b-zafiro{{background:#332f8a}}
.mal{{outline:1.5px solid #e0566f;outline-offset:3px}}
.circ{{border-radius:50%;overflow:hidden;display:inline-block;line-height:0}}
.respeto{{display:inline-block;line-height:0;outline:1px dashed #4a90d9;outline-offset:0}}
.et{{font:400 10.5px/1.4 system-ui;color:#7d7568;margin-top:9px;max-width:200px}}
table{{border-collapse:collapse;margin:18px 0 10px;font-size:13.5px}}
th,td{{text-align:left;padding:7px 20px 7px 0;border-bottom:1px solid #2b2823}}
th{{font:400 10px/1 system-ui;letter-spacing:.16em;text-transform:uppercase;color:#7d7568}}
td{{color:#c9c2b6}} .n{{text-align:right;font-variant-numeric:tabular-nums}}
.nota{{border-top:1px solid #2b2823;margin-top:18px;padding-top:12px;font-size:13.5px}}
</style>
<h1>C.F.D.L. — la firma</h1>
<p class="intro">El símbolo es una banda de líneas finas; las siglas son versalitas
macizas. Juntarlas sin regla deja al símbolo sin voz. Todo lo que sigue sale de una
sola decisión: <b>no se igualan los grosores, se iguala el gris</b>.</p>
{"".join(S)}
''')
