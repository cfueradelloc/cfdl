#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C.F.D.L. — generador de publicaciones para Instagram.

ENTRADA   posts/<id>.json      un brief por publicación (JSON, escrito a mano)
SALIDA    out/<id>/01.png      la imagen (o varias, si es carrusel)
          out/<id>/caption.txt el texto que acompaña a la imagen
          out/<id>/alt.txt     el texto alternativo, una línea por lámina
          out/index.html       entrada y salida enfrentadas, para revisar

Una publicación son SIEMPRE dos cosas: imagen y texto. El generador escribe las
dos; si el brief no trae texto, emite un andamio marcado [PENDIENTE] y el
linter no deja pasar la publicación hasta que alguien lo escriba.

Sólo biblioteca estándar: aquí no hay Pillow, ImageMagick ni PyYAML. Por eso
los datos son JSON y todo el tratamiento de imagen ocurre en CSS/SVG en el
momento del render. El diseño vive en src/_shared.css, no en este archivo:
este archivo emite estructura y propiedades personalizadas.

    python3 build_posts.py --lint --verificar --indice
    bash render.sh
"""
import os, sys, json, glob, re, html, datetime

HERE  = os.path.dirname(os.path.abspath(__file__))
RAIZ  = os.path.normpath(os.path.join(HERE, "..", ".."))
SRC   = os.path.join(HERE, "src")
OUT   = os.path.join(HERE, "out")
POSTS = os.path.join(HERE, "posts")
EJEM  = os.path.join(HERE, "ejemplos")
CAL   = os.path.join(RAIZ, "content", "events", "calendario-eventos.md")

# ── formatos ───────────────────────────────────────────────────────────────
# Las tres proporciones que usa Instagram. 4:5 es la de feed (la que más
# superficie ocupa en el scroll); 1:1 para lo que también se cruza a otras
# plataformas; 9:16 para historias.
FORMATOS = {"feed": (1080, 1350), "cuadrado": (1080, 1080), "historia": (1080, 1920)}
FMT_ALIAS = {"4:5": "feed", "1:1": "cuadrado", "9:16": "historia",
             "story": "historia", "square": "cuadrado", "post": "feed"}

THEMES = {"pink":    {"duo_dark": "#332f8a", "duo_light": "#f8ccce"},
          "citrine": {"duo_dark": "#171513", "duo_light": "#ffb923"}}
ALIAS = {"rosa": "pink", "citrina": "citrine"}

MESES = ["enero","febrero","marzo","abril","mayo","junio",
         "julio","agosto","septiembre","octubre","noviembre","diciembre"]
MES_ABBR = {"ene":1,"feb":2,"mar":3,"abr":4,"may":5,"jun":6,
            "jul":7,"ago":8,"sep":9,"oct":10,"nov":11,"dic":12}
DIAS = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]

PLANTILLAS = {"evento","ciclo","recordatorio","cita","portada","retrato",
              "programa","datos","resumen","pieza","numero"}
# Tope de bloques de contenido por lámina. No es un consejo. En el feed una
# imagen se ve a ~430 pt: meter el inventario entero de un cartel impreso deja
# el cuerpo de texto a ~8 px reales. El carrusel es la válvula de escape.
TOPES = {"evento":6, "recordatorio":4, "cita":3, "portada":5, "retrato":6,
         "numero":4, "pieza":5, "datos":8, "programa":9, "ciclo":9, "resumen":6}

CTA = re.compile(r"\b(únete|unete|descubre|no te lo pierdas|reserva ya|apúntate|"
                 r"apuntate|corre|date prisa|últimas plazas|ultimas plazas|"
                 r"desliza|swipe|link en bio)\b", re.I)
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️←-⇿]")
# Detección de Title Case. Una palabra funcional capitalizada a media frase lo
# sugiere («La Fractura Profiláctica»), pero no basta: los nombres propios
# españoles llevan artículo dentro («Lorca en La Habana», «El Almíbar»). Lo que
# sí discrimina es que no quede NINGUNA palabra funcional en minúscula: si la
# hay, la frase está en caja de frase y el artículo alto es parte de un nombre.
_FUNC = ("de|del|la|el|los|las|un|una|y|o|en|a|al|ante|con|sin|por|para|"
         "que|su|sus|lo|se|como|desde|hasta|entre|sobre|tras")
_F_ALTA = re.compile(r"(?<!^)\b(" + _FUNC.title().replace("|", "|") + r")\b")
_F_BAJA = re.compile(r"\b(" + _FUNC + r")\b")


def parece_title_case(t):
    """Dos señales, ninguna de las cuales marca un nombre propio.

    A · palabra funcional capitalizada a media frase → «Publicar De Otra Manera».
    B · la frase ABRE con artículo y todo lo demás va en alta → «La Fractura
        Profiláctica». Que abra con artículo es lo que la separa de un nombre de
        persona: «Pablo Martín Sánchez» también va todo en alta, pero no empieza
        por artículo.
    Las dos exigen que no quede ninguna funcional en minúscula: si la hay, la
    frase está en caja de frase y el artículo alto es parte de un nombre
    («Lorca en La Habana»)."""
    if _F_BAJA.search(t):
        return False
    if _F_ALTA.search(t):
        return True
    pal = [w for w in t.split() if w[:1].isalpha()]
    return bool(len(pal) >= 3
                and re.match(r"^(" + _FUNC.title() + r")$", pal[0])
                and all(w[:1].isupper() for w in pal))


def esc(s): return html.escape(str(s), quote=True)
def hex01(h):
    h = h.lstrip("#")
    return tuple(round(int(h[i:i+2], 16)/255, 3) for i in (0, 2, 4))
def fecha_larga(iso):
    d = datetime.date.fromisoformat(iso)
    return DIAS[d.weekday()], f"{d.day} de {MESES[d.month-1]}", str(d.year)


def ruta(p):
    """Rutas de brief → rutas relativas a src/*.html.

    Un brief escribe `docs/gallery/x.jpg` (desde la raíz del repo) o
    `assets/retratos/x.jpg` (desde el módulo). Resolverlo aquí evita que quien
    escribe un brief tenga que contar cuántos `../` hacen falta.
    """
    if p.startswith(("http://", "https://", "data:")): return p
    if p.startswith(("docs/", "content/", "skills/")): return "../../../" + p
    return "../" + p.lstrip("./")


def ruta_abs(p):
    if p.startswith(("http://", "https://", "data:")): return None
    if p.startswith(("docs/", "content/", "skills/")): return os.path.join(RAIZ, p)
    return os.path.join(HERE, p.lstrip("./"))


def load_defaults():
    with open(os.path.join(HERE, "defaults.json"), encoding="utf-8") as f:
        return json.load(f)


def resolver(v, tabla):
    if isinstance(v, str):
        return tabla.get(v, {"nombre": v, "ciudad": "", "marca": v})
    return v or {}


# ── la marca del colectivo, dibujada ───────────────────────────────────────
# El favicon del sitio es una «C» de tres barras con un punto amarillo. Se
# redibuja en SVG en lugar de enlazar el PNG: así toma los colores del tema,
# funciona sobre fondo claro y oscuro, y no pixela a ningún tamaño.
def svg_marca(alto=44, mono=False):
    """El logotipo del colectivo, redibujado.

    No es el favicon del sitio (una «C» de barras): es el cuadrado ámbar con
    «C.F. / D.L.» en negro y un doble filete cuyas esquinas no cierran — el
    detalle deliberado que hace que la propia marca esté fuera de lugar.
    Muestreado de assets/logos/cfdl-logo-original.jpeg: el ámbar es #ffb923.

    Se redibuja en SVG en vez de enlazar el JPEG porque así no pixela a ningún
    tamaño, y porque `mono` permite ponerlo a una sola tinta cuando el cartel
    no admite un cuadrado de color.
    """
    fondo = "none" if mono else "#ffb923"
    tinta = "currentColor" if mono else "#171513"
    return (
      f'<svg class="marca" viewBox="0 0 100 100" width="{alto}" height="{alto}" '
      f'aria-label="C.F.D.L." role="img">'
      f'<rect width="100" height="100" fill="{fondo}"/>'
      # Filete exterior con una muesca en el borde superior, cerca de la
      # esquina izquierda: el trazo no llega a cerrar.
      f'<path d="M20 5 H95 V95 H5 V5 H11" fill="none" stroke="{tinta}" '
      f'stroke-width="1.9" stroke-linecap="square"/>'
      # Filete interior, cerrado, y una pata que se descuelga por la izquierda.
      f'<rect x="10.5" y="10.5" width="79" height="79" fill="none" '
      f'stroke="{tinta}" stroke-width="1.9"/>'
      f'<path d="M7 64 V95" fill="none" stroke="{tinta}" stroke-width="1.9" '
      f'stroke-linecap="square"/>'
      f'<text x="51" y="48" text-anchor="middle" fill="{tinta}" '
      f'font-family="FuturaStd, Helvetica, Arial" font-size="35" '
      f'letter-spacing="-0.5">C.F.</text>'
      f'<text x="51" y="84" text-anchor="middle" fill="{tinta}" '
      f'font-family="FuturaStd, Helvetica, Arial" font-size="35" '
      f'letter-spacing="-0.5">D.L.</text>'
      f'</svg>')


def marca_cfdl(s):
    """false | sigla | nombre | logo | logo+sigla | logo+nombre"""
    v = s.get("marca_cfdl")
    if not v: return ""
    v = str(v)
    mono = "mono" in v
    logo = svg_marca(s.get("marca_alto", 40), mono) if v.startswith("logo") else ""
    txt = ""
    if v.endswith("sigla") or v == "sigla":   txt = "C · F · D · L"
    elif v.endswith("nombre") or v == "nombre": txt = "Colectivo Fuera de Lugar"
    elif v in ("logo", "logo-mono"): txt = ""
    cuerpo = logo + (f'<div class="sigla">{esc(txt)}</div>' if txt else "")
    return f'<div class="marca-fila">{cuerpo}</div>' if cuerpo else ""


# ── bloques ────────────────────────────────────────────────────────────────
# Cada uno devuelve "" si su dato no está. Ése es el mecanismo de «todo bloque
# es opcional»: la plantilla enumera bloques, los datos deciden cuáles existen.
def b_marca_lugar(s):
    v = s.get("marca_lugar")
    return f'<div class="marca-lugar">{esc(v)}</div>' if v else ""

def b_strapline(s, ciclos):
    c = s.get("ciclo")
    if not c: return ""
    c = resolver(c, ciclos)
    t = c.get("nombre", "")
    if c.get("lema"): t += f" — {c['lema']}"
    return f'<div class="strapline mt2">{esc(t)}</div>'

def b_antetitulo(s):
    v = s.get("antetitulo")
    return f'<div class="kicker">{esc(v)}</div>' if v else ""

def b_titular(s, cls="hero"):
    v = s.get("titular")
    if not v: return ""
    ls = v if isinstance(v, list) else [v]
    return f'<div class="{cls} mt4">' + "<br>".join(esc(l) for l in ls) + "</div>"

def b_subtitular(s):
    v = s.get("subtitular")
    return f'<div class="sub mt2">{esc(v)}</div>' if v else ""

def b_fecha(s):
    f = s.get("fecha")
    if not f: return ""
    t = esc(" ".join(x for x in [f.get("dia_semana"), f.get("texto")] if x))
    if f.get("anio"): t += f' <span class="anio">{esc(f["anio"])}</span>'
    return f'<div class="fecha mt8">{t}</div>'

def b_hora(s):
    h = s.get("hora")
    if not h: return ""
    t = " ".join(x for x in [h.get("prefijo"), h.get("texto")] if x)
    if h.get("sufijo"): t += h["sufijo"]
    return f'<div class="hora mt2">{esc(t)}</div>'

def b_meta(s, lugares):
    lug = resolver(s.get("lugar"), lugares) if s.get("lugar") else {}
    if not lug.get("nombre"): return ""
    d = lug["nombre"] + (f", {lug['ciudad']}" if lug.get("ciudad") else "")
    t = f"{s['tipo']} — {d}" if s.get("tipo") else d
    return f'<div class="meta">{esc(t)}</div>'

def b_presentacion(s):
    v = s.get("presentacion")
    return f'<div class="meta mt4">{esc(v)}</div>' if v else ""

def b_bio(s):
    v = s.get("bio")
    return f'<div class="bio mt6 fitcheck">{esc(v)}</div>' if v else ""

def b_aforo(s):
    v = s.get("aforo")
    return f'<div class="aforo mt2">{esc(v)}</div>' if v else ""

def _foto(f, extra=""):
    forma = f.get("forma", "banda")
    trat  = f.get("tratamiento", "bn")
    st = []
    if f.get("encuadre"):  st.append(f'--encuadre:{f["encuadre"]}')
    if f.get("contraste"): st.append(f'--foto-contraste:{f["contraste"]}')
    if f.get("brillo"):    st.append(f'--foto-brillo:{f["brillo"]}')
    grano  = " grano" if f.get("grano") else ""
    sangre = " sangre" if forma in ("banda", "media", "alta") else ""
    return (f'<div class="foto f-{forma} t-{trat}{grano}{sangre}{extra}" '
            f'style="{";".join(st)}"><img src="{esc(ruta(f["src"]))}" alt=""></div>')

def b_foto(s):
    f = s.get("foto")
    return _foto(f) if f else ""

def b_rejilla(s):
    """Rejilla de fotos. Fuerza la forma «rej»: con la forma por defecto cada
    foto salía a sangre —1080 px de ancho y márgenes negativos— dentro de una
    rejilla de dos columnas, y reventaba el lienzo."""
    fs = s.get("fotos") or []
    if not fs: return ""
    n = min(len(fs), 4)
    celdas = "".join(_foto({**f, "forma": "rej"}) for f in fs[:4])
    return f'<div class="rejilla n{n} mt6 fitcheck">{celdas}</div>'

def b_portadas(s):
    ps = s.get("portadas") or []
    if not ps: return ""
    return ('<div class="portadas mt6">'
            + "".join(f'<img src="{esc(ruta(p["src"]))}" alt="">' for p in ps)
            + "</div>")

def b_logos(s, cls=""):
    """Logos ajenos: lugar, coproductores, quien financia.

    Llegan como vengan y por defecto se pasan a tinta plana. Un cartel en dos
    tintas con un rectángulo corporativo a todo color deja de ser un cartel
    del colectivo; con el filtro, la página sigue siendo suya."""
    L = s.get("logos")
    if not L: return ""
    if isinstance(L, dict): L = [L]
    trat = s.get("logos_trat", "tinta")
    alto = s.get("logos_alto")
    st = f'style="--logo-h:{alto}px"' if alto else ""
    cred = s.get("logos_cred")
    piezas = "".join(f'<img src="{esc(ruta(l["src"]))}" alt="{esc(l.get("alt",""))}">'
                     for l in L)
    if cred: piezas = f'<div class="cred">{esc(cred)}</div>' + piezas
    return f'<div class="logos t-{trat} {cls}" {st}>{piezas}</div>'

def b_agenda(s):
    fs = s.get("agenda") or []
    if not fs: return ""
    out = []
    for r in fs:
        f = " ".join(x for x in [r.get("dia"), r.get("fecha")] if x)
        out.append(f'<div class="fila"><div class="f">{esc(f)}</div>'
                   f'<div class="n">{esc(r.get("nombre",""))}</div></div>')
    return f'<div class="agenda mt8 fitcheck">{"".join(out)}</div>'

def b_programa(s):
    its = s.get("programa") or []
    if not its: return ""
    out = []
    for i in its:
        d = f'<div class="d">{esc(i["detalle"])}</div>' if i.get("detalle") else ""
        out.append(f'<div class="it"><div class="h">{esc(i.get("hora",""))}</div>'
                   f'<div><div class="t">{esc(i.get("titulo",""))}</div>{d}</div></div>')
    return f'<div class="programa mt8 fitcheck">{"".join(out)}</div>'

def b_datos(s):
    fs = s.get("datos") or []
    if not fs: return ""
    out = "".join(f'<div class="fila"><div class="k">{esc(k)}</div>'
                  f'<div class="v">{esc(v)}</div></div>' for k, v in
                  (list(d.items())[0] for d in fs))
    return f'<div class="datos mt8 fitcheck">{out}</div>'

def b_cita(s):
    c = s.get("cita")
    if not c: return ""
    o = f'<div class="cita-txt fitcheck">«{esc(c["texto"])}»</div>'
    if c.get("fuente"): o += f'<div class="cita-src mt8">{esc(c["fuente"])}</div>'
    return o

def b_numero(s):
    n = s.get("numero")
    if not n: return ""
    u = f'<span class="u"> {esc(n["unidad"])}</span>' if isinstance(n, dict) and n.get("unidad") else ""
    v = n["valor"] if isinstance(n, dict) else n
    return f'<div class="numero">{esc(v)}{u}</div>'

def b_tecnica(s):
    v = s.get("tecnica")
    return f'<div class="meta mt4">{esc(v)}</div>' if v else ""

def b_pie(s, tag, n, total):
    izq = marca_cfdl(s)
    pag = ""
    if s.get("paginacion", total > 1) and total > 1:
        pts = " · ".join((f'<span class="hoy">{i}</span>' if i == n else str(i))
                         for i in range(1, total + 1))
        pag = f'<div class="pag">{pts}</div>'
    marca = tag.replace("·", "<span class=sep>·</span>")
    return (f'<div class="pie mt8"><div class="izq">{izq}'
            f'<div class="tag">{marca}</div></div>{pag}</div>')


# ── recetas ────────────────────────────────────────────────────────────────
def receta(s, d, n, total):
    lugares, ciclos, tag = d["lugares"], d["ciclos"], d["tag"]
    p = s["plantilla"]
    foto = b_foto(s)
    sup = med = inf = ""

    if p == "evento":
        sup = b_marca_lugar(s) + b_strapline(s, ciclos)
        med = (b_antetitulo(s) + b_titular(s) + b_subtitular(s) + b_fecha(s)
               + b_hora(s) + b_presentacion(s) + b_bio(s) + b_portadas(s))
        inf = b_meta(s, lugares) + b_aforo(s) + b_logos(s, "logos-pie") + b_pie(s, tag, n, total)

    elif p == "ciclo":
        sup = b_marca_lugar(s) + b_strapline(s, ciclos)
        c = resolver(s.get("ciclo"), ciclos) if s.get("ciclo") else {}
        hero = b_titular(s) or (f'<div class="hero mt4">{esc(c.get("nombre",""))}</div>' if c else "")
        lema = (f'<div class="sub mt2">{esc(c["lema"])}</div>'
                if c.get("lema") and not s.get("subtitular") else b_subtitular(s))
        med = b_antetitulo(s) + hero + lema + b_agenda(s) + b_hora(s)
        inf = b_meta(s, lugares) + b_aforo(s) + b_logos(s, "logos-pie") + b_pie(s, tag, n, total)

    elif p == "recordatorio":
        med = b_titular(s, "display") + b_subtitular(s) + b_hora(s)
        inf = b_meta(s, lugares) + b_aforo(s) + b_pie(s, tag, n, total)

    elif p == "cita":
        med = b_cita(s)
        inf = b_logos(s, "logos-pie") + b_pie(s, tag, n, total)

    # Portada: la foto ocupa el lienzo entero y el texto se apoya encima, sobre
    # un velo. Es la lámina 1 natural de un carrusel.
    elif p == "portada":
        sup = b_marca_lugar(s) + b_strapline(s, ciclos)
        med = ""
        inf = (b_antetitulo(s) + b_titular(s) + b_subtitular(s) + b_fecha(s)
               + b_hora(s) + b_meta(s, lugares) + b_logos(s, "logos-pie")
               + b_pie(s, tag, n, total))
        foto = ""   # va al fondo, no a su fila

    # Retrato: foto y texto en dos columnas. Da aire a un nombre largo sin
    # tener que encoger la foto a una banda.
    elif p == "retrato":
        lado = s.get("lado", "izq")
        cols = (_foto(s["foto"], " ") if s.get("foto") else "")
        txt = (f'<div>{b_antetitulo(s)}{b_titular(s)}{b_subtitular(s)}'
               f'{b_fecha(s)}{b_hora(s)}{b_bio(s)}{b_portadas(s)}</div>')
        med = (f'<div class="par {lado}">'
               + (cols + txt if lado == "izq" else txt + cols) + "</div>")
        sup = b_marca_lugar(s) + b_strapline(s, ciclos)
        inf = b_meta(s, lugares) + b_aforo(s) + b_logos(s, "logos-pie") + b_pie(s, tag, n, total)
        foto = ""

    elif p == "programa":
        sup = b_marca_lugar(s) + b_strapline(s, ciclos)
        med = b_antetitulo(s) + b_titular(s) + b_subtitular(s) + b_programa(s)
        inf = b_meta(s, lugares) + b_aforo(s) + b_logos(s, "logos-pie") + b_pie(s, tag, n, total)

    elif p == "datos":
        sup = b_marca_lugar(s) + b_strapline(s, ciclos)
        med = b_antetitulo(s) + b_titular(s) + b_datos(s)
        inf = b_aforo(s) + b_logos(s, "logos-pie") + b_pie(s, tag, n, total)

    # Resumen: lo que se publica DESPUÉS del evento. Rejilla de fotos y dos
    # frases. El colectivo ya tiene 39 fotos publicadas en docs/gallery/.
    elif p == "resumen":
        sup = b_marca_lugar(s) + b_strapline(s, ciclos)
        med = (b_antetitulo(s) + b_titular(s) + b_subtitular(s) + b_rejilla(s)
               + b_bio(s) + b_portadas(s))
        inf = b_meta(s, lugares) + b_logos(s, "logos-pie") + b_pie(s, tag, n, total)

    # Pieza: obra generativa de docs/output/. El sitio ya describe cada una
    # como «Técnica — detalle»; aquí se reutiliza tal cual.
    elif p == "pieza":
        sup = b_antetitulo(s)
        med = b_titular(s) + b_subtitular(s) + b_tecnica(s) + b_bio(s)
        inf = b_logos(s, "logos-pie") + b_pie(s, tag, n, total)

    elif p == "numero":
        sup = b_antetitulo(s)
        med = b_numero(s) + b_subtitular(s) + b_bio(s)
        inf = b_meta(s, lugares) + b_logos(s, "logos-pie") + b_pie(s, tag, n, total)

    else:
        raise SystemExit(f"plantilla desconocida: {p}")

    return sup, med, foto, inf


# ── canario ────────────────────────────────────────────────────────────────
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
 # 2 · las zonas no pueden pisarse
 "var z=['.zona-sup','.zona-med','.zona-foto','.zona-inf']"
 ".map(function(q){var e=st.querySelector(q);"
 "return e&&e.getBoundingClientRect().height?e:null;}).filter(Boolean);"
 "for(var i=0;i<z.length-1;i++){"
 "var a=z[i].getBoundingClientRect(),c=z[i+1].getBoundingClientRect();"
 "if(a.bottom>c.top+1){marca(z[i]);marca(z[i+1]);mal.push('zonas solapadas');}}"
 # 3 · ni dos textos entre sí
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
<html lang="es" class="f-{fmt}"><head><meta charset="utf-8">
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
<div class="stage tema-{theme} sup-{sup} v-{var} {extra} fitcheck">
{fondo}
<div class="zona-sup">{z1}</div>
<div class="zona-med">{z2}</div>
<div class="zona-foto">{zf}</div>
<div class="zona-inf">{z3}</div>
</div>
<script>{canario}</script>
</body></html>
"""


def emit(brief, d, forzar_tema=None, forzar_fmt=None, debug=False):
    pid = brief["id"]
    fmts = [forzar_fmt] if forzar_fmt else (
        brief.get("formatos") or [brief.get("formato", "feed")])
    fmts = [FMT_ALIAS.get(f, f) for f in fmts]
    for f in fmts:
        if f not in FORMATOS: raise SystemExit(f"{pid}: formato desconocido «{f}»")
    varios = len(fmts) > 1
    slides = brief["slides"]
    total = len(slides)
    hechos = []

    for fmt in fmts:
        for i, raw in enumerate(slides, 1):
            s = dict(raw)
            # Ojo: ALIAS.get(x, "pink") se tragaba los nombres válidos —
            # «citrine» no está en ALIAS, así que caía al valor por defecto y
            # todo salía en rosa. El alias se resuelve sobre sí mismo.
            th = (forzar_tema or s.get("theme") or brief.get("theme")
                  or d.get("theme", "pink"))
            th = ALIAS.get(th, th)
            if th not in THEMES: raise SystemExit(f"{pid}: tema desconocido «{th}»")
            if s.get("plantilla") not in PLANTILLAS:
                raise SystemExit(f"{pid}: plantilla desconocida «{s.get('plantilla')}»")
            for k in ("marca_lugar", "ciclo", "logos", "logos_trat"):
                if i == 1 and k not in s and k in brief: s[k] = brief[k]

            fs0 = s.get("foto")
            if (s["plantilla"] == "portada" or
                    (fs0 and fs0.get("forma") == "sangre")):
                # Sobre una foto a sangre siempre se escribe encima del velo,
                # así que la superficie es oscura salvo que se diga lo contrario.
                s.setdefault("superficie", "oscuro")
            z1, z2, zf, z3 = receta(s, d, i, total)

            # Portada y cualquier lámina con foto «sangre»: la imagen va al
            # fondo con un velo, y las zonas se le montan encima.
            fondo, extra = "", []
            fs = s.get("foto")
            if s["plantilla"] == "portada" and fs:
                f2 = dict(fs); f2["forma"] = "sangre"
                # Si hay cresta arriba, el velo tiene que oscurecer los dos
                # extremos: si no, el ciclo se pierde sobre una foto con detalle.
                velo = s.get("velo") or ("v-ambos" if z1.strip() else "")
                fondo = _foto(f2) + f'<div class="velo {velo}"></div>'
                extra.append("con-sangre")
            elif fs and fs.get("forma") == "sangre":
                fondo = zf + f'<div class="velo {s.get("velo","")}"></div>'
                zf = ""
                extra.append("con-sangre")
            if s.get("alinear") == "der": extra.append("al-der")
            if s.get("recto"): extra.append("recto")
            if debug: extra.append("debug")

            dk, lt = hex01(THEMES[th]["duo_dark"]), hex01(THEMES[th]["duo_light"])
            page = PAGE.format(
                id=esc(pid), n=i, fmt=fmt, theme=th,
                sup=s.get("superficie", "claro"), var=s.get("variante", "centro"),
                extra=" ".join(extra), fondo=fondo,
                dr=dk[0], dg=dk[1], db=dk[2], lr=lt[0], lg=lt[1], lb=lt[2],
                z1=z1, z2=z2, zf=zf, z3=z3, canario=CANARIO)
            # Una carpeta por publicación: al publicar quieres las imágenes y
            # su texto juntos, no repartidos por tipo de archivo.
            base = f"{pid}/{i:02d}" + (f"-{fmt}" if varios else "")
            plano = base.replace("/", "~")   # src/ se mantiene plano
            with open(os.path.join(SRC, plano + ".html"), "w", encoding="utf-8") as fh:
                fh.write(page)
            hechos.append((plano, base, *FORMATOS[fmt], fmt))
    return hechos


# ── imagen + texto: las dos mitades de una publicación ─────────────────────
def sidecars(brief, d):
    pid = brief["id"]
    cap = brief.get("caption") or {}
    texto = cap.get("texto")
    if not texto:
        # Andamio a partir de los datos. No intenta la voz del colectivo: eso
        # es escritura, no formato. El linter no deja publicar un andamio.
        s0 = brief["slides"][0]
        lug = resolver(s0.get("lugar"), d["lugares"]) if s0.get("lugar") else {}
        ln = []
        if s0.get("tipo") and lug.get("nombre"):
            ln.append(f"{s0['tipo']} — {lug['nombre']}"
                      + (f", {lug['ciudad']}" if lug.get("ciudad") else ""))
        f, h = s0.get("fecha") or {}, s0.get("hora") or {}
        if f:
            ln.append(" ".join(x for x in [f.get("dia_semana"), f.get("texto")] if x)
                      + (f", {h['texto']}" if h.get("texto") else ""))
        if s0.get("aforo") or d.get("aforo"): ln.append(s0.get("aforo") or d["aforo"])
        texto = "[PENDIENTE — escribir en voz C.F.D.L.]\n\n" + "\n".join(ln) \
                + f"\n\n{d['sitio']}"
    et = cap.get("etiquetas", d.get("etiquetas_por_defecto", []))
    if et: texto += "\n\n" + " ".join("#" + e.lower().lstrip("#") for e in et)
    dst = os.path.join(OUT, pid)
    os.makedirs(dst, exist_ok=True)
    with open(os.path.join(dst, "caption.txt"), "w", encoding="utf-8") as fh:
        fh.write(texto.rstrip() + "\n")
    alts = [f"{i:02d}: {s.get('alt','[FALTA texto alternativo]')}"
            for i, s in enumerate(brief["slides"], 1)]
    with open(os.path.join(dst, "alt.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(alts) + "\n")
    return texto


# ── linter ─────────────────────────────────────────────────────────────────
def cadenas(s):
    for k in ("titular","subtitular","antetitulo","bio","aforo","presentacion",
              "marca_lugar","alt","tecnica"):
        v = s.get(k)
        if isinstance(v, list): yield from ((k, x) for x in v)
        elif isinstance(v, str): yield (k, v)
    if isinstance(s.get("cita"), dict): yield ("cita", s["cita"].get("texto",""))

CONTENIDO = ("antetitulo","titular","subtitular","fecha","hora","foto","fotos",
             "portadas","bio","presentacion","agenda","programa","datos","cita",
             "numero","tecnica","aforo","tipo")

def lint(brief, d, caption):
    pid, w = brief["id"], []
    for i, s in enumerate(brief["slides"], 1):
        tag, p = f"{pid}-{i:02d}", s.get("plantilla")
        n = sum(1 for k in CONTENIDO if s.get(k))
        if n > TOPES.get(p, 99):
            w.append(f"{tag}: {n} bloques, el tope de «{p}» es {TOPES[p]} — "
                     f"reparte en más láminas del carrusel")
        if not s.get("alt"): w.append(f"{tag}: sin texto alternativo")
        for f in ([s["foto"]] if s.get("foto") else []) + (s.get("fotos") or []) \
                 + (s.get("portadas") or []) + (
                     s.get("logos") if isinstance(s.get("logos"), list)
                     else [s["logos"]] if s.get("logos") else []):
            a = ruta_abs(f["src"])
            if a and not os.path.exists(a):
                w.append(f"{tag}: no existe el archivo — {f['src']}")
        for k, v in cadenas(s):
            if "!" in v or "¡" in v: w.append(f"{tag}.{k}: signo de exclamación")
            if EMOJI.search(v):      w.append(f"{tag}.{k}: emoji")
            if " - " in v:           w.append(f"{tag}.{k}: guion suelto donde va raya (—)")
            if CTA.search(v):        w.append(f"{tag}.{k}: llamada a la acción")
        t = s.get("titular")
        t = " ".join(t) if isinstance(t, list) else (t or "")
        if parece_title_case(t):
            w.append(f"{tag}.titular: parece Title Case — la casa usa caja de frase")
        if isinstance(s.get("titular"), str) and len(s["titular"]) > 40:
            w.append(f"{tag}.titular: {len(s['titular'])} caracteres sin saltos "
                     f"explícitos — usa una lista de líneas")
        if s.get("bio") and len(s["bio"]) > 340:
            w.append(f"{tag}.bio: {len(s['bio'])} caracteres (máx ~340)")
        ct = (s.get("cita") or {}).get("texto", "")
        if len(ct) > 150:
            w.append(f"{tag}.cita: {len(ct)} caracteres — desborda a tamaño de "
                     f"display; recorta el fragmento")
    if len(brief["slides"]) > 6:
        w.append(f"{pid}: {len(brief['slides'])} láminas (máx recomendado 6)")
    if "!" in caption or "¡" in caption or EMOJI.search(caption) or CTA.search(caption):
        w.append(f"{pid}.caption: exclamación, emoji o llamada a la acción")
    if "[PENDIENTE" in caption:
        w.append(f"{pid}.caption: es un andamio — una publicación es imagen Y "
                 f"texto; falta escribirlo en voz C.F.D.L.")
    return w


# ── contraste con el calendario ────────────────────────────────────────────
ENTRADA = re.compile(
    r"^\*\*(?P<dia>[^·*]+?)\s*·\s*(?P<titulo>.+?)\*\*"
    r"(?:\s*\*\((?P<sem>[^,)]+?)(?:,\s*(?P<hora>\d{1,2}:\d{2}))?\)\*)?"
    r"\s*—\s*(?P<lugar>.+?)\s*$")

def leer_calendario():
    if not os.path.exists(CAL): return {}
    ev, anio = {}, None
    for ln in open(CAL, encoding="utf-8"):
        ln = ln.rstrip("\n")
        m = re.match(r"^##\s+(\d{4})\s*$", ln)
        if m: anio = int(m.group(1)); continue
        m = ENTRADA.match(ln)
        if not m or not anio: continue
        md = re.search(r"(\d{1,2})\s+([a-záéíóú]+)", m.group("dia"))
        if not md or md.group(2)[:3] not in MES_ABBR: continue
        try:
            iso = datetime.date(anio, MES_ABBR[md.group(2)[:3]], int(md.group(1))).isoformat()
        except ValueError: continue
        ev[iso] = {"sem": (m.group("sem") or "").strip().lower(),
                   "hora": m.group("hora") or "",
                   "lugar": m.group("lugar").strip(),
                   "titulo": m.group("titulo").strip()}
    return ev

def verificar(brief, cal):
    """Avisa, nunca rellena: un relleno silencioso haría que un brief pareciera
    autoritativo sin serlo. El calendario manda sobre los hechos."""
    pid, w = brief["id"], []
    if not brief.get("evento_ref") and not any(
            s.get("fecha") or s.get("agenda") for s in brief["slides"]):
        return []
    ref = brief.get("evento_ref")
    if not ref:
        m = re.match(r"(\d{4}-\d{2}-\d{2})", pid)
        ref = m.group(1) if m else None
    if not ref: return [f"{pid}: sin evento_ref ni fecha en el id"]
    if ref not in cal:
        return [f"{pid}: {ref} no está en calendario-eventos.md — actualiza "
                f"primero el calendario"]
    c = cal[ref]
    sem_real, _, _ = fecha_larga(ref)
    for i, s in enumerate(brief["slides"], 1):
        f, h = s.get("fecha") or {}, s.get("hora") or {}
        if f.get("dia_semana") and f["dia_semana"].strip().lower() != sem_real:
            w.append(f"{pid}-{i:02d}: dice «{f['dia_semana']}» pero {ref} cae en {sem_real}")
        if c["hora"] and h.get("texto") and h["texto"] != c["hora"]:
            w.append(f"{pid}-{i:02d}: hora {h['texto']} ≠ calendario {c['hora']}")
        lug = s.get("lugar")
        if lug and c["lugar"]:
            nom = lug if isinstance(lug, str) else lug.get("nombre", "")
            if nom and nom.split()[-1].lower() not in c["lugar"].lower() \
                    and c["lugar"].split()[-1].lower() not in nom.lower():
                w.append(f"{pid}-{i:02d}: lugar «{nom}» ≠ calendario «{c['lugar']}»")
    return w


# ── hoja de revisión: entrada y salida enfrentadas ─────────────────────────
HOJA_CSS = """
*{box-sizing:border-box}
body{font:14px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace;
     background:#12121a;color:#e8e8ef;margin:0;padding:40px 44px}
h1{font:400 15px/1.3 system-ui;letter-spacing:.24em;text-transform:uppercase;
   color:#fff;margin:0 0 6px}
.intro{font:400 14px/1.7 system-ui;color:#9a9ab0;max-width:900px;margin:0 0 36px}
.intro b{color:#e8e8ef;font-weight:500}
.intro code{background:#22222e;padding:2px 6px;border-radius:3px;font-size:13px}
h2{font:400 13px/1.3 system-ui;letter-spacing:.16em;text-transform:uppercase;
   color:#fff;margin:0;padding:0}
.post{border:1px solid #2a2a38;border-radius:6px;margin:0 0 28px;overflow:hidden}
.cab{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;
     background:#1b1b26;padding:14px 18px;border-bottom:1px solid #2a2a38}
.chip{font:400 11px/1 system-ui;letter-spacing:.1em;text-transform:uppercase;
      background:#2e2e3e;color:#b9b9cc;padding:5px 9px;border-radius:3px}
.chip.t{background:#332f8a;color:#f8ccce}
.chip.f{background:#5a4a12;color:#ffd25a}
.lam{display:grid;grid-template-columns:1fr 470px;gap:0;border-top:1px solid #2a2a38}
.lam:first-of-type{border-top:0}
.ent,.sal{padding:18px}
.ent{border-right:1px solid #2a2a38;min-width:0}
.rot{font:400 10px/1 system-ui;letter-spacing:.22em;text-transform:uppercase;
     color:#6f6f88;margin-bottom:10px}
pre{margin:0;white-space:pre-wrap;word-break:break-word;font-size:12.5px;
    line-height:1.55;color:#c9c9dc}
.k{color:#8fb6ff}.s{color:#ffd28a}.n{color:#a6e3a1}.b{color:#f38ba8}
.sal img{width:430px;display:block;border:1px solid #2a2a38}
.sal .nom{font-size:11px;color:#6f6f88;margin-top:8px}
.txt{background:#1b1b26;border-top:1px solid #2a2a38;padding:18px;
     display:grid;grid-template-columns:1fr 1fr;gap:18px}
.txt pre{font:400 13.5px/1.65 system-ui;color:#dcdce8;white-space:pre-wrap}
.falta{color:#ff7ab8}
"""

def _json_color(o):
    t = json.dumps(o, ensure_ascii=False, indent=2)
    t = html.escape(t)
    t = re.sub(r'&quot;([^&]*?)&quot;(\s*:)', r'<span class="k">"\1"</span>\2', t)
    t = re.sub(r'(:\s)&quot;(.*?)&quot;', r'\1<span class="s">"\2"</span>', t)
    t = re.sub(r'(:\s)(-?\d+\.?\d*)', r'\1<span class="n">\2</span>', t)
    t = re.sub(r'(:\s)(true|false|null)', r'\1<span class="b">\2</span>', t)
    return t


def indice(briefs, d, hechos):
    """La página que contesta a «¿cómo es la entrada y cómo es la salida?».

    Cada lámina se muestra con el JSON exacto que la produjo al lado de la
    imagen que salió, y debajo el texto que la acompaña. Nada de adivinar qué
    clave hizo qué."""
    sec = []
    for b in briefs:
        pid = b["id"]
        s0 = b["slides"][0]
        fmts = b.get("formatos") or [b.get("formato", "feed")]
        chips = (f'<span class="chip t">{b.get("theme", d.get("theme"))}</span>'
                 + "".join(f'<span class="chip f">{FMT_ALIAS.get(f,f)} '
                           f'{FORMATOS[FMT_ALIAS.get(f,f)][0]}×'
                           f'{FORMATOS[FMT_ALIAS.get(f,f)][1]}</span>' for f in fmts)
                 + "".join(f'<span class="chip">{s["plantilla"]}</span>'
                           for s in b["slides"]))
        lams = ""
        for i, s in enumerate(b["slides"], 1):
            pngs = [h[1] for h in hechos if h[1].startswith(f"{pid}/{i:02d}")]
            imgs = "".join(
                f'<img src="{p}.png" alt=""><div class="nom">out/{p}.png</div>'
                for p in pngs if os.path.exists(os.path.join(OUT, p + ".png")))
            lams += (f'<div class="lam"><div class="ent">'
                     f'<div class="rot">entrada · posts/{html.escape(pid)}.json '
                     f'→ slides[{i-1}]</div><pre>{_json_color(s)}</pre></div>'
                     f'<div class="sal"><div class="rot">salida</div>{imgs}</div></div>')
        cap = os.path.join(OUT, pid, "caption.txt")
        alt = os.path.join(OUT, pid, "alt.txt")
        ct = open(cap, encoding="utf-8").read() if os.path.exists(cap) else ""
        at = open(alt, encoding="utf-8").read() if os.path.exists(alt) else ""
        cls = ' class="falta"' if "[PENDIENTE" in ct else ""
        sec.append(
            f'<div class="post"><div class="cab"><h2>{html.escape(pid)}</h2>{chips}</div>'
            f'{lams}'
            f'<div class="txt"><div><div class="rot">salida · out/{html.escape(pid)}'
            f'/caption.txt — el texto de la publicación</div>'
            f'<pre{cls}>{html.escape(ct)}</pre></div>'
            f'<div><div class="rot">salida · out/{html.escape(pid)}/alt.txt — '
            f'texto alternativo por lámina</div><pre>{html.escape(at)}</pre></div>'
            f'</div></div>')

    doc = (f'<!doctype html><meta charset="utf-8">'
           f'<title>C.F.D.L. — Instagram · entrada y salida</title>'
           f'<style>{HOJA_CSS}</style>'
           f'<h1>C.F.D.L. — Instagram</h1>'
           f'<p class="intro">Cada fila enfrenta <b>la entrada</b> —el JSON exacto de esa '
           f'lámina en <code>posts/&lt;id&gt;.json</code>— con <b>la salida</b>: el PNG y, '
           f'debajo, el texto que lo acompaña. Una publicación son siempre las dos cosas.<br>'
           f'Las imágenes se muestran a <b>430&nbsp;px</b>, el ancho real en el feed de un '
           f'teléfono: <b>si la fecha no se lee aquí, el cartel ha fallado</b>, por bien que '
           f'se vea a 1080. La maquetación se ajusta en <code>src/_shared.css</code>, '
           f'nunca en el Python.</p>'
           + "".join(sec))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)


# ── principal ──────────────────────────────────────────────────────────────
def main():
    a = sys.argv[1:]
    tema = None
    for k, v in (("--pink","pink"),("--rosa","pink"),
                 ("--citrine","citrine"),("--citrina","citrine")):
        if k in a: tema = v
    fmt = None
    if "--formato" in a:
        fmt = FMT_ALIAS.get(a[a.index("--formato")+1], a[a.index("--formato")+1])
        if fmt not in FORMATOS:
            raise SystemExit(f"formato desconocido; usa {', '.join(FORMATOS)}")
    solo = a[a.index("--solo")+1] if "--solo" in a else None
    debug = "--debug" in a

    os.makedirs(SRC, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    d = load_defaults()

    fich = sorted(f for f in glob.glob(os.path.join(POSTS, "*.json"))
                  if not os.path.basename(f).startswith("_"))
    ejemplos = set()
    if "--ejemplos" in a and os.path.isdir(EJEM):
        ej = sorted(glob.glob(os.path.join(EJEM, "*.json")))
        ejemplos = {os.path.splitext(os.path.basename(f))[0] for f in ej}
        fich += ej
    if solo:
        fich = [f for f in fich if solo in os.path.basename(f)]
    if not fich:
        print("no hay briefs que construir"); return

    # Sólo el HTML generado: _shared.css se escribe a mano y debe sobrevivir.
    for f in glob.glob(os.path.join(SRC, "*.html")): os.remove(f)

    briefs, avisos, hechos = [], [], []
    for fp in fich:
        with open(fp, encoding="utf-8") as fh: b = json.load(fh)
        b.setdefault("id", os.path.splitext(os.path.basename(fp))[0])
        hechos += emit(b, d, tema, fmt, debug)
        cap = sidecars(b, d)
        briefs.append(b)
        if "--lint" in a: avisos += lint(b, d, cap)

    # render.sh no puede adivinar el tamaño de ventana de cada página: se lo
    # decimos aquí, en texto plano, para no meter jq ni python en el bash.
    with open(os.path.join(SRC, "_sizes.txt"), "w", encoding="utf-8") as fh:
        for plano, base, W, H, _ in hechos: fh.write(f"{plano} {base} {W} {H}\n")

    if "--verificar" in a:
        cal = leer_calendario()
        print(f"calendario: {len(cal)} entradas datadas")
        for b in briefs:
            # Un ejemplo ilustra una plantilla; no anuncia nada que el
            # calendario tenga que confirmar.
            if b["id"] not in ejemplos: avisos += verificar(b, cal)

    if "--indice" in a:
        indice(briefs, d, hechos)
        print("hoja de entrada/salida → out/index.html")

    porfmt = {}
    for *_, f in hechos: porfmt[f] = porfmt.get(f, 0) + 1
    detalle = ", ".join(f"{v} en {k}" for k, v in sorted(porfmt.items()))
    print(f"{len(briefs)} briefs, {len(hechos)} láminas ({detalle}) → src/*.html")
    print(f"{len(briefs)} carpetas en out/ — imagen(es) + caption.txt + alt.txt")
    if avisos:
        print(f"\n{len(avisos)} aviso(s):")
        for x in avisos: print("  ·", x)
    elif "--lint" in a or "--verificar" in a:
        print("sin avisos")


if __name__ == "__main__":
    main()
