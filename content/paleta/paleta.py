#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — una sola paleta.

PROPUESTA. El sitio, Instagram y las camisetas siguen con lo suyo hasta que se
decida; aquí no se cablea nada.

EL PROBLEMA. El colectivo arrastraba dos paletas que no se hablaban: la rosa
—Candy Pink, Zafiro, Factory Yellow— publicada en cfdl.site, y la citrina
—Niebla, Cera, Citrina, Medianoche— documentada como «alternativa». Instagram
implementaba las dos, las camisetas una tercera variante del citrino, y la
marca nueva ámbar sobre zafiro. Cuatro superficies, tres respuestas.

LO QUE RESULTÓ AL MEDIRLO. Ámbar y zafiro no se pelean: están a 138° de matiz,
que es un complementario partido —el complementario exacto del ámbar sería
azul puro, h 260°; el zafiro está en 301°, violáceo—. Lo que faltaba es que
nunca habían compartido suelo. Y el escalón que los une ya estaba en casa: el
rosa cae a 76° del zafiro y a 63° del ámbar, casi en medio del salto.

Sobraban dos duplicados, no un color: dos amarillos a 17° que no se distinguen
en valor, y dos notas frías a 45°. Quitando uno de cada par, la paleta se
resuelve sola.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from color import (lch, contraste, nivel, distancia, salto_matiz,
                   desde_lch)

# ── LA PALETA ──────────────────────────────────────────────────────────────
# SEIS NEUTROS, CINCO COLORES, DOS PARA ENCIMA DE LO OSCURO.
#
# CINCO Y NO TRES, por un motivo concreto: hay tres ciclos —En voz alta, La
# Magistral, Noches íntimas— y con tres cromáticos uno de ellos tendría que
# quedarse el ámbar, que es del colectivo y no de un ciclo. Ámbar y zafiro
# fijos, más tres bandas de ciclo. No se añaden para repartir la rueda: un
# sistema de marca no es un gráfico, y el sitio no tiene ni un formulario, así
# que colores semánticos —error, aviso, éxito— no hacen ninguna falta.
#
# LOS DOS NUEVOS VAN OSCUROS Y APAGADOS. El candidato matemáticamente correcto
# —un verde a L*80 con croma 45— sale #83d99b: neón, alegre, tecnológico, lo
# contrario de moho, maleza, ruinas y extenuación. A claridad alta un verde
# necesita croma bajo para seguir siendo serio; a L*30 aguanta croma 28 y lee
# como tinta de imprenta.
#
# Y NÁUFRAGO NO ESTÁ EN h256. Ahí es donde vivía Medianoche, a 45° del zafiro,
# que es justo por lo que se retiró. Empujado a h231 quedan 71° al zafiro y
# 76° al moho: las tres oscuras repartidas.
#
# El primer reparto tenía siete cromáticos y tres neutros, que es al revés de
# como se construye un sistema: los grises hacen el trabajo callado —bordes,
# separadores, estados inactivos, rejillas— y sin ellos hay que tirar de color
# para todo, así que la superficie acaba rosa y el borde lavanda, y una ficha
# de evento grita cuando debería susurrar.
#
# Entre L*97 y L*42 había 55 puntos sin un solo tono. La rampa los tapa.
#
# LOS GRISES VAN EN EL MATIZ DEL ÁMBAR, a croma 6–7. A ese croma no se leen
# como otro color cálido: se leen como grises. Pero grises del mismo papel, no
# el gris frío de fábrica, que sobre un fondo cálido se ve azulado y sucio.
PALETA = [
    # — la rampa neutra —
    ("papel",   "#fdf5eb", "fondo de página", "neutro",
     "nuevo — el propio ámbar llevado a L*97 con casi nada de croma"),
    ("hueso",   "#f1e7db", "superficie levantada sobre el papel", "neutro",
     "nuevo — 1,13:1 contra el papel: se ve sin separarse"),
    ("filete",  "#e0d6ca", "borde, separador, filete", "neutro",
     "nuevo — tapa el hueco que dejaba sin token los 56 bordes del sitio"),
    ("ceniza",  "#a89f96", "inactivo, rejilla, filete fuerte", "neutro",
     "nuevo — 2,42:1: se ve de sobra sin llegar a leerse como texto"),
    ("humo",    "#6a625a", "texto secundario sobre claro", "neutro",
     "revisado de #857c75, que daba 3,78:1 y lleva tiempo publicado así"),
    ("tinta",   "#171513", "texto principal", "neutro",
     "ya existía: el negro cálido de la impresión"),
    # — los colores —
    ("ámbar",   "#ffb923", "ancla: campo, marca, acento", "color",
     "ya existía: el ámbar del logotipo y del manifiesto impreso"),
    ("rosa",    "#f8ccce", "el puente: bandas y tintes", "color",
     "ya existía: Candy Pink, el fondo publicado del sitio"),
    ("zafiro",  "#332f8a", "la nota ajena: texto y bandas oscuras", "color",
     "ya existía: Sapphire, la tinta de la web"),
    ("moho",    "#1b5033", "banda de ciclo", "color",
     "nuevo — «La llegada del moho» es una pieza del sitio, y moho y maleza "
     "están en el vocabulario del manifiesto"),
    ("náufrago","#004d5f", "banda de ciclo", "color",
     "nuevo — petróleo profundo; náufrago y garganta sin fondo vienen del "
     "mismo vocabulario"),
    # — para poner encima de lo oscuro —
    ("cera",    "#fff4d6", "tinta clara sobre fondo oscuro", "sobre oscuro",
     "ya existía: la «Cera» de brand-content, el crema de la marca"),
    ("lavanda", "#bbabd5", "secundario sobre zafiro", "sobre oscuro",
     "ya existía: Lavender, las superficies del sitio"),
]
HEX = {n: h for n, h, _, _, _ in PALETA}
GRUPOS = ("neutro", "color", "sobre oscuro")

