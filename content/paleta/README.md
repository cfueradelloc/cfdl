# `content/paleta/` — una sola paleta

**Propuesta.** El sitio, Instagram, las camisetas y la marca siguen con lo suyo:
aquí no se cablea nada. Lo que hay que mirar está en
[`index.html`](index.html) — y esa página está pintada con la propia paleta, que
es la única prueba que vale.

## El problema

El colectivo arrastraba **dos paletas que no se hablaban**. La rosa —Candy Pink,
Zafiro, Factory Yellow— es la identidad publicada en `cfdl.site`; la citrina
—Niebla, Cera, Citrina, Medianoche— vive en `brand-content` como «alternativa».
Instagram implementaba las dos (`--pink` / `--citrine`), las camisetas una
tercera variante del citrino, y la marca nueva ámbar sobre zafiro. Cuatro
superficies, tres respuestas a la misma pregunta.

## Lo que resultó al medirlo

- **Ámbar y zafiro no se pelean.** Están a 138° de matiz: el complementario
  exacto del ámbar sería azul puro (h 260°), y el zafiro está en h 301°,
  violáceo. Eso es un **complementario partido**, de los esquemas más sólidos que
  hay. Contrastan 6,38:1.
- **Lo que fallaba es que nunca habían compartido suelo.** La paleta rosa
  aterrizaba en Candy Pink (h 17°) y la citrina en Niebla (h 241°).
- **El rosa era el escalón que faltaba.** Del zafiro al rosa hay 76°; del rosa al
  ámbar, 63°. Cae casi en medio del salto de 138°.
- **Sobraban dos duplicados, no un color.** Factory Yellow contra ámbar: 17° de
  matiz y **1,36:1** de contraste, indistinguibles en valor. Zafiro contra
  Medianoche: 45°, dos notas frías que no pueden mandar a la vez.
- **Las camisetas ya habían llegado al papel cálido por su cuenta**:
  `#f1ece0` metido a pelo en 413 sitios, sin token y sin nombre, a ΔE 3,7 del
  `papel` propuesto. Esto no inventa el suelo; le pone nombre al que ya se usaba.

## La paleta — 13 tonos en tres grupos

### seis neutros · la rampa

| token | hex | L\* | C\* | h° | papel |
|---|---|---|---|---|---|
| `papel` | `#fdf5eb` | 96.9 | 5.8 | 80 | fondo de página |
| `hueso` | `#f1e7db` | 92.1 | 7.2 | 79 | superficie levantada |
| `filete` | `#e0d6ca` | 86.1 | 7.3 | 79 | borde, separador |
| `ceniza` | `#a89f96` | 66.0 | 6.1 | 74 | inactivo, rejilla |
| `humo` | `#6a625a` | 42.1 | 5.9 | 74 | texto secundario |
| `tinta` | `#171513` | 6.9 | 1.6 | 73 | texto principal |

**Son seis de trece a propósito.** El primer reparto tenía siete cromáticos y
tres neutros, que es al revés de como se construye un sistema: entre L\*97 y
L\*42 había **55 puntos sin un solo tono**, justo donde viven los bordes, los
separadores y los estados. Sin ellos hay que tirar de color para todo, y una
ficha de evento grita cuando debería susurrar.

Van en el **matiz del ámbar a croma 6–7**: a ese croma no se leen como otro
color cálido, se leen como grises — pero grises del mismo papel, no el gris frío
de fábrica, que sobre un fondo cálido se ve azulado y sucio.

### cinco colores

| token | hex | L\* | h° | papel |
|---|---|---|---|---|
| `ámbar` | `#ffb923` | 79.7 | 80 | el colectivo — campo, marca, acento |
| `zafiro` | `#332f8a` | 25.5 | 301 | el colectivo — banda oscura |
| `rosa` | `#f8ccce` | 85.8 | 17 | el puente, y banda de ciclo clara |
| `moho` | `#1b5033` | 29.9 | 155 | banda de ciclo |
| `náufrago` | `#004d5f` | 29.7 | 231 | banda de ciclo |

**Cinco y no tres**, porque hay tres ciclos y con tres cromáticos uno tendría que
quedarse el ámbar, que es del colectivo. No se añaden para repartir la rueda: un
sistema de marca no es un gráfico, y el sitio no tiene ni un formulario, así que
colores semánticos no hacen falta.

