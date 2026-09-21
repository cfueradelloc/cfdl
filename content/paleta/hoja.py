#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — la página de la paleta.

La página está hecha CON la paleta que propone. Es la única prueba que vale:
una muestra de cuarenta píxeles no dice nada sobre un color de fondo, y un
color que sólo funciona en su propia ficha no funciona.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "marca"))

from color import lch, contraste, nivel, distancia, salto_matiz, desde_lch
from paleta import (PALETA, HEX, GRUPOS, ROLES, CICLOS, PAREJAS,
                    PAREJAS_UI, RETIRADOS, verificar)

try:
    from lockup import firma
    HAY_MARCA = True
except Exception:                                    # pragma: no cover
    HAY_MARCA = False

P = HEX
TOPICO = "#f4f1ea"      # el crema que hoy delata un diseño hecho a máquina


def _n(x):
    return f"{x:.2f}".replace(".", ",")


# ── 1 · la paleta ──────────────────────────────────────────────────────────
def s_paleta():
    p = ['<section><h2>Once tonos, en tres grupos</h2>']
    leyenda = {
        "neutro": "La rampa. Hace el trabajo callado —fondos, superficies, "
                  "bordes, estados— y por eso son seis de once. Van en el "
                  "matiz del ámbar a croma 6–7: a ese croma no se leen como "
                  "otro color cálido, se leen como grises, pero grises del "
                  "mismo papel.",
        "color": "Los cinco que hablan. <b>Ámbar y zafiro son del colectivo</b>; "
                 "los otros tres son bandas de ciclo. Cada uno manda en su "
                 "sitio y ninguno comparte superficie a igual área con otro.",
        "sobre oscuro": "Sólo tienen sentido encima de zafiro o de tinta. "
                        "Sobre papel son invisibles, y está bien que lo sean.",
    }
    for g in GRUPOS:
        p.append(f'<h3>{g}</h3><p class="ent">{leyenda[g]}</p><div class="rej">')
        for n, h, papel, gr, origen in PALETA:
            if gr != g:
                continue
            L, C, H = lch(h)
            et = ('<b class="nv">nuevo</b>' if origen.startswith("nuevo")
                  else '<b class="nv">revisado</b>' if origen.startswith("revisado")
                  else '')
            p.append(f'<figure class="mu"><div class="ch" style="background:{h}">'
                     f'</div><figcaption><b>{n}</b>{et}<code>{h}</code>'
                     f'<span class="num">L*{L:.1f} · C*{C:.1f} · h{H:.0f}°</span>'
                     f'<span class="pa">{papel}</span>'
                     f'<span class="or">{origen}</span></figcaption></figure>')
        p.append('</div>')
    p.append('</section>')
    return "".join(p)


# ── 2 · la rampa ───────────────────────────────────────────────────────────
def s_rampa():
    ramp = [(n, h) for n, h, _, g, _ in PALETA if g == "neutro"]
    p = ['<section><h2>El gris que faltaba</h2>'
         '<p class="ent">El primer reparto tenía siete cromáticos y tres '
         'neutros, que es al revés de como se construye un sistema. Entre '
         '<b>L*97 y L*42 había cincuenta y cinco puntos sin un solo tono</b> — '
         'justo donde viven los bordes, los separadores, los estados inactivos '
         'y las rejillas. Sin ellos hay que tirar de color para todo: la '
         'superficie acaba rosa y el borde lavanda, y una ficha de evento '
         'grita cuando debería susurrar.</p><div class="ramp">']
    for n, h in ramp:
        L = lch(h)[0]
        p.append(f'<div style="background:{h};color:{"#171513" if L > 55 else "#fdf5eb"}">'
                 f'<span>{n}</span><span class="l">L*{L:.0f}</span></div>')
    p.append('</div>')
    p.append('<div class="dos">'
             '<div><div class="ficha"><div class="k">Lectura — La Perecquiana</div>'
             '<h4>Crear donde no alcance ninguna raíz</h4>'
             '<div class="m">Viernes 12 de diciembre, 19:30</div><hr>'
             '<div class="ina">Plazas agotadas</div></div>'
             '<p class="pie">Con rampa: la superficie es <b>hueso</b>, el borde '
             'y el filete <b>filete</b>, el estado agotado <b>ceniza</b>. Tres '
             'grados de gris haciendo tres trabajos, y el color libre para '
             'cuando importe.</p></div>'
             '<div><div class="ficha mal"><div class="k">Lectura — La Perecquiana</div>'
             '<h4>Crear donde no alcance ninguna raíz</h4>'
             '<div class="m">Viernes 12 de diciembre, 19:30</div><hr>'
             '<div class="m">Plazas agotadas</div></div>'
             '<p class="pie">Sin rampa no queda más remedio que usar color, y '
             'el estado agotado no se distingue del resto. Es la misma ficha.</p>'
             '</div></div>')
    p.append('<p class="nota"><b>Ceniza no llega al 3:1</b> que la norma pide '
             'para lo que no es texto — da ' + _n(contraste(P["ceniza"], P["papel"]))
             + ':1 sobre papel. No es un descuido: su trabajo son estados '
             'inactivos y filetes, y la norma exime expresamente los '
             'componentes inactivos y lo decorativo. Se probó bajarla a L*54 '
             'para que cumpliera, y entonces queda a 1,54:1 de humo y las dos '
             'se confunden. Un borde que <i>sí</i> tiene que verse —el contorno '
             'de un campo, una casilla— usa humo.</p></section>')
    return "".join(p)


