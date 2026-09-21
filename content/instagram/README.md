# Instagram — C.F.D.L.

Genera las imágenes de anuncio para [@cfueradelloc](https://www.instagram.com/cfueradelloc/)
a partir de datos estructurados, en la identidad del colectivo. **1080×1350 (4:5)**, el
formato de feed de Instagram; un carrusel es simplemente un brief con varias láminas.

Mismo método que `content/tshirts/`: un emisor en Python de sólo biblioteca estándar
escribe `src/*.html`, y `render.sh` los fotografía con Chrome sin cabeza. Sin paso de
compilación, sin dependencias.

## Reproducir

```bash
python3 build_posts.py --lint --verificar --indice   # briefs → src/*.html + out/*.txt
bash render.sh                                       # src/*.html → out/*.png
open out/index.html                                  # hoja de contactos
```

| bandera | qué hace |
|---|---|
| `--pink` / `--citrine` | fuerza el tema en toda la tirada (alias `--rosa` / `--citrina`) |
| `--solo <texto>` | sólo los briefs cuyo nombre contenga ese texto |
| `--lint` | voz de la casa, topes de bloques, fotos que faltan, alt que faltan |
| `--verificar` | contrasta fecha, hora y lugar con `content/events/calendario-eventos.md` |
| `--indice` | hoja de contactos en `out/index.html` |
| `--debug` | superpone la retícula y el recorte 3:4 de la rejilla de perfil |
| `SCALE=2 bash render.sh` | maestro 2160×2700 (Instagram recorta a 1080 de ancho) |

## Dónde se toca cada cosa

- **`posts/*.json`** — la fuente escrita a mano. Un fichero por publicación.
- **`src/_shared.css`** — **la superficie de ajuste**: retícula, escala tipográfica, temas,
  tratamiento de foto. Se escribe a mano; `build_posts.py` no la genera nunca. Para afinar
  un cartel: `open src/<id>-01.html` en una pestaña normal de Chrome —es 1:1— y edita esta
  hoja en DevTools. El Python emite estructura, no diseño.
- **`defaults.json`** — lo que no cambia: marca de contacto, aforo, lugares, ciclos.
- **`ref/`** — capturas de referencia del perfil real. Entrada, no salida.
- **`assets/retratos/`, `assets/portadas/`** — material de Drive, copiado a mano.

## El brief

`plantilla` es la única clave obligatoria de una lámina. **Todo lo demás es un bloque que
se dibuja si está y desaparece si no.** Ver `posts/_ejemplo.json`.

Cuatro plantillas: **`evento`** (una sesión), **`ciclo`** (varias fechas en una tabla),
**`recordatorio`** (nombre, fecha, hora y nada más), **`cita`** (fragmento del manifiesto).

`slides` es una lista: una lámina → una publicación 4:5; varias → carrusel, numerado
`-01`, `-02`… en el mismo orden en que se sube.

## Decisiones que conviene no deshacer sin pensarlo

- **Un carrusel no es otro formato.** Son N imágenes de 1080×1350. Una sola vía de código.
- **El tope de bloques por lámina es real.** La anatomía completa de un cartel impreso
  (lugar, ciclo, presentación, sigla, nombre, día, hora, foto, portadas, bio, aforo, web,
  QR) es un inventario de A3 que se lee a un brazo de distancia. En el feed, esa misma
  imagen se ve a ~430 pt: meter los trece bloques deja el cuerpo de texto a ~8 px reales.
  El carrusel es la válvula de escape, y el linter la obliga.
- **La fecha es la carga útil**, no una etiqueta: va en serif de display, no en sans
  versaleada como el resto de la cresta.
- **Un solo desplazamiento por cartel.** La fecha se sale de la retícula (`--desplazo`).
  El colectivo se llama Fuera de Lugar; el cartel lo hace en vez de decirlo. Tope 50 px:
  la rejilla de perfil recorta 34 px por lado y el desplazamiento debe seguir entero en la
  miniatura.
- **El acento es puntuación** —un separador, el año, la lámina activa— nunca un campo.
- **`citrine` aquí no es la `citrina` de `content/tshirts/`.** Allí la tinta es casi negra
  porque tenía que sobrevivir sobre algodón blanco. Aquí se usa la paleta ampliada de
  `skills/brand-content/SKILL.md` en su combinación cálida (Cera + Citrina + Medianoche),
  porque Instagram es pantalla, el mismo medio que el sitio.
- **El fallback de las tipografías es `monospace` a propósito.** Si Chrome no carga los
  OTF, todo sale en Courier y el fallo es imposible de pasar por alto. Un fallback
  «Georgia, serif» daría un cartel creíble pero fuera de marca, que es peor.

## Límites conocidos

- **El tratamiento de foto es CSS, no ImageMagick.** `brand-content` prescribe
  `-normalize`, que es adaptativo por imagen; `contrast()` es un multiplicador fijo y no
  puede serlo. Una foto plana sale plana: ajústala a ojo con `foto.contraste` y
  `foto.brillo` contra la hoja de contactos. A cambio, cero dependencias.
- **Las fotos de `docs/gallery/` son 1600×900.** Por eso `foto.forma` es `banda` por
  defecto (1080×608, ratio nativo, sin recorte): un recorte vertical tira medio encuadre y
  suele cortar cabezas.
- **El QR no se genera.** En Instagram apenas sirve —no se escanea la pantalla que tienes
  en la mano— y codificarlo sin dependencias son ~200 líneas. El campo existe para cuando
  estos mismos briefs alimenten un cartel impreso.
- **Los retratos de autor y las portadas están en Drive**, que ahora mismo no sirve los
  bytes en local. Cópialos a mano a `assets/`.
