#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — generador de imágenes para Instagram.

Lee los briefs de posts/*.json y emite src/<id>-NN.html (1080×1350), más el pie
de foto y el texto alternativo en out/. El render a PNG lo hace render.sh con
Chrome sin cabeza.

Sólo biblioteca estándar: en esta máquina no hay Pillow, ImageMagick ni PyYAML,
así que los datos son JSON y todo el tratamiento fotográfico ocurre en CSS/SVG
en el momento del render.

El CSS de maquetación vive en src/_shared.css y se escribe a mano. Este archivo
emite estructura y propiedades personalizadas, nunca reglas de diseño: así
afinar un cartel contra una captura de referencia es editar una hoja de estilos
en DevTools, no regenerar y volver a renderizar.

    python3 build_posts.py                  genera todo
    python3 build_posts.py --citrine        fuerza el tema en toda la tirada
    python3 build_posts.py --solo angela    sólo los briefs que casen
    python3 build_posts.py --lint           revisa voz, topes de bloques, ficheros
    python3 build_posts.py --verificar      contrasta con el calendario canónico
    python3 build_posts.py --indice         hoja de contactos en out/index.html
    python3 build_posts.py --debug          superpone rejilla y recorte 3:4
"""
import os, sys, json, glob, re, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "src")
OUT  = os.path.join(HERE, "out")
POSTS= os.path.join(HERE, "posts")
CAL  = os.path.normpath(os.path.join(HERE, "..", "events", "calendario-eventos.md"))

# ── temas ──────────────────────────────────────────────────────────────────
# El CSS lleva la paleta completa (.tema-pink / .tema-citrine). Aquí sólo hacen
# falta los dos extremos del duotono, porque el mapa de gradiente SVG se calcula
# en Python y se inyecta por página.
THEMES = {
    "pink":    {"duo_dark": "#332f8a", "duo_light": "#f8ccce"},
    "citrine": {"duo_dark": "#1a2e3d", "duo_light": "#fff4d6"},
}
ALIAS = {"rosa": "pink", "citrina": "citrine"}

MESES = ["enero","febrero","marzo","abril","mayo","junio",
         "julio","agosto","septiembre","octubre","noviembre","diciembre"]
MES_ABBR = {"ene":1,"feb":2,"mar":3,"abr":4,"may":5,"jun":6,
            "jul":7,"ago":8,"sep":9,"oct":10,"nov":11,"dic":12}
DIAS = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]

PLANTILLAS = {"evento", "ciclo", "recordatorio", "cita"}
# Tope de bloques por plantilla. No es un consejo: un cartel de 13 bloques a
# 1080×1350 se ve en el feed a ~430pt, o sea el cuerpo de texto a ~8px reales.
# El carrusel es la válvula de escape; esto la obliga.
TOPES = {"evento": 6, "recordatorio": 4, "cita": 3, "ciclo": 99}

CTA = re.compile(r"\b(únete|unete|descubre|no te lo pierdas|reserva ya|apúntate|"
                 r"apuntate|corre|date prisa|últimas plazas|ultimas plazas)\b", re.I)
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️←-⇿]")
# Palabra funcional capitalizada que no abre la cadena → Title Case.
FUNCIONALES = re.compile(
    r"(?<!^)\b(De|Del|La|El|Los|Las|Un|Una|Y|O|En|A|Al|Ante|Con|Sin|Por|Para|"
    r"Que|Su|Sus|Lo|Se|Como|Desde|Hasta|Entre|Sobre|Tras)\b")


def esc(s):
    return html.escape(str(s), quote=True)


def hex_rgb01(h):
    h = h.lstrip("#")
    return tuple(round(int(h[i:i+2], 16) / 255, 3) for i in (0, 2, 4))


def fecha_larga(iso):
    """2025-12-12 → ('viernes', '12 de diciembre', '2025')."""
    d = datetime.date.fromisoformat(iso)
    return DIAS[d.weekday()], f"{d.day} de {MESES[d.month - 1]}", str(d.year)


# ── carga y mezcla ─────────────────────────────────────────────────────────
def load_defaults():
    with open(os.path.join(HERE, "defaults.json"), encoding="utf-8") as f:
        return json.load(f)


def resolver(valor, tabla):
    """Una clave ('perecquiana') se busca en defaults; un objeto literal gana."""
    if isinstance(valor, str):
        return tabla.get(valor, {"nombre": valor, "ciudad": "", "marca": valor})
    return valor or {}


# ── primitivas de bloque ───────────────────────────────────────────────────
# Cada una devuelve "" si su dato no está. Ése es el mecanismo de «todo bloque
# es opcional»: la plantilla lista bloques, los datos deciden cuáles existen.
def b_marca_lugar(s):
    v = s.get("marca_lugar")
    return f'<div class="marca-lugar">{esc(v)}</div>' if v else ""


def sigla_txt(s):
    """La sigla vive en el pie, junto a la marca de contacto. Arriba competía
    con la cresta del ciclo siendo del mismo tamaño y tratamiento."""
    v = s.get("marca_cfdl")
    if not v:
        return ""
    return "C · F · D · L" if v == "sigla" else "Colectivo Fuera de Lugar"


def b_strapline(s, ciclos):
    c = s.get("ciclo")
    if not c:
        return ""
    c = resolver(c, ciclos)
    t = c.get("nombre", "")
    if c.get("lema"):
        t += f" — {c['lema']}"
    return f'<div class="strapline mt2">{esc(t)}</div>'


def b_antetitulo(s):
    v = s.get("antetitulo")
    return f'<div class="kicker">{esc(v)}</div>' if v else ""


def b_titular(s, cls="hero"):
    v = s.get("titular")
    if not v:
        return ""
    lineas = v if isinstance(v, list) else [v]
    return f'<div class="{cls} mt4">' + "<br>".join(esc(l) for l in lineas) + "</div>"


def b_subtitular(s):
    v = s.get("subtitular")
    return f'<div class="sub mt2">{esc(v)}</div>' if v else ""


def b_fecha(s):
    f = s.get("fecha")
    if not f:
        return ""
    txt = esc(" ".join(x for x in [f.get("dia_semana"), f.get("texto")] if x))
    if f.get("anio"):
        txt += f' <span class="anio">{esc(f["anio"])}</span>'
    return f'<div class="fecha mt8">{txt}</div>'


def b_hora(s):
    h = s.get("hora")
    if not h:
        return ""
    txt = " ".join(x for x in [h.get("prefijo"), h.get("texto")] if x)
    if h.get("sufijo"):
        txt += h["sufijo"]
    return f'<div class="hora mt2">{esc(txt)}</div>'


def b_meta(s, lugares):
    """Línea de referencia de la casa: Tipo — Lugar, Ciudad."""
    lug = resolver(s.get("lugar"), lugares) if s.get("lugar") else {}
    partes = []
    if lug.get("nombre"):
        partes.append(lug["nombre"] + (f", {lug['ciudad']}" if lug.get("ciudad") else ""))
    if not partes:
        return ""
    txt = f"{s['tipo']} — {partes[0]}" if s.get("tipo") else partes[0]
    return f'<div class="meta">{esc(txt)}</div>'


def b_presentacion(s):
    v = s.get("presentacion")
    return f'<div class="meta mt4">{esc(v)}</div>' if v else ""


def b_bio(s):
    v = s.get("bio")
    return f'<div class="bio mt6 fitcheck">{esc(v)}</div>' if v else ""


def b_aforo(s):
    v = s.get("aforo")
    return f'<div class="aforo mt2">{esc(v)}</div>' if v else ""


def b_foto(s):
    f = s.get("foto")
    if not f:
        return ""
    forma = f.get("forma", "banda")
    trat  = f.get("tratamiento", "bn")
    st = []
    if f.get("encuadre"):
        st.append(f'--encuadre:{f["encuadre"]}')
    if f.get("contraste"):
        st.append(f'--foto-contraste:{f["contraste"]}')
    if f.get("brillo"):
        st.append(f'--foto-brillo:{f["brillo"]}')
    grano = " grano" if f.get("grano") else ""
    sangre = " sangre" if forma in ("banda", "sangre") else ""
    return (f'<div class="foto f-{forma} t-{trat}{grano}{sangre}" '
            f'style="{";".join(st)}"><img src="{esc(f["src"])}" alt=""></div>')


def b_portadas(s):
    ps = s.get("portadas") or []
    if not ps:
        return ""
    imgs = "".join(f'<img src="{esc(p["src"])}" alt="">' for p in ps)
    return f'<div class="portadas mt6">{imgs}</div>'


def b_agenda(s):
    filas = s.get("agenda") or []
    if not filas:
        return ""
    out = []
    for r in filas:
        f = " ".join(x for x in [r.get("dia"), r.get("fecha")] if x)
        out.append(f'<div class="fila"><div class="f">{esc(f)}</div>'
                   f'<div class="n">{esc(r.get("nombre",""))}</div></div>')
    return f'<div class="agenda mt8 fitcheck">{"".join(out)}</div>'


def b_cita(s):
    c = s.get("cita")
    if not c:
        return ""
    out = f'<div class="cita-txt fitcheck">«{esc(c["texto"])}»</div>'
    if c.get("fuente"):
        out += f'<div class="cita-src mt8">{esc(c["fuente"])}</div>'
    return out


def b_pie(s, tag, n, total):
    sig = sigla_txt(s)
    izq = f'<div class="sigla">{esc(sig)}</div>' if sig else ""
    pag = ""
    if s.get("paginacion", total > 1) and total > 1:
        puntos = " · ".join(
            (f'<span class="hoy">{i}</span>' if i == n else str(i))
            for i in range(1, total + 1))
        pag = f'<div class="pag">{puntos}</div>'
    return (f'<div class="pie mt8"><div class="izq">{izq}<div class="tag">'
            f'{tag.replace("·", "<span class=sep>·</span>")}</div></div>{pag}</div>')


# ── recetas ────────────────────────────────────────────────────────────────
def receta(s, d, n, total):
    lugares, ciclos, tag = d["lugares"], d["ciclos"], d["tag"]
    p = s["plantilla"]

    if p == "evento":
        sup = b_marca_lugar(s) + b_strapline(s, ciclos)
        med = (b_antetitulo(s) + b_titular(s) + b_subtitular(s)
               + b_fecha(s) + b_hora(s) + b_presentacion(s) + b_bio(s))
        foto = b_foto(s)
        inf = b_meta(s, lugares) + b_aforo(s) + b_pie(s, tag, n, total)

    elif p == "ciclo":
        sup = b_marca_lugar(s) + b_strapline(s, ciclos)
        c = resolver(s.get("ciclo"), ciclos) if s.get("ciclo") else {}
        hero = b_titular(s) or (
            f'<div class="hero mt4">{esc(c.get("nombre",""))}</div>' if c else "")
        lema = (f'<div class="sub mt2">{esc(c["lema"])}</div>'
                if c.get("lema") and not s.get("subtitular") else b_subtitular(s))
        med = b_antetitulo(s) + hero + lema + b_agenda(s) + b_hora(s)
        foto = b_foto(s)
        inf = b_meta(s, lugares) + b_aforo(s) + b_pie(s, tag, n, total)

    elif p == "recordatorio":
        sup = ""
        med = b_titular(s, "display") + b_subtitular(s) + b_hora(s)
        foto = b_foto(s)
        inf = b_meta(s, lugares) + b_aforo(s) + b_pie(s, tag, n, total)

    elif p == "cita":
        sup = ""
        med = b_cita(s)
        foto = ""
        inf = b_pie(s, tag, n, total)

    else:
        raise SystemExit(f"plantilla desconocida: {p}")

    return sup, med, foto, inf


# ── página ─────────────────────────────────────────────────────────────────
# El canario mide cajas contra el lienzo y contra las demás zonas. La versión
# anterior dependía de overflow:hidden y scrollHeight, lo que (a) obligaba a
# recortar la zona media —y se comía el desplazamiento de la fecha— y (b) no
# veía el fallo real que apareció en el primer render: la banda de foto pisando
# la línea meta. Medir rectángulos no impone nada a la maquetación.
CANARIO = (
 "addEventListener('load',function(){"
 "var st=document.querySelector('.stage');if(!st)return;"
 "var R=st.getBoundingClientRect(),mal=[];"
 "function marca(e){e.style.outline='3px solid #ff00a0';}"
 # 1 · nada puede salirse del lienzo
 "st.querySelectorAll('*').forEach(function(el){"
 "if(el.classList.contains('canary'))return;"
 "var b=el.getBoundingClientRect();if(!b.width&&!b.height)return;"
 "if(b.top<R.top-1||b.bottom>R.bottom+1||b.left<R.left-1||b.right>R.right+1){"
 "marca(el);mal.push('fuera del lienzo');}});"
 # 2 · las zonas no pueden pisarse (la banda de foto sobre la línea meta)
 "var z=['.zona-sup','.zona-med','.zona-foto','.zona-inf']"
 ".map(function(q){var e=st.querySelector(q);"
 "return e&&e.getBoundingClientRect().height?e:null;}).filter(Boolean);"
 "for(var i=0;i<z.length-1;i++){"
 "var a=z[i].getBoundingClientRect(),c=z[i+1].getBoundingClientRect();"
 "if(a.bottom>c.top+1){marca(z[i]);marca(z[i+1]);mal.push('zonas solapadas');}}"
 # 3 · ni dos textos entre sí. Es el fallo que se coló en la plantilla de
 #     ciclo: la columna de fechas creció y se montó sobre los nombres, sin
 #     salirse de ninguna zona ni del lienzo.
 "var t=[].slice.call(st.querySelectorAll('*')).filter(function(e){"
 "return e.children.length===0&&e.textContent.trim()"
 "&&e.getBoundingClientRect().width;});"
 "for(var i=0;i<t.length;i++)for(var j=i+1;j<t.length;j++){"
 "var a=t[i].getBoundingClientRect(),b=t[j].getBoundingClientRect();"
 "if(a.left<b.right-2&&b.left<a.right-2&&a.top<b.bottom-2&&b.top<a.bottom-2){"
 "marca(t[i]);marca(t[j]);mal.push('textos superpuestos');}}"
 "if(mal.length)st.insertAdjacentHTML('beforeend',"
 "'<div class=\"canary\">'+mal[0]+'</div>');});"
)

PAGE = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>C.F.D.L. — {id} · {n}</title>
<link rel="stylesheet" href="_shared.css">
</head><body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="duo" color-interpolation-filters="sRGB">
<feColorMatrix type="matrix" values="0.2126 0.7152 0.0722 0 0
 0.2126 0.7152 0.0722 0 0  0.2126 0.7152 0.0722 0 0  0 0 0 1 0"/>
<feComponentTransfer>
<feFuncR type="table" tableValues="{dr} {lr}"/>
<feFuncG type="table" tableValues="{dg} {lg}"/>
<feFuncB type="table" tableValues="{db} {lb}"/>
</feComponentTransfer></filter></defs></svg>
<div class="stage tema-{theme} sup-{sup}{dbg} fitcheck">
<div class="zona-sup">{z1}</div>
<div class="zona-med">{z2}</div>
<div class="zona-foto">{zf}</div>
<div class="zona-inf">{z3}</div>
</div>
<script>{canario}</script>
</body></html>
"""


def emit(brief, d, forzar_tema=None, debug=False):
    pid = brief["id"]
    theme = forzar_tema or brief.get("theme") or d.get("theme", "pink")
    slides = brief["slides"]
    total = len(slides)
    paths = []
    for i, raw in enumerate(slides, 1):
        s = dict(raw)
        s.setdefault("aforo", None)   # el aforo se declara, no se hereda a ciegas
        th = forzar_tema or s.get("theme") or theme
        th = ALIAS.get(th, th)
        if th not in THEMES:
            raise SystemExit(f"{pid}: tema desconocido «{th}»")
        if s.get("plantilla") not in PLANTILLAS:
            raise SystemExit(f"{pid}: plantilla desconocida «{s.get('plantilla')}»")
        # heredar del post lo que la lámina no diga
        for k in ("marca_lugar", "ciclo"):
            if i == 1 and k not in s and k in brief:
                s[k] = brief[k]
        z1, z2, zf, z3 = receta(s, d, i, total)
        dk = hex_rgb01(THEMES[th]["duo_dark"])
        lt = hex_rgb01(THEMES[th]["duo_light"])
        page = PAGE.format(
            id=esc(pid), n=i, theme=th, sup=s.get("superficie", "claro"),
            dbg=" debug" if debug else "",
            dr=dk[0], dg=dk[1], db=dk[2], lr=lt[0], lg=lt[1], lb=lt[2],
            z1=z1, z2=z2, zf=zf, z3=z3, canario=CANARIO)
        p = os.path.join(SRC, f"{pid}-{i:02d}.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(page)
        paths.append(p)
    return paths


# ── pie de foto y texto alternativo ────────────────────────────────────────
def sidecars(brief, d):
    pid = brief["id"]
    cap = (brief.get("caption") or {})
    texto = cap.get("texto")
    if not texto:
        # Andamio a partir de los datos. No intenta la voz del colectivo: eso es
        # escritura, no formato. La skill es lo que convierte esto en copia real.
        s0 = brief["slides"][0]
        lug = resolver(s0.get("lugar"), d["lugares"]) if s0.get("lugar") else {}
        linea = []
        if s0.get("tipo") and lug.get("nombre"):
            linea.append(f"{s0['tipo']} — {lug['nombre']}"
                         + (f", {lug['ciudad']}" if lug.get("ciudad") else ""))
        f, h = s0.get("fecha") or {}, s0.get("hora") or {}
        if f:
            linea.append(" ".join(x for x in [f.get("dia_semana"), f.get("texto")] if x)
                         + (f", {h['texto']}" if h.get("texto") else ""))
        if s0.get("aforo") or d.get("aforo"):
            linea.append(s0.get("aforo") or d["aforo"])
        texto = "[PENDIENTE — escribir en voz C.F.D.L.]\n\n" + "\n".join(linea) \
                + f"\n\n{d['sitio']}"
    etiquetas = cap.get("etiquetas", d.get("etiquetas_por_defecto", []))
    if etiquetas:
        texto += "\n\n" + " ".join("#" + e.lower().lstrip("#") for e in etiquetas)
    with open(os.path.join(OUT, f"{pid}.caption.txt"), "w", encoding="utf-8") as fh:
        fh.write(texto.rstrip() + "\n")
    alts = [f"{i:02d}: {s.get('alt','[FALTA texto alternativo]')}"
            for i, s in enumerate(brief["slides"], 1)]
    with open(os.path.join(OUT, f"{pid}.alt.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(alts) + "\n")
    return texto


# ── linter: mecaniza las reglas de voz de CLAUDE.md ────────────────────────
def cadenas(s):
    for k in ("titular", "subtitular", "antetitulo", "bio", "aforo",
              "presentacion", "marca_lugar", "alt"):
        v = s.get(k)
        if isinstance(v, list):
            yield from ((k, x) for x in v)
        elif isinstance(v, str):
            yield (k, v)
    if isinstance(s.get("cita"), dict):
        yield ("cita", s["cita"].get("texto", ""))


def lint(brief, d, caption):
    pid, w = brief["id"], []
    for i, s in enumerate(brief["slides"], 1):
        tag = f"{pid}-{i:02d}"
        p = s.get("plantilla")
        # Cuentan los bloques de contenido, no la cresta: marca_lugar, ciclo y
        # marca_cfdl son una línea al tamaño de etiqueta y no cargan la lámina.
        bloques = sum(1 for k in ("antetitulo", "titular", "subtitular", "fecha",
                                  "hora", "foto", "portadas", "bio", "presentacion",
                                  "agenda", "cita", "aforo", "tipo") if s.get(k))
        if bloques > TOPES.get(p, 99):
            w.append(f"{tag}: {bloques} bloques, el tope de «{p}» es "
                     f"{TOPES[p]} — reparte en más láminas del carrusel")
        if not s.get("alt"):
            w.append(f"{tag}: sin texto alternativo")
        f = s.get("foto")
        if f:
            ruta = os.path.normpath(os.path.join(SRC, f["src"]))
            if not os.path.exists(ruta):
                w.append(f"{tag}: la foto no existe — {f['src']}")
        for k, v in cadenas(s):
            if "!" in v or "¡" in v:
                w.append(f"{tag}.{k}: signo de exclamación")
            if EMOJI.search(v):
                w.append(f"{tag}.{k}: emoji")
            if " - " in v:
                w.append(f"{tag}.{k}: guion suelto donde va raya (—)")
            if CTA.search(v):
                w.append(f"{tag}.{k}: llamada a la acción")
        t = s.get("titular")
        t = " ".join(t) if isinstance(t, list) else (t or "")
        # La firma real del Title Case es una palabra funcional capitalizada a
        # media frase («La Fractura Profiláctica»). Un nombre propio con dos
        # mayúsculas («Ángela Mallén») es correcto y no debe saltar.
        if FUNCIONALES.search(t):
            w.append(f"{tag}.titular: parece Title Case — la casa usa caja de frase")
        if isinstance(s.get("titular"), str) and len(s["titular"]) > 40:
            w.append(f"{tag}.titular: {len(s['titular'])} caracteres sin saltos "
                     f"explícitos — usa una lista de líneas")
        if s.get("bio") and len(s["bio"]) > 340:
            w.append(f"{tag}.bio: {len(s['bio'])} caracteres (máx ~340)")
        # A 108px una cita larga desborda el lienzo. El canario lo caza en el
        # render, pero avisar antes sale más barato que renderizar para verlo.
        ct = (s.get("cita") or {}).get("texto", "")
        if len(ct) > 150:
            w.append(f"{tag}.cita: {len(ct)} caracteres — por encima de ~150 "
                     f"desborda a tamaño de display; recorta el fragmento")
    if len(brief["slides"]) > 6:
        w.append(f"{pid}: {len(brief['slides'])} láminas (máx recomendado 6)")
    if d["tag"] not in "".join(open(os.path.join(SRC, f"{pid}-01.html"),
                                    encoding="utf-8").read().split("<span class=sep>·</span>")[0:1]) \
            and "cfueradelloc" not in open(os.path.join(SRC, f"{pid}-01.html"),
                                           encoding="utf-8").read():
        w.append(f"{pid}: falta la marca de contacto")
    if "!" in caption or "¡" in caption or EMOJI.search(caption) or CTA.search(caption):
        w.append(f"{pid}.caption: exclamación, emoji o llamada a la acción")
    if "[PENDIENTE" in caption:
        w.append(f"{pid}.caption: es un andamio, falta escribirlo en voz C.F.D.L.")
    return w


# ── contraste con el calendario canónico ───────────────────────────────────
ENTRADA = re.compile(
    r"^\*\*(?P<dia>[^·*]+?)\s*·\s*(?P<titulo>.+?)\*\*"
    r"(?:\s*\*\((?P<sem>[^,)]+?)(?:,\s*(?P<hora>\d{1,2}:\d{2}))?\)\*)?"
    r"\s*—\s*(?P<lugar>.+?)\s*$")


def leer_calendario():
    if not os.path.exists(CAL):
        return {}
    ev, anio = {}, None
    for ln in open(CAL, encoding="utf-8"):
        ln = ln.rstrip("\n")
        m = re.match(r"^##\s+(\d{4})\s*$", ln)
        if m:
            anio = int(m.group(1)); continue
        m = ENTRADA.match(ln)
        if not m or not anio:
            continue
        md = re.search(r"(\d{1,2})\s+([a-záéíóú]+)", m.group("dia"))
        if not md or md.group(2)[:3] not in MES_ABBR:
            continue
        try:
            iso = datetime.date(anio, MES_ABBR[md.group(2)[:3]],
                                int(md.group(1))).isoformat()
        except ValueError:
            continue
        ev[iso] = {"sem": (m.group("sem") or "").strip().lower(),
                   "hora": m.group("hora") or "",
                   "lugar": m.group("lugar").strip(),
                   "titulo": m.group("titulo").strip()}
    return ev


def verificar(brief, cal):
    """Avisa, nunca rellena: un relleno silencioso haría que un brief pareciera
    autoritativo sin serlo. El calendario es la fuente de verdad de los hechos."""
    pid, w = brief["id"], []
    # Una cita del manifiesto no anuncia nada: no hay evento contra el que
    # contrastar y exigirle uno sería ruido.
    if not brief.get("evento_ref") and not any(
            s.get("fecha") or s.get("agenda") for s in brief["slides"]):
        return []
    ref = brief.get("evento_ref")
    if not ref:
        m = re.match(r"(\d{4}-\d{2}-\d{2})", pid)
        ref = m.group(1) if m else None
    if not ref:
        return [f"{pid}: sin evento_ref ni fecha en el id"]
    if ref not in cal:
        return [f"{pid}: {ref} no está en calendario-eventos.md — "
                f"actualiza primero el calendario"]
    c = cal[ref]
    sem_real, _, _ = fecha_larga(ref)
    for i, s in enumerate(brief["slides"], 1):
        f, h = s.get("fecha") or {}, s.get("hora") or {}
        if f.get("dia_semana") and f["dia_semana"].strip().lower() != sem_real:
            w.append(f"{pid}-{i:02d}: dice «{f['dia_semana']}» pero {ref} "
                     f"cae en {sem_real}")
        if c["sem"] and f.get("dia_semana") and \
                f["dia_semana"].strip().lower() != c["sem"]:
            w.append(f"{pid}-{i:02d}: día de la semana difiere del calendario "
                     f"({c['sem']})")
        if c["hora"] and h.get("texto") and h["texto"] != c["hora"]:
            w.append(f"{pid}-{i:02d}: hora {h['texto']} ≠ calendario {c['hora']}")
        lug = s.get("lugar")
        if lug and c["lugar"]:
            nom = lug if isinstance(lug, str) else lug.get("nombre", "")
            if nom and nom.split()[-1].lower() not in c["lugar"].lower() \
                    and c["lugar"].split()[-1].lower() not in nom.lower():
                w.append(f"{pid}-{i:02d}: lugar «{nom}» ≠ calendario «{c['lugar']}»")
    return w


# ── hoja de contactos ──────────────────────────────────────────────────────
def indice(briefs, d):
    filas = []
    for b in briefs:
        pid = b["id"]
        cap = os.path.join(OUT, f"{pid}.caption.txt")
        txt = open(cap, encoding="utf-8").read() if os.path.exists(cap) else ""
        laminas = ""
        for i in range(1, len(b["slides"]) + 1):
            png = f"{pid}-{i:02d}.png"
            if not os.path.exists(os.path.join(OUT, png)):
                continue
            laminas += (
                f'<div class="l"><div class="feed"><img src="{png}"></div>'
                f'<div class="cap3x4"><img src="{png}"><span class="crop"></span></div>'
                f'<div class="full"><img src="{png}"></div>'
                f'<div class="n">{png}</div></div>')
        filas.append(f'<section><h2>{html.escape(pid)}</h2>'
                     f'<div class="laminas">{laminas}</div>'
                     f'<pre>{html.escape(txt)}</pre></section>')
    doc = """<!doctype html><meta charset="utf-8"><title>C.F.D.L. — hoja de contactos</title>
<style>
body{font:14px/1.5 -apple-system,sans-serif;background:#1a1a1a;color:#eee;margin:0;padding:32px}
h1{font-size:18px;font-weight:400;letter-spacing:.2em;text-transform:uppercase}
h2{font-size:13px;font-weight:400;letter-spacing:.14em;text-transform:uppercase;color:#9a9a9a;margin:40px 0 12px}
section{border-top:1px solid #333;padding-top:16px}
.laminas{display:flex;flex-wrap:wrap;gap:28px}
.l{display:flex;gap:14px;align-items:flex-start}
.feed img{width:430px;display:block}
.cap3x4{position:relative;width:322px;overflow:hidden}
.cap3x4 img{width:430px;margin-left:-54px;display:block}
.cap3x4 .crop{position:absolute;inset:0;outline:2px dashed #4af;pointer-events:none}
.full img{width:1080px;display:block}
.n{writing-mode:vertical-rl;font-size:10px;color:#777;letter-spacing:.1em}
pre{white-space:pre-wrap;background:#242424;padding:16px;font-size:13px;max-width:700px;margin-top:16px}
.leyenda{color:#8a8a8a;font-size:12px;margin-bottom:8px}
</style>
<h1>C.F.D.L. — hoja de contactos</h1>
<p class="leyenda">Columna 1: 430&nbsp;px, el tamaño real en el feed — <b>si la fecha no se lee aquí, el cartel ha fallado</b>.
Columna 2: recorte 3:4 de la rejilla de perfil. Columna 3: 1080&nbsp;px para el detalle.</p>
""" + "".join(filas)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)


# ── principal ──────────────────────────────────────────────────────────────
def main():
    a = sys.argv[1:]
    tema = None
    for k, v in (("--pink", "pink"), ("--rosa", "pink"),
                 ("--citrine", "citrine"), ("--citrina", "citrine")):
        if k in a:
            tema = v
    solo = None
    if "--solo" in a:
        solo = a[a.index("--solo") + 1]
    debug = "--debug" in a

    os.makedirs(SRC, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    d = load_defaults()

    ficheros = sorted(f for f in glob.glob(os.path.join(POSTS, "*.json"))
                      if not os.path.basename(f).startswith("_"))
    if solo:
        ficheros = [f for f in ficheros if solo in os.path.basename(f)]
    if not ficheros:
        print("no hay briefs en posts/"); return

    # Borra sólo el HTML generado: _shared.css se escribe a mano y debe sobrevivir.
    for f in glob.glob(os.path.join(SRC, "*.html")):
        os.remove(f)

    briefs, avisos, n = [], [], 0
    for fp in ficheros:
        with open(fp, encoding="utf-8") as fh:
            b = json.load(fh)
        b.setdefault("id", os.path.splitext(os.path.basename(fp))[0])
        emit(b, d, tema, debug)
        cap = sidecars(b, d)
        briefs.append(b)
        n += len(b["slides"])
        if "--lint" in a:
            avisos += lint(b, d, cap)

    if "--verificar" in a:
        cal = leer_calendario()
        print(f"calendario: {len(cal)} entradas datadas")
        for b in briefs:
            avisos += verificar(b, cal)

    if "--indice" in a:
        indice(briefs, d)
        print(f"hoja de contactos → out/index.html")

    print(f"{len(briefs)} briefs, {n} láminas → src/*.html")
    if avisos:
        print(f"\n{len(avisos)} aviso(s):")
        for x in avisos:
            print("  ·", x)
    elif "--lint" in a or "--verificar" in a:
        print("sin avisos")


if __name__ == "__main__":
    main()