# ── 3 · los papeles ────────────────────────────────────────────────────────
def s_roles():
    p = ['<section><h2>Qué va en cada sitio</h2>'
         '<p class="ent">Una paleta sin esto es una lista de colores bonitos.</p>'
         '<table class="ro"><tr><th>papel</th><th>sobre claro</th>'
         '<th>sobre oscuro</th><th></th></tr>']
    for rol, cl, osc, det in ROLES:
        p.append(f'<tr><td class="rn">{rol}</td>'
                 f'<td><i style="background:{P[cl]}"></i>{cl}</td>'
                 f'<td><i style="background:{P[osc]}"></i>{osc}</td>'
                 f'<td class="det">{det}</td></tr>')
    p.append('</table>'
             '<p class="nota">El aviso más útil de toda la paleta está en la '
             'fila del <b>foco</b>: el ámbar da '
             + _n(contraste(P["ámbar"], P["papel"])) + ':1 sobre papel, así que '
             '<b>no puede ser el anillo del teclado</b> — desaparece. El foco va '
             'en zafiro. El ámbar es el color de la marca, no el de la '
             'interfaz.</p></section>')
    return "".join(p)


# ── 4 · el diagnóstico ─────────────────────────────────────────────────────
def _rueda():
    import math
    R, r, cx, cy = 92, 60, 108, 108
    p = ['<svg viewBox="0 0 216 216" width="216" height="216" role="img" '
         'aria-label="Rueda de matices con zafiro en 301 grados, rosa en 17 '
         'y ámbar en 80">']
    for g in range(0, 360, 3):
        a0, a1 = math.radians(g - 1.45), math.radians(g + 1.45)
        col = desde_lch(72, 42, g)
        x1, y1 = cx + R * math.cos(a0), cy + R * math.sin(a0)
        x2, y2 = cx + R * math.cos(a1), cy + R * math.sin(a1)
        x3, y3 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x4, y4 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        p.append(f'<path d="M{x1:.1f} {y1:.1f}A{R} {R} 0 0 1 {x2:.1f} {y2:.1f}'
                 f'L{x3:.1f} {y3:.1f}A{r} {r} 0 0 0 {x4:.1f} {y4:.1f}Z" '
                 f'fill="{col}"/>')
    a1, a2 = math.radians(301), math.radians(80)
    p.append(f'<path d="M{cx+34*math.cos(a1):.1f} {cy+34*math.sin(a1):.1f}'
             f'A34 34 0 0 1 {cx+34*math.cos(a2):.1f} {cy+34*math.sin(a2):.1f}" '
             f'fill="none" stroke="{P["ceniza"]}" stroke-width="1.3" '
             f'stroke-dasharray="3 3"/>')
    for n, g in (("zafiro", 301), ("rosa", 17), ("ámbar", 80),
                 ("moho", 155), ("náufrago", 231)):
        a = math.radians(g)
        p.append(f'<line x1="{cx+r*math.cos(a):.1f}" y1="{cy+r*math.sin(a):.1f}" '
                 f'x2="{cx+(R+9)*math.cos(a):.1f}" y2="{cy+(R+9)*math.sin(a):.1f}" '
                 f'stroke="{P["tinta"]}" stroke-width="2"/>')
        p.append(f'<circle cx="{cx+(R+15)*math.cos(a):.1f}" '
                 f'cy="{cy+(R+15)*math.sin(a):.1f}" r="6.5" fill="{P[n]}" '
                 f'stroke="{P["tinta"]}" stroke-width="1.1"/>')
    p.append(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="12" '
             f'fill="{P["humo"]}">138°</text></svg>')
    return "".join(p)


