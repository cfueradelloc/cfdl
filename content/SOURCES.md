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
| Eventos (`docs/eventos.html`) | `content/events/calendario-eventos.md` | `Eventos/<ciclo>/` — docs «Actividad», dosieres y `Carteles/` de cada ciclo (14.4, La Magistral, En Voz Alta, Libros del Baobab, Almíbar Off, Equinoccio Sound, Welcome Summer, Cines Casablanca, Salut Drets Acció) |
| Galería (`docs/galeria.html`) | `docs/gallery/*.jpg` | `Eventos/En Voz Alta/<autor>/Fotos/` y demás `Fotos/` de cada evento |
| Manifiesto (`docs/manifiesto.html`) | `docs/assets/docs/Manifesto_Fuera_De_Lugar.pdf`, `docs/assets/images/` | `Contenido/Manifiesto/` — traducciones (ES/CA/EN/DE/FR/PT/AST) y `Manifiesto/Fotos/` |
| Branding (logo, tipografía) | `docs/assets/logo/`, `docs/assets/fonts/` | `Branding/` — logo, favicon, fuentes |
| Traducciones del manifiesto (referencia) | `skills/brand-content/references/manifesto/` | `Contenido/Manifiesto/` |

## Cómo actualizar eventos
1. Edita `content/events/calendario-eventos.md` (la lista canónica).
2. Refleja los cambios en `docs/eventos.html` (estructura *Próximos* / *Pasados*).
3. Si añades fotos, colócalas en `docs/gallery/` y enlázalas desde `docs/galeria.html`.

## Pendiente
- El perfil de Instagram [@cfueradelloc](https://www.instagram.com/cfueradelloc/) tiene
  material (fechas, posts) que no se ha volcado aquí — requiere inicio de sesión. Ver las
  notas ⚠️ «por confirmar» en `calendario-eventos.md`.