Los dos nuevos van **oscuros y apagados**. El candidato matemáticamente correcto
para el verde —L\*80, croma 45— sale `#83d99b`: neón, tecnológico, lo contrario
de *moho, maleza, ruinas*. A L\*30 con croma 28 lee como tinta de imprenta.
Y `náufrago` **no está en h256**, que es donde vivía Medianoche a 45° del zafiro:
empujado a h231 quedan 71° al zafiro y 76° al moho.

### dos para encima de lo oscuro

`cera` `#fff4d6` · `lavanda` `#bbabd5`. Sobre papel son invisibles, y está bien
que lo sean.

## Cómo pedirla

```python
import paleta, color
paleta.HEX["ámbar"]                     # '#ffb923'
color.lch("#ffb923")                    # (79.7, 78.1, 80.4)
color.contraste("#171513", "#ffb923")   # 10.59
color.nivel(10.59)                      # 'AAA'
color.desde_lch(96.9, 6, 80)            # '#fdf5eb'
```

```
python3 paleta.py              lista los trece tonos
python3 paleta.py --verificar  comprueba los contrastes, sale con error si falla
python3 hoja.py                rehace index.html
python3 color.py <hex> [<hex>] mide un color, o un par
```

`--verificar` recorre las **31 parejas** que el sistema necesita: 27 de texto a
4,5:1 y 4 de interfaz a 3:1. Sale con código distinto de cero si alguna cae, para
que la paleta no se degrade en silencio — la misma disciplina de
`content/instagram/render.sh`.

### Dos avisos que salen de la medición

- **El ámbar no puede ser el anillo de foco** sobre fondo claro: da 1,59:1 sobre
  papel y desaparece. El foco va en zafiro. El ámbar es el color de la marca, no
  el de la interfaz.
- **`ceniza` no llega al 3:1** de la norma para lo que no es texto (2,41:1). No
  es un descuido: su trabajo son estados inactivos y filetes, y la norma exime
  expresamente los componentes inactivos y lo decorativo. Bajarla a L\*54 para
  que cumpliera la dejaba a 1,54:1 de `humo` y las dos se confundían. Un borde
  que *sí* tiene que verse usa `humo`.

## Lo que se retira

`#fde700` Factory Yellow · `#1a2e3d` Medianoche · `#4a6880` Pizarra ·
`#e8edf0` Niebla · `#ffd25a` Sol · `#6b4200` Resina · `#7d9e92` Salvia ·
`#c07d00` Azafrán · `#857c75` Smoke · `#c8b8d8` lavender-pink ·
`#e9ad51` el citrino de camisetas. Cada uno con su razón numérica en
[`index.html`](index.html).

## El coste de cablear, medido

No se ha cableado nada, pero conviene tener el número antes de decidirlo:

| cambiar… | toca |
|---|---|
| un token del sitio | **11 sitios de definición** + 5 `<meta name="theme-color">` + el favicon (SVG, PNG y PDF) + dos `:hover` sueltos `#e8b8c8` |
| `#332f8a` | además: THEMES de Instagram, 3 de las 5 paletas de camisetas → **406 archivos regenerados**, seis `.py` de marca, 28 SVG |
| `#ffb923` o `#171513` | Instagram + marca + camisetas, y **cero archivos bajo `docs/`** |

Los seis tokens del sitio están repetidos literalmente en once sitios: `base.css`,
siete `docs/output/*.html`, el `_shared.css` de Instagram, la plantilla de
`algorithmic-art` y la prosa de dos skills. Y hay **159 arrays RGB en JavaScript**
(`[51,47,138]`, `[248,204,206]`…) en las piezas generativas que ninguna búsqueda
de hexadecimales encuentra.

El orden sensato para cablear sería **Instagram primero** — es donde más duele
tener dos temas y no se ha publicado nada todavía.

### Una corrección pendiente en la documentación

`skills/brand-content/references/colorplan.md:83` afirma que la paleta ámbar «no
está en uso». Es falso: hay unas **tres mil apariciones** de `#ffb923` y
`#171513` entre la marca, Instagram y las camisetas. Es la frase más peligrosa
del repositorio para esta decisión.

### Dos fallos anteriores, localizados y sin tocar

Aparecieron al inventariar el repositorio; no los provoca este trabajo.

- `docs/output/garganta.html:346` tiene un literal roto — `'#14081 9'`, con un
  espacio dentro del hexadecimal.
- `--rule` se declara **sólo** en el bloque oscuro de `base.css` y tiene nueve
  consumidores; en modo claro no hay valor de reserva.