def _par(a, b, na, nb, veredicto):
    c = contraste(a, b)
    return (f'<div class="pa2"><div class="pab">'
            f'<span style="background:{a}"></span>'
            f'<span style="background:{b}"></span></div>'
            f'<div><b>{na}</b> h{lch(a)[2]:.0f}° · <b>{nb}</b> h{lch(b)[2]:.0f}°'
            f'<span class="num">{salto_matiz(a,b):.0f}° de matiz · contraste '
            f'{_n(c)}:1</span><span class="ve">{veredicto}</span></div></div>')


def s_porque():
    za = salto_matiz(P["ámbar"], P["zafiro"])
    zr = salto_matiz(P["zafiro"], P["rosa"])
    ra = salto_matiz(P["rosa"], P["ámbar"])
    return (
        '<section><h2>Por qué una sola, y no dos</h2>'
        '<div class="dos rue"><div>' + _rueda() + '</div><div>'
        f'<p class="ent">La duda era si el ámbar y el zafiro son compatibles. '
        f'Están a <b>{za:.0f}°</b> de matiz. El complementario exacto del ámbar '
        f'sería azul puro, h 260°; el zafiro está en h 301°, violáceo, cuarenta '
        f'grados más allá. Eso no es un choque: es un <b>complementario '
        f'partido</b>, de los esquemas más sólidos que hay. Y contrastan '
        f'{_n(contraste(P["ámbar"], P["zafiro"]))}:1, apto para texto.</p>'
        '<p>Lo que fallaba no era el par: es que <b>nunca habían compartido '
        'suelo</b>. La paleta rosa aterrizaba en Candy Pink y la citrina en '
        'Niebla, dos fondos de familias distintas.</p>'
        f'<p>Y el escalón que los une ya estaba en casa. Del zafiro al rosa hay '
        f'<b>{zr:.0f}°</b>; del rosa al ámbar, <b>{ra:.0f}°</b>. El rosa cae casi '
        f'en medio del salto. No era un tercer color que sobraba: era el peldaño '
        f'que faltaba.</p></div></div>'
        '<h3>lo que sí sobraba: dos duplicados</h3><div class="pares">'
        + _par("#fde700", P["ámbar"], "Factory Yellow", "ámbar",
               "Dos amarillos que no se distinguen en valor. Cabe uno.")
        + _par(P["zafiro"], "#1a2e3d", "zafiro", "Medianoche",
               "Violáceo contra azul verdadero. Dos notas frías no pueden "
               "mandar a la vez.")
        + '</div><p class="nota">Quitando uno de cada par, la paleta se resuelve '
        'sola. No hizo falta inventar colores: la escala cálida ya estaba '
        'repartida por el repositorio —el negro de la imprenta, el ámbar, la '
        'cera— cubriendo de L*7 a L*96 en un solo matiz. Y las camisetas ya '
        'habían llegado por su cuenta a un blanco cálido, <code>#f1ece0</code>, '
        'metido a pelo en cuatrocientos trece sitios sin token ni nombre. La '
        'propuesta no inventa el suelo: le pone nombre al que ya se usaba.</p>'
        '</section>')


