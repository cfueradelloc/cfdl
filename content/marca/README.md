# La marca — C.F.D.L.

Fuente única del logotipo. Lo que lo use lo pide aquí, para que no haya dos
versiones separándose con el tiempo.

> **Propuesta, no identidad vigente.** El sitio, las camisetas y el módulo de
> Instagram siguen usando el logotipo anterior. Aquí no hay nada conectado.

## La idea

El manifiesto impreso compone su texto como una **espiral rectangular**:
rectángulos encajados girando hacia dentro, con la vuelta interior cortada a
media altura. **No cierra nunca** — *cambiante y nunca cumplido*.

La marca es esa espiral, estilizada hasta que aguanta a 16 px. No hacía falta
inventarle un símbolo al colectivo: ya tenía uno, y está impreso. La
reproducción exacta de la hoja vive en `content/tshirts/build_designs.py`
(`svg_espiral_frame`), medida sobre el original: proporción 0.571, siete
anillos.

## Densidad en vez de variantes

Siete anillos se empastan en un favicon. En lugar de dibujar marcas distintas
para cada tamaño, se elige **cuántas vueltas** da la espiral. Es el mismo signo.

| densidad | vueltas | para |
|---|---|---|
| `fina` | 3½ | 64 px en adelante — la densidad de la hoja impresa |
| `media` | 2½ | 32–64 px, y junto a texto |
| `gruesa` | 2 | por debajo de 32 px: favicon, sellos, bordado |

## Piezas

| pieza | qué es | cuándo |
|---|---|---|
| `monograma` | la espiral en cuadrado | uso general, pie de cartel |
| `perfil` | igual, metida hacia dentro | **foto de perfil**: cabe entera en el círculo |
| `hoja` | proporción 0.571, vertical | cabeceras, papelería — es la hoja impresa |
| `linea` | signo + `C.F.D.L.` al lado | firmas, pies, cabeceras horizontales |
| `lockup` | signo sobre `C.F.D.L.` | cuando manda el eje vertical |

**`perfil` existe por una razón concreta.** Instagram recorta en círculo, y a
una espiral rectangular perder las esquinas no le sienta como un recorte: le
sienta como una avería. Con el margen de 15 unidades el cuadrado entero cabe en
el círculo inscrito (la semidiagonal de un cuadrado de lado 70 es 49,5 < 50).

## Cómo pedirlo

```python
import marca
marca.svg("perfil", fondo="ambar", tinta="negro", densidad="fina", size=1080)
marca.svg("linea",  fondo="ninguno", tinta="auto", densidad="media")
```

- **pieza** `monograma` · `perfil` · `hoja` · `linea` · `lockup`
- **fondo** `ambar` · `negro` · `blanco` · `ninguno`
- **tinta** `negro` · `blanco` · `zafiro` · `ambar` · `crema` · `auto`
- **densidad** `fina` · `media` · `gruesa`

`tinta="auto"` devuelve `currentColor`: el SVG hereda el color del texto que lo
rodea, que es lo cómodo dentro de una página que ya tiene temas.

## Combinaciones probadas

`index.html` enfrenta cada pieza con cada fondo y cada tinta que le sirve:
blanco, negro, ámbar, rosa y zafiro — solo, con las siglas al lado, apilado, y
llevándose su propio campo encima.

Pares que funcionan:

| fondo | tinta |
|---|---|
| blanco | negro · zafiro |
| negro | ámbar · blanco · crema |
| ámbar | negro |
| rosa (el de la web) | zafiro · negro |
| zafiro (banda oscura) | ámbar · crema |

## Archivos

```
marca.py           el generador — la única fuente
svg/               18 combinaciones exportadas
png/               los tamaños que hacen falta de verdad
  perfil-instagram.png  1080 · foto de perfil, a prueba de círculo
  favicon-180.png       180  · icono de aplicación
  favicon-32.png        32   · favicon, densidad gruesa
  linea-negro.png       680×200 · firma
  hoja.png              513×900 · la hoja
index.html         la hoja de casos
bocetos/           las rondas descartadas, como registro
```

`python3 marca.py` regenera SVG y hoja. `bash exportar_png.sh` rehace los PNG.

## Decisiones de dibujo

- **El arranque queda a ras de la esquina.** En la primera versión sobraba un
  rabito suelto que parecía un descuido.
- **El remate interior es el único gesto abierto** — dibuja el 45 % de su última
  recta y se detiene. Es lo que hace la hoja impresa, y es lo que significa la
  marca.
- **Centrado óptico.** Una espiral hacia dentro carga su masa a un lado; el
  dibujo se devuelve por diferencia entre su caja real y la del lienzo. Sin eso
  el avatar se ve descolgado.
- **Trazo y hueco casi iguales.** Es lo que produce la vibración de la hoja
  impresa. En `gruesa` el hueco baja un punto para que a 16 px no se cierre.
- **Uniones en inglete, remates a hueso.** Nada redondeado: es una hoja doblada,
  no un icono de aplicación.

## Rondas descartadas

`bocetos/` guarda el camino, que explica las decisiones mejor que un resumen:

1. **ronda 1** — cuadrado ámbar con siglas y doble filete. Honestamente malo:
   primitivas sueltas, sin sistema, y una barra suelta que se leía como ruido.
2. **ronda 2–3** — la C con el brazo fuera de sitio, y el **registro corrido**
   (dos planchas, una desplazada). Buena idea —el colectivo imprime— y
   funcionaba, pero se le inventaba un símbolo al colectivo teniendo uno ya.
3. **ronda 4–5** — la espiral. Dos hallazgos: siete anillos se empastan (de ahí
   la densidad variable), y una vuelta corrida SOBRE la espiral era ruido —
   confirmó que una idea a la vez.

## Colores

| | hex | qué es |
|---|---|---|
| ámbar | `#ffb923` | el del logotipo y el del manifiesto impreso |
| negro | `#171513` | la tinta impresa, negro cálido |
| zafiro | `#332f8a` | la tinta de la web |
| crema | `#fff4d6` | sobre negro, cuando el ámbar pesa demasiado |

Ojo: el `#e9ad51` de `content/tshirts/` es otra cosa — la aproximación al papel
Colorplan Citrine, un punto más apagada.