# ── LOS PAPELES ────────────────────────────────────────────────────────────
# Qué token va en qué sitio. Tenerlo escrito es lo que separa una paleta de
# una lista de colores bonitos.
ROLES = [
    ("fondo",        "papel",  "tinta",   "la página"),
    ("superficie",   "hueso",  "zafiro",  "lo que se levanta del papel"),
    ("borde",        "filete", "lavanda", "fichas, tablas, separadores"),
    ("texto",        "tinta",  "papel",   "el cuerpo"),
    ("secundario",   "humo",   "lavanda", "pies, metadatos, fechas"),
    ("inactivo",     "ceniza", "ceniza",  "lo que está ahí pero no se puede usar"),
    ("banda",        "zafiro", "ámbar",   "cabecera, pie, cita destacada"),
    ("campo",        "ámbar",  "ámbar",   "post entero, camiseta, logotipo"),
    ("acento",       "ámbar",  "ámbar",   "regla, punto, marca"),
    ("foco",         "zafiro", "ámbar",   "el anillo del teclado — NO ámbar sobre claro"),
    ("tinte",        "rosa",   "rosa",    "franja suave, sombreado"),
]

# Qué ciclo lleva qué banda. Provisional — es una decisión editorial, no de
# color, y se cambia cambiando esta tabla. Lo que sí es de color: las tres se
# distinguen entre sí (71–147° de matiz) y ninguna es el ámbar ni el zafiro,
# que son del colectivo y no de un ciclo.
CICLOS = [
    ("En voz alta",    "rosa",     "clara — zafiro encima, 7,58:1"),
    ("La Magistral",   "náufrago", "oscura — cera encima, 8,61:1"),
    ("Noches íntimas", "moho",     "oscura — cera encima, 8,55:1"),
]

# ── LAS PAREJAS OBLIGATORIAS ───────────────────────────────────────────────
# Si una de éstas baja de 4,5:1 la paleta está rota, y --verificar lo dice con
# código de salida. Es la misma disciplina de content/instagram/render.sh: que
# el fallo se note, en vez de degradarse en silencio.
PAREJAS = [
    ("tinta", "papel"), ("humo", "papel"), ("zafiro", "papel"),
    ("tinta", "hueso"), ("humo", "hueso"), ("zafiro", "hueso"),
    ("tinta", "rosa"), ("zafiro", "rosa"),
    ("tinta", "ámbar"), ("zafiro", "ámbar"),
    ("papel", "zafiro"), ("cera", "zafiro"), ("lavanda", "zafiro"),
    ("ámbar", "zafiro"), ("rosa", "zafiro"),
    ("papel", "tinta"), ("ámbar", "tinta"), ("cera", "tinta"),
    ("rosa", "tinta"),
    ("papel", "moho"), ("cera", "moho"), ("ámbar", "moho"), ("rosa", "moho"),
    ("papel", "náufrago"), ("cera", "náufrago"), ("ámbar", "náufrago"),
    ("rosa", "náufrago"),
]