# ── 5 · el suelo ───────────────────────────────────────────────────────────
def s_suelo():
    p = ['<section><h2>El suelo, a área completa</h2>'
         '<p class="ent">Un fondo no se juzga en una muestra pequeña: a ese '
         'tamaño los tres de abajo parecen el mismo. Se juzga a área completa y '
         'con texto encima. Lo único que cambia entre ellos es el croma.</p>']
    for C, et in ((6, "C*6 — el propuesto"), (10, "C*10"), (14, "C*14")):
        h = desde_lch(96.9, C, 80)
        p.append(f'<div class="pr" style="background:{h}"><p>Escogemos la '
                 f'extenuación: de la palabra, de los recursos, de la energía '
                 f'corporal.</p><span>{et} — <code>{h}</code> · a ΔE '
                 f'{distancia(h, TOPICO):.1f} del crema genérico</span></div>')
    p.append('<p class="nota">Conviene decirlo: <code>' + P["papel"] + '</code> '
             'está a ΔE ' + f'{distancia(P["papel"], TOPICO):.1f}' + ' de '
             '<code>' + TOPICO + '</code>, el crema que hoy delata un diseño '
             'hecho a máquina. Se separa por ser más claro y más amarillo —está '
             'en la familia del ámbar, no en la del beige— pero el margen es '
             'estrecho. Subir el croma lo aleja del tópico y lo acerca al papel '
             'de embalar.</p></section>')
    return "".join(p)


# ── 6 · puesta a prueba ────────────────────────────────────────────────────
def s_prueba():
    # SIEMPRE uno de los tres tamaños de la marca. A 44 px la retícula de
    # «medio» deja el trazo en 0,44 px —sublpíxel— y el zafiro se ve lavado.
    # La marca tiene tres tamaños y sólo tres: 104, 60 y 30.
    def _m(tinta):
        return firma("medio", alto=60, tinta=tinta) if HAY_MARCA else ""
    marca_c, marca_a, marca_z = _m(P["tinta"]), _m(P["ámbar"]), _m(P["zafiro"])
    return (
        '<section><h2>Puesta a prueba</h2>'
        '<p class="ent">Lo único que decide de verdad. Los números no salvan una '
        'paleta que aplicada no se sostiene.</p>'
        # cabecera de sitio
        '<div class="ap"><div class="web">'
        f'<div class="wbar"><div class="wm">{marca_a}</div>'
        '<nav>manifiesto · proyectos · eventos · galería</nav></div>'
        '<div class="wbody"><h4>Ante la síntesis, la disgregación</h4>'
        '<p>Escogemos la extenuación: de la palabra, de los recursos, de la '
        'energía corporal. Reivindicamos la libertad perdida a posta.</p>'
        '<div class="wmeta">Exposición colectiva — Sala d\'Art Jove, Barcelona'
        '</div><div class="wrule"></div></div></div>'
        '<p class="pie">Una página: banda zafiro con la marca en ámbar, cuerpo '
        'sobre papel, pie en humo, filete en ámbar.</p></div>'
        # post e insignia
        '<div class="dos ap">'
        '<div><div class="post"><div class="pk">Lectura — La Perecquiana, '
        'Valladolid</div><h4>Crear donde no alcance ninguna raíz</h4>'
        '<div class="pm">Viernes 12 de diciembre, 19:30</div>'
        f'<div class="pl">{marca_c}</div></div>'
        '<p class="pie">Campo ámbar entero, tinta encima — '
        f'{_n(contraste(P["tinta"], P["ámbar"]))}:1.</p></div>'
        '<div><div class="cita">«Buscamos la extenuación: de la palabra, de los '
        'recursos, de la energía corporal.»'
        f'<div class="cf">{marca_a}</div></div>'
        '<p class="pie">Banda zafiro, cera encima, la marca en ámbar — '
        f'{_n(contraste(P["ámbar"], P["zafiro"]))}:1.</p></div></div>'
        # la marca
        '<div class="ap"><div class="marcas">'
        f'<div class="mq" style="background:{P["papel"]}">{marca_c}</div>'
        f'<div class="mq" style="background:{P["hueso"]}">{marca_z}</div>'
        f'<div class="mq" style="background:{P["ámbar"]}">{marca_c}</div>'
        f'<div class="mq" style="background:{P["rosa"]}">{marca_z}</div>'
        f'<div class="mq" style="background:{P["zafiro"]}">{marca_a}</div>'
        f'<div class="mq" style="background:{P["tinta"]}">{marca_a}</div>'
        '</div><p class="pie">La marca real, importada de '
        '<code>content/marca/lockup.py</code>, sobre los seis fondos que la '
        'paleta permite. No es una maqueta.</p></div></section>')


