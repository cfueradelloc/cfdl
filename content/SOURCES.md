# Fuentes — de dónde sale el contenido del sitio

Mapa entre cada sección del sitio y su material en bruto, que vive en el Google Drive del
colectivo (carpeta sincronizada localmente). **Trabajar siempre sobre la copia local**, no
vía el conector MCP (ver `CLAUDE.md`).

Raíz del Drive:

```
/Users/mduranfrigola/Library/CloudStorage/GoogleDrive-miquelduranfrigola@gmail.com/My Drive/Documents/Writing/CFDL
```

| Sección del sitio | Archivo(s) en el repo | Material original en el Drive |
|---|---|---|
| Eventos (`docs/eventos.html`) | `content/events/calendario-eventos.md` | `Eventos/<ciclo>/` — docs «Actividad», dosieres y `Carteles/` de cada ciclo (14.4, La Magistral, En Voz Alta, Libros del Baobab, Almíbar Off, Equinoccio Sound, Welcome Summer, Cines Casablanca, Salut Drets Acció). `Tragaluz/` sólo guarda el dossier de prensa de Vicente Navarro (sello El Tragaluz): archivo, no evento |
| Galería (`docs/galeria.html`) | `docs/gallery/*.jpg` | `Eventos/En Voz Alta/<autor>/Fotos/` y demás `Fotos/` de cada evento |
| Manifiesto (`docs/manifiesto.html`) | `docs/assets/docs/Manifesto_Fuera_De_Lugar.pdf`, `docs/assets/images/` | `Contenido/Manifiesto/` — traducciones (ES/CA/EN/DE/FR/PT/AST) y `Manifiesto/Fotos/` |
| Branding (logo, tipografía) | `docs/assets/logo/`, `docs/assets/fonts/` | `Branding/` — logo, favicon, fuentes |
| Traducciones del manifiesto (referencia) | `skills/brand-content/references/manifesto/` | `Contenido/Manifiesto/` |
| Archivo de Instagram | — (sólo en el Drive) | `Instagram/` — copia de lo publicado en @cfueradelloc, con `index.md`; la escribe la skill `instagram-archive` |
| Instagram (@cfueradelloc) | `content/instagram/posts/*.json` → `content/instagram/out/*.png` | `Eventos/<ciclo>/Carteles/` — carteles anteriores; `Eventos/<ciclo>/<autor>/` — retratos y portadas |

## Cómo actualizar eventos
1. Edita `content/events/calendario-eventos.md` (la lista canónica).
2. Refleja los cambios en `docs/eventos.html` (estructura *Próximos* / *Pasados*).
3. Si añades fotos, colócalas en `docs/gallery/` y enlázalas desde `docs/galeria.html`.

## Cómo anunciar en Instagram
Las imágenes se generan en `content/instagram/` (ver su README y la skill `instagram-post`).
El calendario manda: primero la entrada en `calendario-eventos.md`, después el brief.

## Archivo de Instagram
Lo publicado en [@cfueradelloc](https://www.instagram.com/cfueradelloc/) se descarga en
`Instagram/` del Drive con la skill `instagram-archive`
(`skills/instagram-archive/scripts/archive.sh chrome`). Cotejar su `index.md` con
`calendario-eventos.md` y resolver ahí las notas ⚠️ «por confirmar».

Mientras Instagram bloquee la descarga automática, el archivo vigente son las **capturas**
(`Instagram/Screenshot 2026-10-03 …png`, 34 publicaciones de jun 2025 a oct 2026); de ahí
sale la revisión del calendario del 3 oct 2026. Las plantillas de
`content/instagram/` se dedujeron de los carteles del Drive; las publicaciones reales del
archivo sirven para afinarlas.
