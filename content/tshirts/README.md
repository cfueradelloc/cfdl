# Camisetas — C.F.D.L. (v3)

**102 propuestas de camiseta**, cada una como PNG individual 2400×1600 (mockup sobre una camiseta
blanca real). **Impresión compacta y centrada en el cuello** (~⅓ del pecho, márgenes amplios,
nunca pegada a las costuras; centro de impresión = 50.5%, el cuello medido de la foto),
tipografía de marca real, texto **literal del manifiesto**, `@cfueradelloc · cfdl.site` en todas,
**sin logotipo**, em dash (—) nunca guion.

Paleta de la **web dominante** (zafiro `#332f8a` + amarillo `#fde700`); **el rosa caramelo
`#f8ccce` aparece como tercera nota** en ~12 diseños (sellos con fondo rosa, barras de censura
rosas, tinta rosa, acentos). Citrina (ámbar/negro) y amatista para variedad. Sin negro
(no se encontró una foto de camiseta negra lisa de calidad; el blanco es la base, como acordado).

## Familias

- **Texto puro (14)** — solo las más ingeniosas: marca blanca, fuera de lugar, suicidio creativo,
  garganta sin fondo, lo atópico, náufrago, atopia, la creación como trastorno, la obra mejora si
  está fuera de lugar…
- **Antítesis (13)** — término tachado → sustituto (la síntesis→la disgregación, la cura→la
  prótesis, la empatía→la opacidad, el individuo→la colectividad, la rehabilitación→la fractura…).
- **Texto + gráfico (16)** — SVG en paleta + cita: brújula sin imán, anillos, fractura, moho,
  maleza, espiral, guion largo.
- **Tipografía concreta (6)** — la forma dice el sentido: *garganta* cayendo al vacío, *exilio*
  descendiendo, *disgregación/ruinas/fractura* fragmentándose, *extenuación* estirada, *maleza*
  enredada en zarcillos.
- **Sellos / cuños circulares (8)** — sello con texto en el aro + palabra central (fuera de lugar,
  marca blanca, atopia, aduanas, moho, suicidio creativo, C·F·D·L); varios con fondo **rosa**.
- **Desplazados (5)** — la palabra «fuera de lugar» literalmente descolocada/partida.
- **Redacción (5)** — línea del manifiesto con barras de censura (rosas o zafiro), visible solo
  el fragmento clave.
- **C.F.D.L. tipográfico (9)** — solo las siglas (rejilla, línea, serif, vertical).
- **Manifiesto — ideas gráficas (7)**: acordeón plegado, banda de sombra dentada (amarilla),
  hoja con esquina doblada, **índice 01–10** (tabla de contenidos del manifiesto), colofón
  («Manifiesto cambiante y nunca cumplido · primera edición · octubre 2023»), sello de edición,
  página densa. Solo **2 fotos** del manifiesto (el abanico amarillo, en color y duotono zafiro).
- **Bloques del manifiesto (6)**, **verbos (2)**.
- **Cerca del corazón (8)** — mini-estampas en el pecho izquierdo (mini ·C·F·D·L·, brújula, sello,
  punto amarillo, *marca blanca*, *atópico*).

## Reproducir
`python3 build_designs.py` (genera `src/NN-*.html`) y `bash render.sh` (PNG 2×, 2400×1600,
Chrome headless en paralelo, perfiles aislados). `prep_photos.py` trata las fotos del manifiesto.