def s_ciclos():
    p = ['<section><h2>Por qué cinco colores y no tres</h2>'
         '<p class="ent">Hay <b>tres ciclos</b> —En voz alta, La Magistral, '
         'Noches íntimas— y las piezas generativas piden arrays de cuatro '
         'colores. Con tres cromáticos, uno de los ciclos tendría que quedarse '
         'el ámbar, y el ámbar es del colectivo. De ahí salen los dos que '
         'faltaban.</p>'
         '<p class="ent">Lo que <i>no</i> justifica añadirlos es repartir la '
         'rueda: quedan 221° vacíos entre el ámbar y el zafiro, pero un sistema '
         'de marca no es un gráfico. Y colores semánticos —error, aviso, '
         'éxito— no hacen ninguna falta: el sitio no tiene ni un '
         'formulario.</p><div class="cic">']
    for ciclo, tok, det in CICLOS:
        h = P[tok]
        claro = lch(h)[0] > 55
        fg = P["zafiro"] if claro else P["cera"]
        p.append(f'<div class="cb" style="background:{h};color:{fg}">'
                 f'<div class="ck">{ciclo}</div>'
                 f'<h4>Crear donde no alcance ninguna raíz</h4>'
                 f'<div class="cm">{tok} · {det}</div></div>')
    p.append(f'<div class="cb" style="background:{P["ámbar"]};color:{P["tinta"]}">'
             f'<div class="ck">el colectivo</div>'
             f'<h4>Ante la síntesis, la disgregación</h4>'
             f'<div class="cm">ámbar · el campo claro</div></div>'
             f'<div class="cb" style="background:{P["zafiro"]};color:{P["cera"]}">'
             f'<div class="ck">el colectivo</div><h4>Brújula sin imán</h4>'
             f'<div class="cm">zafiro · la banda oscura</div></div>')
    p.append('</div><p class="nota">El candidato matemáticamente correcto para '
             'el verde —L*80, croma 45— sale <code>#83d99b</code>: neón, alegre, '
             'tecnológico. Lo contrario de <i>moho, maleza, ruinas, '
             'extenuación</i>. A claridad alta un verde necesita croma bajo para '
             'seguir siendo serio; a L*30 aguanta croma 28 y lee como tinta de '
             'imprenta.</p>'
             '<p class="nota">Y <b>náufrago no está en h256</b>, que es donde '
             'vivía Medianoche, a 45° del zafiro — justo por lo que se retiró. '
             'Empujado a h231 quedan 71° al zafiro y 76° al moho: las tres '
             'oscuras repartidas, no dos azules peleándose.</p></section>')
    return "".join(p)


# ── 7 · la matriz ──────────────────────────────────────────────────────────
def s_matriz():
    ns = [n for n, _, _, _, _ in PALETA]
    p = ['<section><h2>Qué se puede poner sobre qué</h2><div class="tw">'
         '<table class="mt"><tr><th></th>']
    for n in ns:
        p.append(f'<th>{n}</th>')
    p.append('</tr>')
    for n in ns:
        p.append(f'<tr><th class="fi">{n}</th>')
        for m in ns:
            if n == m:
                p.append('<td class="mismo">·</td>')
                continue
            c = contraste(P[n], P[m])
            p.append(f'<td class="n-{nivel(c).replace(" ", "")}">{c:.1f}</td>')
        p.append('</tr>')
    t = len(PAREJAS) + len(PAREJAS_UI)
    p.append('</table></div><p class="ley">'
             '<i class="n-AAA"></i> AAA &nbsp; <i class="n-AA"></i> AA &nbsp; '
             '<i class="n-grande"></i> sólo titulares &nbsp; '
             '<i class="n-no"></i> no se juntan</p>'
             f'<p class="nota">Las <b>{t} parejas</b> que el sistema necesita de '
             'verdad pasan su umbral, todas — ' + str(len(PAREJAS)) + ' de texto '
             'a 4,5:1 y ' + str(len(PAREJAS_UI)) + ' de interfaz a 3:1. '
             '<code>paleta.py --verificar</code> lo comprueba y sale con error si '
             'alguna cae, para que la paleta no se degrade en silencio.</p>'
             '<p class="nota">El rojo de la tabla no es un fallo: la mayoría de '
             'los pares claros no deben tocarse, y para eso está. La trampa que '
             'conviene recordar es <b>rosa sobre ámbar</b>, '
             + _n(contraste(P["rosa"], P["ámbar"])) + ':1 — son casi la misma '
             'claridad y uno desaparece sobre el otro.</p></section>')
    return "".join(p)


