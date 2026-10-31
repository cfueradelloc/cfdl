# Vista previa social (og:image / twitter:image)

`social.html` compone la imagen de 1200×630 que muestran WhatsApp, Instagram,
Facebook, X, LinkedIn o Slack al compartir cfdl.site: la foto del manifiesto
(`docs/assets/images/portada.jpg`, como en la portada), el velo, la «línea» de
la marca en ámbar y «Colectivo Fuera de Lugar · Col·lectiu Fora de Lloc».

Para regenerarla (desde la raíz del repositorio):

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --hide-scrollbars --allow-file-access-from-files --force-device-scale-factor=1 \
  --window-size=1200,630 --virtual-time-budget=3000 \
  --screenshot=/tmp/social.png "file://$PWD/studio/social/social.html"
python3 -c "from PIL import Image; Image.open('/tmp/social.png').convert('RGB').save('docs/assets/images/social-cfdl.jpg', quality=88, optimize=True, progressive=True)"
```

**Si cambia la imagen, cambia también su nombre** (y el `og:image` /
`twitter:image` de todas las páginas): las apps guardan la vista previa en
caché por la dirección de la imagen, y con el mismo nombre seguirían
enseñando la anterior.
