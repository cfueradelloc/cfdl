# Portadas de libros

Se copian aquí a mano desde el Drive del colectivo (`Eventos/<ciclo>/<autor>/Docs/`).
El módulo no baja nada solo.

Se dibujan con el bloque `portadas`, que funciona en `evento`, `retrato` y `resumen`:

```json
"portadas": [
  { "src": "assets/portadas/motel-milla-noventa.jpg" },
  { "src": "assets/portadas/cuentos-madre-muerte.avif" }
]
```

Salen en fila, a 220 px de alto, con un filete del color del borde del tema. No se
recortan: si una portada es muy apaisada, ocupará más ancho que las demás.

Dos o tres como mucho — cuentan para el tope de bloques de la lámina, y una fila de
cuatro portadas a 220 px ya no se distingue en el feed.

Antes de publicar una portada, comprueba que el colectivo puede hacerlo.