# Lo que no es texto pero sí tiene que verse: un borde de campo, un anillo de
# foco, una casilla. La WCAG pide 3:1 para eso, y es donde salta el aviso más
# útil de toda la paleta — el ÁMBAR NO PUEDE SER EL ANILLO DE FOCO sobre claro:
# da 1,59:1 sobre papel y desaparece. El foco va en zafiro. El ámbar es el
# color de la marca, no el de la interfaz.
PAREJAS_UI = [
    ("humo", "papel"), ("humo", "hueso"),
    ("zafiro", "papel"), ("zafiro", "hueso"),
]
# CENIZA NO ESTÁ AQUÍ, y no es un descuido. Da 2,41:1 sobre papel, por debajo
# del 3:1 — pero su trabajo son estados inactivos, rejillas y filetes fuertes,
# y la WCAG exime expresamente los componentes inactivos y lo decorativo. Se
# probó bajarla a L*54 para que cumpliera: entonces queda a 1,54:1 de humo y
# las dos se confunden. Un borde que SÍ tiene que verse —el contorno de un
# campo, una casilla, el anillo de foco— usa humo o zafiro, no ceniza.

# ── LO QUE SE RETIRA ───────────────────────────────────────────────────────
RETIRADOS = [
    ("#fde700", "Factory Yellow",
     "1,36:1 contra el ámbar y a 17° de matiz: dos amarillos que no se "
     "distinguen en valor. Cabe uno."),
    ("#1a2e3d", "Medianoche", "rama fría azul (h 256°) que compite con el "
     "zafiro (h 301°). Dos notas frías a 45° no pueden mandar a la vez."),
    ("#4a6880", "Pizarra", "misma rama, mismo motivo"),
    ("#e8edf0", "Niebla", "el fondo frío de la paleta citrina; el suelo ahora "
     "es cálido"),
    ("#ffd25a", "Sol", "escalón de la rama citrina que se queda sin trabajo"),
    ("#6b4200", "Resina", "íd. — el cálido profundo lo hace azafrán"),
    ("#7d9e92", "Salvia", "íd. — verde suelto sin ningún papel"),
    ("#c07d00", "Azafrán",
     "con la rampa puesta se queda casi sin trabajo: era un cuarto cálido "
     "cromático en una paleta que ya es 70 % un solo matiz. Los filetes los "
     "hacen ahora filete y ceniza, que es lo que debe hacer un filete."),
    ("#857c75", "Smoke",
     "3,78:1 sobre fondo claro — por debajo del mínimo legible, y lleva tiempo "
     "publicado como texto secundario. Lo sustituye humo."),
    ("#c8b8d8", "lavender-pink",
     "el borde del sitio era un color; ahora es un gris, que es lo que pide un "
     "borde. Lo sustituye filete."),
    ("#e9ad51", "citrino de camisetas",
     "un tercer valor para el mismo concepto, aproximación al papel Colorplan. "
     "Se unifica en ámbar."),
]

# Lo que hay que corregir en la documentación el día que esto se adopte.
# colorplan.md afirma que la paleta ámbar «no está en uso», y hay unas 3000
# apariciones de #ffb923 y #171513 entre marca, Instagram y camisetas.
CONTRADICCION = ("skills/brand-content/references/colorplan.md", 83)


# ── LOS TONOS ──────────────────────────────────────────────────────────────
# Un tono es un color de la paleta puesto a trabajar: la banda oscura de una
# pieza, con su tinta encima, su secundario y su filete. Los cinco cromáticos
# dan cinco tonos, y ésa es toda la variación que necesita una pieza — antes
# eran dos temas enteros, «pink» y «citrine», cada uno con su propio suelo.
#
# NO SE ELIGEN A OJO. El secundario y el filete se derivan del propio tono
# aclarándolo u oscureciéndolo, con el croma bajado a 0,72 para que no
# compitan, y el desplazamiento se BUSCA: el más pequeño que alcanza 4,5:1.
# Así el secundario sigue perteneciendo a su banda en vez de ser otro color.
_K = 0.72                    # cuánto croma conserva un derivado


def _deriva(h, dL):
    L, C, H = lch(h)
    return desde_lch(max(2, min(98, L + dL)), C * _K, H)


def _busca(h, objetivo, arriba):
    """El desplazamiento de claridad más pequeño que alcanza el contraste."""
    paso = 1 if arriba else -1
    for i in range(1, 96):
        c = _deriva(h, paso * i)
        if contraste(c, h) >= objetivo:
            return c
    raise SystemExit(f"no hay derivado de {h} que llegue a {objetivo}:1")


def _tono(nombre):
    h = HEX[nombre]
    claro = lch(h)[0] > 55
    sobre = HEX["tinta"] if claro else HEX["cera"]
    # El acento se usa sobre PAPEL, no sobre la banda. El ámbar sobre papel da
    # 1,59:1 y el rosa 1,34: sirven para un punto grande, no para un filete.
    # Por eso un tono claro presta su versión oscurecida como acento.
    acento = h if not claro else _busca(h, 4.5, False)
    return {
        "color":  h,
        "sobre":  sobre,
        "segundo": _busca(h, 4.5, not claro),
        "filete": _deriva(h, -16 if claro else 18),
        "acento": acento,
    }


