#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — la página de la marca.

Esto es lo que hay que mirar: la marca tal como queda, y dónde están los
archivos. Las páginas de trabajo —cómo se construyó, el barrido de ajustes, el
explorador— van al pie, porque son para quien quiera entrar, no para quien
quiera usarla.
"""
import os
from lockup import firma, AMBAR, NEGRO, ZAFIRO, BLANCO, CREMA

AQUI = os.path.dirname(os.path.abspath(__file__))


def _fig(sv, et, css=""):
    return (f'<figure class="{css}"><div class="l">{sv}</div>'
            f'<figcaption>{et}</figcaption></figure>')


def pagina():
    p = []

    # ── la firma, a tamaño de verdad ───────────────────────────────────────
    p.append('<section class="hero">'
             f'<div class="l">{firma("media", alto=124)}</div>'
             '<p class="ph">La firma. Símbolo y siglas — el uso principal.</p>'
             '</section>')

    # ── sobre cada fondo ───────────────────────────────────────────────────
    p.append('<section><h2>Sobre cada fondo</h2><div class="rej">')
    for css, tinta, et in (("f-blanco", NEGRO, "negro sobre blanco"),
                           ("f-negro",  AMBAR, "ámbar sobre negro"),
                           ("f-ambar",  NEGRO, "negro sobre ámbar"),
                           ("f-rosa",   ZAFIRO, "zafiro sobre rosa"),
                           ("f-zafiro", CREMA, "crema sobre zafiro")):
        p.append(_fig(firma("media", alto=58, tinta=tinta), et, css))
    p.append('</div></section>')

    # ── el símbolo solo ────────────────────────────────────────────────────
    p.append('<section><h2>El símbolo solo</h2><div class="rej">')
    p.append(_fig('<span class="circ">'
                  + firma("media", alto=120, con_siglas=False,
                          campo=AMBAR, respiro=0.11) + '</span>',
                  "foto de perfil — cabe entera en el círculo", "f-claro"))
    p.append(_fig(firma("media", alto=104, con_siglas=False, campo=AMBAR),
                  "con campo", "f-claro"))
    p.append(_fig(firma("media", alto=104, con_siglas=False),
                  "sin campo", "f-blanco"))
    p.append(_fig(firma("gruesa", alto=104, con_siglas=False, campo=AMBAR),
                  "favicon — menos anillos", "f-claro"))
    p.append('</div></section>')

    # ── tamaños ────────────────────────────────────────────────────────────
    p.append('<section><h2>Tamaños</h2><div class="rej abajo">')
    for a, d, et in ((104, "media", "104 px"), (68, "media", "68 px"),
                     (46, "media", "46 px"), (30, "gruesa", "30 px")):
        p.append(_fig(firma(d, alto=a), et, "f-blanco"))
    p.append('</div><p class="nota">Por debajo de unos 24&nbsp;px la espiral deja '
             'de leerse como espiral y queda un marco. Se conserva el centro '
             'vacío, que es lo que significa.</p></section>')

    # ── el ajuste, en una línea ────────────────────────────────────────────
    p.append('<section><h2>El ajuste</h2><table class="aj">'
             '<tr><td>alto del símbolo</td><td>3,20 × la altura de mayúscula</td></tr>'
             '<tr><td>separación</td><td>0,40 anchos de símbolo'
             ' <i>— 1,35 mayúsculas, 4,8× el hueco entre letras</i></td></tr>'
             '<tr><td>interletrado</td><td>0,200 em</td></tr>'
             '<tr><td>centrado</td><td>mismo aire por encima y por debajo de las '
             'letras <i>— comprobado midiendo píxeles</i></td></tr>'
             '</table></section>')

    # ── archivos ───────────────────────────────────────────────────────────
    p.append('<section><h2>Los archivos</h2><div class="arch">'
             '<div><b>svg/</b><span>16 combinaciones. El SVG es el maestro: escala '
             'sin perder nada, y con <code>tinta="auto"</code> hereda el color del '
             'texto que lo rodea.</span></div>'
             '<div><b>png/</b><span><code>perfil-instagram</code> 1080&nbsp;· '
             '<code>linea-negro</code> y <code>linea-blanco</code> 663×200&nbsp;· '
             '<code>favicon-32</code> y <code>favicon-180</code>&nbsp;· '
             '<code>monograma-512</code>&nbsp;· <code>hoja</code></span></div>'
             '<div><b>para regenerar</b><span><code>python3 marca.py</code> rehace '
             'los SVG y esta página. <code>bash exportar_png.sh</code>, los '
             'PNG.</span></div>'
             '</div></section>')

    with open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(PLANTILLA.replace("{cuerpo}", "".join(p)))
    print("página → content/marca/index.html")


PLANTILLA = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>C.F.D.L. — la marca</title>
<style>
@font-face{font-family:'FuturaStd';
  src:url('../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');
  font-display:block}
:root{
  --papel:#faf7f1; --papel2:#f2eee6; --tinta:#1b1713; --tinta2:#6d6459;
  --tinta3:#9b9184; --linea:#e2dbcf;
}
@media (prefers-color-scheme:dark){:root{
  --papel:#141210; --papel2:#1d1a16; --tinta:#efe9e0; --tinta2:#a79d8f;
  --tinta3:#7c7365; --linea:#2d2924;}}
*{box-sizing:border-box}
body{margin:0;background:var(--papel);color:var(--tinta);
  font:400 16px/1.6 ui-sans-serif,system-ui,sans-serif}
.h{max-width:1000px;margin:0 auto;padding:60px 32px 90px}
.et{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--tinta3)}
h1{font:400 34px/1.1 ui-sans-serif,system-ui;letter-spacing:.02em;margin:12px 0 0}
.baj{color:var(--tinta2);max-width:60ch;margin:14px 0 0}
header{border-bottom:1px solid var(--linea);padding-bottom:34px}
section{border-bottom:1px solid var(--linea);padding:40px 0}
section:last-of-type{border-bottom:0}
h2{font:400 11px/1 ui-sans-serif,system-ui;letter-spacing:.22em;
  text-transform:uppercase;color:var(--tinta3);margin:0 0 24px}
.hero{text-align:center;padding:52px 0 44px}
.hero .l{display:inline-block;line-height:0;background:#fff;padding:34px 44px}
.ph{color:var(--tinta2);font-size:14px;margin:20px 0 0}
.rej{display:flex;flex-wrap:wrap;gap:22px;align-items:flex-start}
.rej.abajo{align-items:flex-end}
figure{margin:0;text-align:center}
figure .l{line-height:0;padding:16px 20px;display:block;border-radius:2px}
figcaption{font-size:11.5px;color:var(--tinta2);margin-top:10px;max-width:210px}
.f-blanco .l{background:#fff} .f-negro .l{background:#171513}
.f-ambar .l{background:#ffb923} .f-rosa .l{background:#f8ccce}
.f-zafiro .l{background:#332f8a} .f-claro .l{background:var(--papel2)}
.circ{border-radius:50%;overflow:hidden;display:inline-block;line-height:0}
.nota{font-size:13.5px;color:var(--tinta2);margin:24px 0 0;max-width:62ch}
table.aj{border-collapse:collapse;font-size:14.5px}
table.aj td{padding:9px 28px 9px 0;border-bottom:1px solid var(--linea);
  vertical-align:baseline}
table.aj td:first-child{color:var(--tinta3);white-space:nowrap;
  font-size:11px;letter-spacing:.16em;text-transform:uppercase}
table.aj i{font-style:normal;color:var(--tinta3);font-size:13px}
.arch{display:grid;gap:18px}
.arch div{display:grid;grid-template-columns:150px 1fr;gap:18px;
  align-items:baseline}
.arch b{font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--tinta3);font-weight:400}
.arch span{color:var(--tinta2);font-size:14.5px}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;
  background:var(--papel2);padding:1px 6px;border-radius:3px;color:var(--tinta)}
footer{border-top:1px solid var(--linea);margin-top:56px;padding-top:22px;
  font-size:13px;color:var(--tinta3)}
footer a{color:var(--tinta2);text-decoration:none;border-bottom:1px solid var(--linea)}
footer a:hover{color:var(--tinta)}
footer p{margin:0 0 8px}
:focus-visible{outline:2px solid var(--tinta);outline-offset:3px}
@media (max-width:620px){.arch div{grid-template-columns:1fr;gap:4px}}
</style></head><body><div class="h">

<header>
  <div class="et">Colectivo Fuera de Lugar · Col·lectiu Fora de Lloc</div>
  <h1>La marca</h1>
  <p class="baj">La espiral del manifiesto impreso: el texto vive en el margen y
  el centro queda vacío. Propuesta — el sitio y lo impreso siguen con el
  logotipo anterior.</p>
</header>

{cuerpo}

<footer>
  <p>Cómo se llegó hasta aquí, por si hace falta entrar:</p>
  <p><a href="firma.html">construcción de la firma</a> ·
     <a href="ajuste.html">barrido de ajustes</a> ·
     <a href="explorador.html">explorador de variantes</a> ·
     <a href="analisis.html">medidas del dibujo</a> ·
     <a href="rondas.html">rondas descartadas</a></p>
</footer>

</div></body></html>
"""

if __name__ == "__main__":
    pagina()
