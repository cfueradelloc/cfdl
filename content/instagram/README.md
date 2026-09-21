# Instagram — C.F.D.L.

Genera las publicaciones de [@cfueradelloc](https://www.instagram.com/cfueradelloc/) a
partir de datos estructurados, en la identidad del colectivo.

Mismo método que `content/tshirts/`: un emisor en Python de sólo biblioteca estándar
escribe `src/*.html`, y `render.sh` los fotografía con Chrome sin cabeza. Sin paso de
compilación, sin dependencias.

## Entrada y salida

**Una publicación son siempre dos cosas: una imagen y un texto.** El generador escribe
las dos.

```
ENTRADA                        SALIDA
posts/<id>.json  ──────────▶   out/<id>/01.png       la imagen
                               out/<id>/02.png       …y las demás, si es carrusel
                               out/<id>/caption.txt  el texto que la acompaña
                               out/<id>/alt.txt      el alternativo, una línea por lámina

                               out/index.html        todo lo anterior, enfrentado
```

**Una carpeta por publicación.** Al publicar abres `out/<id>/`, arrastras los PNG en
orden de nombre y copias `caption.txt`. Nada que buscar entre archivos sueltos.

Con varios formatos el nombre lo dice: `01-feed.png`, `01-historia.png`.

Un brief mínimo y lo que produce:

```json
{
  "id": "2025-12-12-angela-mallen",
  "theme": "pink",
  "slides": [{
    "plantilla": "evento",
    "ciclo": "en-voz-alta",
    "marca_cfdl": "logo+sigla",
    "titular": ["Ángela", "Mallén"],
    "tipo": "Lectura",
    "fecha": { "dia_semana": "viernes", "texto": "12 de diciembre", "anio": "2025" },
    "hora":  { "prefijo": "a partir de las", "texto": "19:30" },
    "lugar": "perecquiana",
    "alt": "Cartel de la lectura de Ángela Mallén."
  }],
  "caption": { "texto": "Cerramos «En voz alta» con Ángela Mallén…", "etiquetas": [] }
}
```

`plantilla` es la única clave obligatoria de una lámina. **Todo lo demás es un bloque que
se dibuja si está y desaparece si no** — por eso el mismo archivo sirve para un cartel
denso y para uno de tres líneas. Referencia completa y anotada en `posts/_ejemplo.json`.

**`out/index.html` es la pieza que hay que abrir para revisar**: enfrenta el JSON exacto
de cada lámina con el PNG que salió y con su texto. Las imágenes se muestran a 430 px, el
ancho real en el feed de un teléfono — *si la fecha no se lee ahí, el cartel ha fallado*.

## Reproducir

```bash
python3 build_posts.py --ejemplos --lint --verificar --indice
bash render.sh
open out/index.html
```

| bandera | qué hace |
|---|---|
| `--pink` / `--citrine` | fuerza el tema en toda la tirada (alias `--rosa` / `--citrina`) |
| `--formato feed\|cuadrado\|historia` | fuerza la proporción en toda la tirada |
| `--ejemplos` | construye también `ejemplos/`, un brief por plantilla |
| `--solo <texto>` | sólo los briefs cuyo nombre contenga ese texto |
| `--lint` | voz de la casa, topes de bloques, archivos y textos alternativos que faltan |
| `--verificar` | contrasta fecha, hora y lugar con `content/events/calendario-eventos.md` |
| `--indice` | la hoja de entrada/salida en `out/index.html` |
| `--debug` | superpone la retícula, el recorte 3:4 y la zona insegura de historias |
| `SCALE=2 bash render.sh` | maestro al doble (Instagram recorta a 1080 de ancho) |
| `bash render.sh <texto>` | renderiza sólo las páginas que casen |

## Formatos

Las tres proporciones que usa Instagram. Un brief puede pedir varias a la vez con
`"formatos": ["feed","cuadrado","historia"]`; entonces la salida lleva el formato en el
nombre (`<id>-01-historia.png`).

| clave | tamaño | para qué |
|---|---|---|
| `feed` *(por defecto)* | 1080×1350 (4:5) | la publicación de feed; la que más superficie ocupa en el scroll |
| `cuadrado` | 1080×1080 (1:1) | cuando también se cruza a otras plataformas |
| `historia` | 1080×1920 (9:16) | historias. Márgenes de 260/300 px porque ahí es donde la interfaz de Instagram tapa el contenido |

Cada formato reajusta la escala tipográfica: lo que respira a 1920 de alto se ahoga a 1080.

## Plantillas

| plantilla | qué es | tope de bloques |
|---|---|---|
| `evento` | una sesión: nombre, fecha, hora, lugar, foto opcional | 6 |
| `ciclo` | varias fechas en una tabla, con hora y lugar comunes | 9 |
| `recordatorio` | nombre, fecha, hora y nada más | 4 |
| `cita` | fragmento del manifiesto, sólo tipografía | 3 |
| `portada` | foto a toda página con el texto encima — la lámina 1 natural de un carrusel | 5 |
| `retrato` | foto y texto en dos columnas; da aire a un nombre largo | 6 |
| `programa` | secuencia con horas y detalle por acto | 9 |
| `datos` | información práctica en pares clave/valor | 8 |
| `resumen` | lo que se publica *después*: rejilla de fotos y dos frases | 6 |
| `pieza` | obra generativa de `docs/output/`, con su «Técnica — detalle» | 5 |
| `numero` | una cifra a gran tamaño (14,4 km, una edición, un aforo) | 4 |

**El tope de bloques es real, no un consejo.** La anatomía completa de un cartel impreso
—lugar, ciclo, presentación, sigla, nombre, día, hora, foto, portadas, bio, aforo, web,
QR— es un inventario de A3 que se lee a un brazo de distancia. En el feed esa imagen se ve
a ~430 pt: meter los trece bloques deja el cuerpo de texto a ~8 px reales. El carrusel es
la válvula de escape, y el linter la obliga.

## Logotipos

Dos cosas distintas:

- **La marca del colectivo** se redibuja en SVG desde `build_posts.py` (`marca_cfdl`): el
  cuadrado ámbar con «C.F. / D.L.» y el doble filete cuyas esquinas no cierran — la marca
  ya es, ella misma, algo fuera de lugar. No es el favicon del sitio, que es otra cosa.
  `logo` la dibuja en color; `logo-mono` a una sola tinta, para cuando el cartel no admite
  un cuadrado de color. El original está en `assets/logos/cfdl-logo-original.jpeg`.
- **Los logos ajenos** (lugar, colaboradores, quien financia) son archivos que se dejan a
  mano en `assets/logos/` y por defecto se pasan a **tinta plana**. Ver
  `assets/logos/README.md`.

## Dónde se toca cada cosa

- **`posts/*.json`** — la fuente escrita a mano. Un fichero por publicación.
- **`ejemplos/*.json`** — un brief por plantilla, ejecutable. Es la documentación real.
- **`src/_shared.css`** — **la superficie de ajuste**: retícula, escala, temas, formatos,
  tratamiento de foto. Se escribe a mano; `build_posts.py` no la genera nunca. Para afinar
  un cartel: `open src/<id>-01.html` en una pestaña de Chrome —es 1:1— y edita esta hoja en
  DevTools. El Python emite estructura, no diseño.
- **`defaults.json`** — lo que no cambia: marca de contacto, aforo, lugares, ciclos.
- **`ref/`** — capturas de referencia del perfil real. Entrada, no salida.

## Decisiones que conviene no deshacer sin pensarlo

- **Un carrusel no es otro formato.** Son N imágenes del mismo tamaño. Una sola vía de código.
- **La fecha es la carga útil**, no una etiqueta: va en serif de display, no en sans versaleada.
- **Un solo desplazamiento por cartel.** La fecha se sale de la retícula (`--desplazo`). El
  colectivo se llama Fuera de Lugar; el cartel lo hace en vez de decirlo. Tope 50 px: la
  rejilla de perfil recorta 34 px por lado y el desplazamiento debe seguir entero en la
  miniatura.
- **El acento es puntuación** —un separador, el año, la lámina activa— nunca un campo.
- **Los dos temas son objetos reales del colectivo.** `pink` es la identidad publicada en
  la web. `citrine` es su ámbar: el `#ffb923` del logotipo —muestreado del propio archivo,
  `assets/logos/cfdl-logo-original.jpeg`— y el del manifiesto impreso, ese acordeón
  amarillo de `docs/gallery/manifiesto-*.jpg`. `brand-content` lo llama «Citrina (marca)».
  Ojo: el `#e9ad51` de `content/tshirts/` es otra cosa —la aproximación al papel Colorplan
  Citrine, un punto más apagada—, así que los dos módulos no comparten ámbar.
- **El fallback de las tipografías es `monospace` a propósito.** Si Chrome no carga los OTF,
  todo sale en Courier y el fallo es imposible de pasar por alto. Un fallback «Georgia,
  serif» daría un cartel creíble pero fuera de marca, que es peor.
- **El canario.** Cada página se autoexamina al renderizar y estampa una banda magenta si
  algo se sale del lienzo, si dos zonas se pisan o si dos textos se solapan. Los tres casos
  han ocurrido durante el desarrollo y ninguno rompía nada visiblemente en el HTML.

## Límites conocidos

- **El tratamiento de foto es CSS, no ImageMagick.** `brand-content` prescribe `-normalize`,
  que es adaptativo por imagen; `contrast()` es un multiplicador fijo y no puede serlo. Una
  foto plana sale plana: ajústala a ojo con `foto.contraste` y `foto.brillo` contra la hoja
  de contactos. A cambio, cero dependencias.
- **Las fotos de `docs/gallery/` son 1600×900.** Por eso `foto.forma` es `banda` por defecto
  (1080×608, ratio nativo, sin recorte): un recorte vertical tira medio encuadre y suele
  cortar cabezas.
- **El QR no se genera.** En Instagram apenas sirve —no se escanea la pantalla que tienes en
  la mano— y codificarlo sin dependencias son ~200 líneas.
- **Los retratos de autor y las portadas están en Drive**, que ahora mismo no sirve los bytes
  en local. Cópialos a mano a `assets/`.
- **El perfil real no se ha podido leer** (exige inicio de sesión). Las plantillas se
  dedujeron de los carteles del Drive, del CSS del sitio y de las reglas de voz de
  `CLAUDE.md`. Deja capturas en `ref/` para afinarlas.