# ── 8 · lo retirado ────────────────────────────────────────────────────────
def s_retirado():
    p = ['<section><h2>Lo que se retira</h2><table class="re">']
    for h, n, razon in RETIRADOS:
        p.append(f'<tr><td><i style="background:{h}"></i><code>{h}</code></td>'
                 f'<td class="rn">{n}</td><td class="det">{razon}</td></tr>')
    p.append('</table><p class="nota">Y una corrección que hay que hacer el día '
             'que esto se adopte: <code>skills/brand-content/references/'
             'colorplan.md</code> afirma que la paleta ámbar «no está en uso». '
             'Es falso —hay unas tres mil apariciones de <code>#ffb923</code> y '
             '<code>#171513</code> entre la marca, Instagram y las camisetas— y '
             'es la frase más peligrosa del repositorio para esta '
             'decisión.</p></section>')
    return "".join(p)


def pagina():
    cuerpo = "".join((s_paleta(), s_rampa(), s_roles(), s_porque(), s_suelo(),
                      s_prueba(), s_ciclos(), s_matriz(), s_retirado()))
    css = PLANTILLA_CSS.format(**{k.replace("á", "a").replace("í", "i"): v
                                  for k, v in P.items()})
    html = (PLANTILLA.replace("{estilo}", css)
                     .replace("{cuerpo}", cuerpo))
    with open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    mal = verificar(ruidoso=False)
    print(f"página → content/paleta/index.html   "
          f"({len(PALETA)} tonos · {len(PAREJAS)+len(PAREJAS_UI)-mal} de "
          f"{len(PAREJAS)+len(PAREJAS_UI)} parejas pasan)")
    return mal


