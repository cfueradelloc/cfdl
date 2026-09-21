# Logotipos ajenos

Lugar, coproductores, quien financia. Se copian aquí a mano; el módulo no baja
nada de Drive ni de internet.

`_ejemplo-a.svg` y `_ejemplo-b.svg` son marcas inventadas, sólo para que
`ejemplos/ej-10-logos.json` tenga algo que dibujar. **No son el logotipo de
nadie**: sustitúyelos por los reales antes de publicar.

## Cómo entran en el cartel

```json
"logos_cred": "con",
"logos_trat": "tinta",
"logos_alto": 52,
"logos": [ { "src": "assets/logos/perecquiana.svg", "alt": "La Perecquiana" } ]
```

`logos_trat` decide cómo se tratan:

| valor | qué hace |
|---|---|
| `tinta` *(por defecto)* | a sólido en el color del texto — negro sobre claro, blanco sobre oscuro |
| `blanco` | a sólido blanco, siempre |
| `gris` | escala de grises, conservando el medio tono |
| `color` | tal cual vino |

**`tinta` es el valor por defecto a propósito.** Un cartel a dos tintas con un
rectángulo corporativo a todo color encima deja de ser un cartel del colectivo.
Si alguien exige su color de marca exacto por contrato, existe `color`; si no,
déjalo en tinta.

Prefiere **SVG**: escala sin pixelar y el filtro de tinta lo deja limpio. Un PNG
con fondo blanco opaco se verá como un recuadro blanco — recórtalo con
transparencia antes.

## La marca del propio colectivo no se trata como un logo ajeno

`cfdl-logo-original.jpeg` (1600×1600, bajado del Drive) es el original y se guarda aquí
como referencia, pero **no se enlaza desde ningún cartel**. La marca se redibuja en SVG
desde `build_posts.py` (`svg_marca`): el cuadrado ámbar `#ffb923`, «C.F. / D.L.» en
FuturaStd y el doble filete cuyas esquinas no cierran — ese desajuste es del diseño
original, no un error.

Redibujarla en vez de enlazar el JPEG gana tres cosas: no pixela a ningún tamaño, no
arrastra el fondo blanco del JPEG, y admite una versión a una tinta (`logo-mono`) para
cuando el cartel no acepta un cuadrado de color.

Se pide desde el brief con `"marca_cfdl": "logo"`, `"logo-mono"`, `"logo+sigla"`…
