# La marca — C.F.D.L.

Fuente única del logotipo. Lo que lo use lo pide aquí, para que no haya dos
versiones separándose con el tiempo.

> **Propuesta, no identidad vigente.** El sitio, las camisetas y el módulo de
> Instagram siguen usando el logotipo anterior. Aquí no hay nada conectado.

## La idea

El colectivo **imprime**. Un *registro corrido* —dos planchas, y una que se
desplaza— es literalmente algo fuera de lugar. Nace del medio en vez de
imponerse desde fuera, y del mismo dibujo salen la versión a dos tintas y la de
una, sin dibujar dos veces.

Es lo que le faltaba a la marca anterior: un mecanismo. Allí había un cuadrado,
un doble filete, unas siglas y una esquina que no cerraba — cuatro ideas
conviviendo. Aquí hay una, aplicada al monograma y a las letras.

## Dos piezas, porque un dibujo no hace dos trabajos

| pieza | para qué | límite |
|---|---|---|
| `monograma` | la foto de perfil (que recorta en círculo), el favicon, el pie de un cartel | aguanta a **16 px**: no hay letra que leer |
| `lockup` | donde hay sitio: cabeceras, cartelería, papelería | **se empasta por debajo de 48 px** |
| `linea` | firmas y pies en horizontal | monograma + siglas |

Eso es justo lo que rompía el logotipo anterior: se le pedían los dos trabajos
a la vez, y el filete era lo primero que moría.

## Tres modos

| modo | qué hace | cuándo |
|---|---|---|
| `duo` | las dos planchas, la de atrás corrida | por defecto, donde haya dos tintas |
| `mono` | la plancha corrida queda en contorno | una sola tinta, a tamaño medio o grande |
| `plano` | sin corrimiento | tamaños diminutos, sellos, bordados, grabado |

`plano` no es una versión pobre: por debajo de ~20 px el corrimiento se empasta
y la marca se lee mejor sin él.

## Cómo pedirlo

```python
import marca
marca.svg("monograma", fondo="ambar", tinta="negro", modo="duo", size=96)
marca.svg("lockup", fondo="ninguno", tinta="auto")   # hereda currentColor
```

- **pieza** `monograma` · `lockup` · `linea`
- **fondo** `ambar` · `negro` · `blanco` · `ninguno`
- **tinta** `negro` · `blanco` · `zafiro` · `ambar` · `crema` · `auto`
- **modo** `duo` · `mono` · `plano`

`tinta="auto"` devuelve `currentColor`: el SVG hereda el color del texto que lo
rodea, que es lo cómodo dentro de una página que ya tiene temas.

## Archivos

```
marca.py          el generador — la única fuente
svg/              17 combinaciones exportadas
png/              los tamaños que hacen falta de verdad
  perfil-instagram.png  1080 · la foto de perfil
  favicon-180.png       180  · icono de aplicación
  favicon-32.png        32   · favicon, en modo plano
index.html        hoja de muestras: cada pieza sobre cada fondo, a cada tamaño
bocetos/          las rondas descartadas, como registro
```

`python3 marca.py` regenera SVG y hoja. `bash exportar_png.sh` rehace los PNG.

## Decisiones de dibujo

- **La boca se corta en vertical**, sobre el eje, no perpendicular al arco. Es
  lo que hace que una marca geométrica parezca dibujada y no recortada.
- **Todo cabe dentro del círculo inscrito** en el cuadrado, así que el recorte
  circular de Instagram no se come nada.
- **Centrado óptico**: con la plancha de atrás corrida, la masa se va
  abajo-derecha; el grupo se devuelve medio corrimiento en diagonal para que el
  conjunto quede centrado. Sin eso, el avatar se ve descolgado.
- **El fantasma cambia de color según el fondo** — ámbar hondo sobre ámbar,
  crema sobre negro, ámbar sobre claro. Un único valor fijo desaparecía sobre
  el campo ámbar.
- **Los radios y el grosor salen de un sistema** (centro 50, R 36, r 17,
  corrimiento 8), no de ajustar a ojo cada versión.

## Colores

| | hex | qué es |
|---|---|---|
| ámbar | `#ffb923` | el del logotipo y el del manifiesto impreso |
| ámbar hondo | `#c07d00` | la plancha de atrás sobre campo ámbar |
| negro | `#171513` | la tinta impresa, negro cálido |
| zafiro | `#332f8a` | la tinta de la web |
| crema | `#fff4d6` | la plancha de atrás sobre negro |

Ojo: el `#e9ad51` de `content/tshirts/` es otra cosa — la aproximación al papel
Colorplan Citrine, un punto más apagada.
