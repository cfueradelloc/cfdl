# Galería — curaduría y tratamiento de las fotos

Las fotos de `docs/gallery/` (1600 px, para el visor) y `docs/gallery/sm/`
(900 px, `.jpg` + `.webp`, para la retícula) **no se editan a mano**: salen de
`tratar.py` a partir de los másteres de `originales/`.

```
Drive · CFDL/Seleccion/        (selección + balance de blancos, ver SELECCION.md)
        │  copiar con el nombre web (p. ej. 14-4-sani-1.jpg)
        ▼
studio/gallery/originales/     másteres, sin tocar
        │  python3 studio/gallery/tratar.py [nombre …]
        ▼
docs/gallery/<nombre>.jpg      1600 px
docs/gallery/sm/<nombre>.jpg   900 px
docs/gallery/sm/<nombre>.webp  900 px
```

Luego, una línea en el array `IMAGES` **y** otra en el `<noscript>` de
`docs/galeria.html` (con `w` y `h` reales de la foto de 1600 px).

## Reglas de curaduría (obligatorias)

1. **Nunca una cabeza cortada.** Ni por el encuadre original (una persona
   partida por el borde, una coronilla fuera) ni por la web: la retícula
   muestra cada foto en su proporción exacta (`w`/`h` del array = los de la
   foto), sin recorte ni zoom al pasar. Si una foto tiene una cabeza cortada
   de origen, **no entra**.
2. **Sin redundancia.** De un mismo encuentro, sólo tomas que aporten un
   encuadre o un momento distinto. Dos casi iguales → queda la mejor.
3. **Calidad.** Fuera desenfoques (también el movido en la cara), las muy
   oscuras y las de luz rara que el tratamiento no salva.
4. **Nunca dos fotos del mismo encuentro juntas.** Lo garantiza el script de
   la página (ni al lado ni encima/debajo, en cualquier ancho); el encuentro
   es lo que va tras « · » en el pie (`cap`). Un pie, un encuentro: escríbelo
   siempre igual.

## Tratamiento (`tratar.py`)

Sobrio e igual para todas, para que la serie se vea homogénea y profesional:
niveles por luminancia (sin tocar el color, ganancia limitada), medios tonos
hacia una luminancia común (corrección limitada: la noche sigue siendo noche),
curva en S leve (+8 %), saturación hacia un objetivo común (limitada) y enfoque
de salida tras reducir. La receta está arriba en el script; si se ajusta, se
vuelve a pasar sobre los másteres — nunca sobre lo ya tratado.

## Cómo se comporta la galería

- Filas justificadas con 6 px de aire; cada fila ocupa el ancho exacto.
- Se ve ~60 % de la colección; el resto está en reserva. A ratos irregulares
  (1,6–3,2 s) una foto se funde en otra de la reserva **de la misma
  proporción** (±2 %) y de un encuentro distinto al de sus vecinas. La foto
  bajo el ratón no cambia; tampoco con el visor abierto, la pestaña oculta o
  movimiento reducido.
- «Barajar» (a mano, y sola cada 40 s): cada foto se va en su momento y el
  orden nuevo vuelve foto a foto — nunca todas a la vez.
- Clic: el visor, con la foto entera (1600 px), su pie y «07 / 40»; flechas,
  teclado, deslizar y Esc.

## Registro

- **2026-11-01 · Segunda curaduría** (58 → 40). Fuera, por casi iguales:
  `envozalta-angela-4`, `-angela-5`, `-pablo-2`; `magistral-juan-3`, `-juan-5`;
  `magistral-tinaut-4`; `14-4-laura-5`; `welcome-summer-2`, `-4`, `-5`, `-6`;
  `lorca-habana-1`; `manifiesto-3` (≈ `manifiesto-2` y la foto de portada).
  Fuera por **cabeza cortada**: `magistral-juan-6`, `magistral-tinaut-5`,
  `14-4-sani-2`, `banel-adama-3`. Fuera por **movida**: `14-4-laura-2`.
  Primer pase de `tratar.py` sobre las 40.