# La hoja está pintada con la propia paleta: no hay un solo color fuera de
# ella. Si algún token estuviera mal elegido, esta página sería la primera en
# no sostenerse.
PLANTILLA_CSS = """
/* La marca que se importa de lockup.py trae su caja calculada con las
   métricas de FuturaStd. Sin declarar la fuente, el navegador cae en
   Helvetica —más ancha— y el punto final de «C.F.D.L.» queda fuera del
   viewBox y aparece cortado. Ya pasó una vez. */
@font-face{{font-family:'FuturaStd';
  src:url('../../docs/assets/fonts/FuturaStd-Book.otf') format('opentype');
  font-display:block}}
:root{{
  --papel:{papel}; --hueso:{hueso}; --filete:{filete}; --ceniza:{ceniza};
  --humo:{humo}; --tinta:{tinta};
  --ambar:{ambar}; --rosa:{rosa}; --zafiro:{zafiro};
  --cera:{cera}; --lavanda:{lavanda};
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--papel);color:var(--tinta);
  font:400 16px/1.62 ui-sans-serif,system-ui,sans-serif}}
.h{{max-width:1000px;margin:0 auto;padding:60px 32px 96px}}
header{{border-bottom:1px solid var(--filete);padding-bottom:34px}}
.et{{font-size:11px;letter-spacing:.22em;text-transform:uppercase;
  color:var(--ceniza)}}
h1{{font:400 34px/1.1 ui-sans-serif,system-ui;letter-spacing:.01em;margin:12px 0 0}}
.baj{{color:var(--humo);max-width:62ch;margin:14px 0 0}}
section{{border-bottom:1px solid var(--filete);padding:44px 0}}
section:last-of-type{{border-bottom:0}}
h2{{font:400 11px/1 ui-sans-serif,system-ui;letter-spacing:.22em;
  text-transform:uppercase;color:var(--ceniza);margin:0 0 22px}}
h3{{font:400 11px/1 ui-sans-serif;letter-spacing:.18em;text-transform:uppercase;
  color:var(--humo);margin:30px 0 10px;font-weight:500}}
h3:first-of-type{{margin-top:0}}
p.ent{{color:var(--humo);max-width:64ch;margin:0 0 20px;font-size:15px}}
p.ent b,p.nota b{{color:var(--tinta);font-weight:500}}
.nota{{font-size:13.5px;color:var(--humo);margin:22px 0 0;max-width:66ch}}
.pie{{font-size:13px;color:var(--humo);margin:10px 0 0;max-width:52ch}}
code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px;
  background:var(--hueso);padding:1px 5px;border-radius:2px;color:var(--tinta)}}
/* muestras */
.rej{{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:18px}}
.mu{{margin:0}}
.ch{{height:74px;border-radius:2px;border:1px solid var(--filete)}}
.mu b{{display:block;margin-top:9px;font-weight:500;font-size:14.5px}}
.mu .nv{{display:inline;margin:0 7px 0 7px;font-size:10px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ceniza);font-weight:400}}
.mu code{{display:inline-block;margin-top:2px;background:none;padding:0;
  color:var(--humo)}}
.mu .num{{display:block;font-size:11.5px;color:var(--ceniza);margin-top:2px}}
.mu .pa{{display:block;font-size:12.5px;color:var(--humo);margin-top:6px}}
.mu .or{{display:block;font-size:11.5px;color:var(--ceniza);margin-top:4px}}
/* rampa */
.ramp{{display:flex;border-radius:2px;overflow:hidden;border:1px solid var(--filete)}}
.ramp div{{flex:1;height:86px;padding:9px;display:flex;flex-direction:column;
  justify-content:flex-end;font-size:11.5px}}
.ramp .l{{font-family:ui-monospace,Menlo,monospace;font-size:10.5px;opacity:.75}}
.dos{{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start;
  margin-top:26px}}
.ficha{{background:var(--hueso);border:1px solid var(--filete);border-radius:2px;
  padding:20px}}
.ficha .k{{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--humo)}}
.ficha h4{{font:italic 400 21px/1.3 Georgia,'Times New Roman',serif;margin:8px 0 6px}}
.ficha .m{{font-size:13px;color:var(--humo)}}
.ficha hr{{border:0;border-top:1px solid var(--filete);margin:14px 0}}
.ficha .ina{{font-size:13px;color:var(--ceniza)}}
.ficha.mal{{background:var(--rosa);border-color:var(--rosa)}}
.ficha.mal .k,.ficha.mal .m{{color:var(--zafiro);opacity:.72}}
.ficha.mal h4{{color:var(--zafiro)}}
.ficha.mal hr{{border-color:var(--lavanda)}}
/* papeles */
table.ro,table.re{{border-collapse:collapse;font-size:14.5px;width:100%}}
table.ro td,table.ro th,table.re td{{padding:9px 14px 9px 0;
  border-bottom:1px solid var(--filete);vertical-align:baseline;text-align:left}}
table.ro th{{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--ceniza);font-weight:400}}
.rn{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--humo);white-space:nowrap}}
table.ro i,table.re i{{display:inline-block;width:12px;height:12px;border-radius:2px;
  border:1px solid var(--filete);margin-right:8px;vertical-align:-1px}}
.det{{color:var(--humo);font-size:13.5px}}
/* rueda y pares */
.rue{{grid-template-columns:240px 1fr;align-items:center}}
.pares{{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:6px}}
.pa2{{display:flex;gap:14px;align-items:flex-start;font-size:13.5px}}
.pab{{display:flex;flex-shrink:0}}
.pab span{{width:34px;height:52px;display:block;border:1px solid var(--filete)}}
.pa2 .num{{display:block;font-size:12px;color:var(--ceniza);margin-top:3px}}
.pa2 .ve{{display:block;color:var(--humo);margin-top:6px}}
/* suelo */
.pr{{padding:32px 30px;margin-bottom:2px}}
.pr p{{margin:0;font-size:19px;max-width:44ch}}
.pr span{{display:block;margin-top:12px;font-size:12px;color:var(--humo)}}
/* puesta a prueba */
.ap{{margin-top:26px}}
.web{{border:1px solid var(--filete);border-radius:2px;overflow:hidden}}
.wbar{{background:var(--zafiro);padding:14px 20px;display:flex;
  align-items:center;justify-content:space-between;gap:20px;line-height:0}}
.wbar nav{{color:var(--lavanda);font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;line-height:1}}
.wbody{{padding:26px 20px 24px;background:var(--papel)}}
.wbody h4{{font:italic 400 25px/1.25 Georgia,'Times New Roman',serif;margin:0 0 10px}}
.wbody p{{margin:0;max-width:52ch;font-size:15px}}
.wmeta{{margin-top:14px;font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--humo)}}
.wrule{{width:46px;height:3px;background:var(--ambar);margin-top:14px}}
.post{{background:var(--ambar);padding:26px 22px;border-radius:2px}}
.post .pk{{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--tinta);opacity:.66}}
.post h4{{font:italic 400 24px/1.24 Georgia,'Times New Roman',serif;margin:10px 0 8px;
  max-width:16ch}}
.post .pm{{font-size:13.5px;color:var(--tinta);opacity:.78}}
.post .pl{{margin-top:22px;line-height:0}}
.cita{{background:var(--zafiro);color:var(--cera);padding:26px 22px;
  border-radius:2px;font:italic 400 19px/1.45 Georgia,'Times New Roman',serif;
  min-height:100%}}
.cita .cf{{margin-top:22px;line-height:0}}
.marcas{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
  gap:2px;border:1px solid var(--filete);border-radius:2px;overflow:hidden}}
.mq{{padding:22px 16px;display:flex;align-items:center;justify-content:center;
  line-height:0}}
/* ciclos */
.cic{{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));
  gap:10px}}
.cb{{padding:18px 16px;border-radius:2px;min-height:148px;display:flex;
  flex-direction:column;justify-content:space-between}}
.cb .ck{{font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;
  opacity:.72}}
.cb h4{{font:italic 400 17px/1.24 Georgia,'Times New Roman',serif;margin:8px 0 0}}
.cb .cm{{font-size:11px;opacity:.72;margin-top:10px}}
/* matriz */
.tw{{overflow-x:auto}}
table.mt{{border-collapse:collapse;font-size:12.5px;width:100%;min-width:640px}}
table.mt th,table.mt td{{padding:6px 7px;text-align:center;
  border:1px solid var(--papel)}}
table.mt th{{font-weight:400;font-size:10.5px;color:var(--humo);
  text-align:left;background:var(--papel)}}
table.mt th.fi{{white-space:nowrap;padding-right:12px}}
.n-AAA{{background:#cfe0cd}} .n-AA{{background:#e5ead3}}
.n-grande{{background:#f4e3c6}} .n-no{{background:#efd8d8;color:var(--ceniza)}}
.mismo{{background:var(--hueso);color:var(--ceniza)}}
.ley{{font-size:12.5px;color:var(--humo);margin:14px 0 0}}
.ley i{{display:inline-block;width:13px;height:13px;border-radius:2px;
  vertical-align:-2px;margin-right:4px;border:1px solid var(--filete)}}
table.re td{{padding:10px 14px 10px 0}}
table.re code{{background:none;padding:0;color:var(--humo)}}
footer{{border-top:1px solid var(--filete);margin-top:56px;padding-top:22px;
  font-size:13px;color:var(--ceniza)}}
footer a{{color:var(--humo);text-decoration:none;
  border-bottom:1px solid var(--filete)}}
footer a:hover{{color:var(--tinta)}}
footer p{{margin:0 0 8px}}
:focus-visible{{outline:2px solid var(--zafiro);outline-offset:3px}}
@media (max-width:760px){{.dos,.pares{{grid-template-columns:1fr}}
  .rue{{grid-template-columns:1fr}}}}
"""

PLANTILLA = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>C.F.D.L. — la paleta</title>
<style>{estilo}</style></head><body><div class="h">

<header>
  <div class="et">Colectivo Fuera de Lugar · Col·lectiu Fora de Lloc</div>
  <h1>La paleta</h1>
  <p class="baj">Una sola, en lugar de dos. Seis grises que hacen el trabajo
  callado, tres colores que hablan, dos para poner encima de lo oscuro.
  Propuesta — el sitio, Instagram y las camisetas siguen con lo suyo.</p>
</header>

{cuerpo}

<footer>
  <p>Esta página está pintada con la propia paleta: no hay un solo color fuera
  de ella.</p>
  <p><code>python3 paleta.py</code> lista los tonos ·
     <code>python3 paleta.py --verificar</code> comprueba los contrastes ·
     <code>python3 hoja.py</code> rehace esta página ·
     <a href="../marca/index.html">la marca</a></p>
</footer>

</div></body></html>
"""

if __name__ == "__main__":
    sys.exit(1 if pagina() else 0)