TONOS = {n: _tono(n) for n in ("ámbar", "rosa", "zafiro", "moho", "náufrago")}

# El nombre del tono llega desde un JSON y acaba en una clase CSS, así que no
# puede llevar tilde.
SIN_TILDE = str.maketrans("áéíóúñ", "aeioun")


def clave(nombre):
    return nombre.translate(SIN_TILDE)


def css():
    """El bloque de tokens, para que lo escriba quien lo necesite en vez de
    mantenerlo a mano en dos sitios. Instagram tenía los suyos repetidos en el
    CSS y en Python, y era cuestión de tiempo que divergieran."""
    L = ["/* GENERADO por content/paleta/paleta.py — no editar a mano.",
         "   Se rehace con: python3 paleta.py --css */",
         ":root {"]
    for n, h, _, _, _ in PALETA:
        L.append(f"  --{clave(n)}: {h};")
    L.append("}")
    L.append("")
    L.append("/* Un tono por pieza. El suelo es SIEMPRE el papel; lo que cambia")
    L.append("   es de quién es la banda. */")
    for n, t in TONOS.items():
        k = clave(n)
        L.append(f".tono-{k} {{")
        L.append(f"  --bg:var(--papel); --surface:var(--hueso); "
                 f"--text:var(--tinta);")
        L.append(f"  --muted:var(--humo); --border:var(--filete);")
        L.append(f"  --accent:{t['acento']};")
        L.append(f"  --band-bg:{t['color']}; --band-fg:{t['sobre']};")
        L.append(f"  --band-muted:{t['segundo']}; --band-rule:{t['filete']};")
        L.append(f"  --duo-dark:{t['color']}; --duo-light:var(--papel);")
        L.append("}")
    return "\n".join(L) + "\n"


def verificar(ruidoso=True):
    """Devuelve el número de parejas que fallan. Dos listas y dos umbrales:
    texto pide 4,5:1; lo que no es texto pero tiene que verse, 3:1."""
    mal = 0
    for lista, umbral, et in ((PAREJAS, 4.5, "texto"),
                              (PAREJAS_UI, 3.0, "no texto")):
        if ruidoso:
            print(f"\n  — {et}, mínimo {umbral}:1 —")
        for a, b in lista:
            c = contraste(HEX[a], HEX[b])
            if c < umbral:
                mal += 1
                if ruidoso:
                    print(f"  FALLA  {a} sobre {b}: {c:.2f}:1", file=sys.stderr)
            elif ruidoso:
                print(f"  ok     {a:8s} sobre {b:8s} {c:6.2f}:1  {nivel(c)}")
    # y cada tono contra su propia banda
    if ruidoso:
        print("\n  — tonos, cada uno sobre su banda —")
    n_t = 0
    for n, t in TONOS.items():
        for campo, umbral in (("sobre", 4.5), ("segundo", 4.5), ("acento", 0)):
            if umbral == 0:
                continue
            n_t += 1
            c = contraste(t[campo], t["color"])
            if c < umbral:
                mal += 1
                if ruidoso:
                    print(f"  FALLA  {n}/{campo}: {c:.2f}:1", file=sys.stderr)
            elif ruidoso:
                print(f"  ok     {n:9s} {campo:8s} {c:6.2f}:1  {nivel(c)}")
        # el acento se usa sobre PAPEL, no sobre la banda
        n_t += 1
        c = contraste(t["acento"], HEX["papel"])
        if c < 3.0:
            mal += 1
            if ruidoso:
                print(f"  FALLA  {n}/acento sobre papel: {c:.2f}:1", file=sys.stderr)
        elif ruidoso:
            print(f"  ok     {n:9s} acento   {c:6.2f}:1 sobre papel")
    if ruidoso:
        t = len(PAREJAS) + len(PAREJAS_UI) + n_t
        print(f"\n{t - mal} de {t} parejas pasan su umbral.")
    return mal


if __name__ == "__main__":
    if "--css" in sys.argv:
        print(css(), end="")
        sys.exit(0)
    if "--verificar" in sys.argv:
        sys.exit(1 if verificar() else 0)
    for g in GRUPOS:
        print(f"\n  — {g} —")
        for n, h, papel, gr, _ in PALETA:
            if gr != g:
                continue
            L, C, H = lch(h)
            print(f"  {n:8s} {h}  L*{L:5.1f} C*{C:5.1f} h{H:4.0f}°   {papel}")
