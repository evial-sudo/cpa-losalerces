# cpa-losalerces

Página pública con los datos de transferencia bancaria del **Centro de Padres Colegio Los Alerces**.

- **Sitio publicado:** https://evial-sudo.github.io/cpa-losalerces/
- **Publicado con:** GitHub Pages (gratis, permanente, HTTPS).
- **Archivo único:** `index.html` (HTML + CSS + JS + logo y favicon incrustados, sin dependencias ni CDN).

> Importante: este repositorio usa **una sola rama, `gh-pages`**. GitHub Pages publica
> desde esa rama. No crees ni edites otra rama: si editas una copia en otra rama, el sitio
> no se actualizará y podrías confundir versiones.

## Archivos

| Archivo | Para qué sirve |
|---|---|
| `index.html` | El sitio completo. Es el único archivo que se publica. |
| `logo-original.png` | Logo del Centro de Padres tal como se recibió. |
| `actualizar-logo.py` | Vuelve a incrustar el logo dentro de `index.html`. |
| `generar-qr.py` | Genera los PNG del código QR. |
| `verificar-qr.py` | Comprueba que los QR apunten a la URL correcta. |
| `qr-cpa-losalerces.png` | QR de alta resolución (1640×1640 px, nivel M). |
| `qr-cpa-losalerces-poster.png` | QR con encabezado, para imprimir y pegar. |

## Cómo actualizar la página si cambian los datos

Edita `index.html` y cambia **dos veces** cada valor: una en el texto visible y otra en el
atributo `data-value` (ese es el que se copia al portapapeles). Si los dos no coinciden,
se copiará el dato antiguo.

Ejemplo de una fila:

```html
<button class="row" type="button" data-field="N° de cuenta" data-value="13543750">
  <span class="field">
    <span class="label">N° de cuenta</span>
    <span class="value">13543750</span>
  </span>
  <span class="chip" aria-hidden="true">Copiar</span>
</button>
```

- El bloque que copia el botón **"Copiar todos los datos"** se arma solo, con los atributos
  `data-field` y `data-value` de cada fila, en el orden en que aparecen. No hay nada más que editar.
- Para **agregar** un dato: duplica una fila completa y cambia `data-field`, `data-value` y el texto visible.
- Para **quitar** un dato: borra la fila completa.
- No cambies `class="row"` ni los atributos `data-field` / `data-value`.

### Publicar el cambio (opción simple, desde el navegador)

1. Abre https://github.com/evial-sudo/cpa-losalerces/blob/gh-pages/index.html
2. Haz clic en el lápiz (Edit this file), aplica los cambios y confirma con **Commit changes**.
3. Espera 1–2 minutos y refresca https://evial-sudo.github.io/cpa-losalerces/

### Publicar el cambio (por Git)

```bash
git clone https://github.com/evial-sudo/cpa-losalerces.git
cd cpa-losalerces
# edita index.html
git commit -am "Actualiza datos de transferencia"
git push origin gh-pages
```

### Verificar después de publicar

- La página abre en el celular sin iniciar sesión y sin avisos de "sitio no seguro".
- El botón **"Copiar todos los datos"** muestra "Copiado" y al pegar aparecen las 6 líneas.
- Cada fila copia solo su valor y muestra "Copiado".

## Cómo cambiar el logo

1. Guarda el logo nuevo como `logo-original.png` (reemplazando el actual).
2. Ejecuta:

```bash
pip3 install pillow
python3 actualizar-logo.py logo-original.png index.html
```

El script recorta el margen blanco, comprime la imagen y la incrusta en `index.html`
junto con el favicon. También deja `logo-web.png` y `favicon.png` por si los necesitas sueltos.
3. Publica el cambio (commit y push a `gh-pages`).

El logo se muestra dentro de un recuadro blanco para que se vea bien también en modo oscuro.

## Código QR

El QR apunta a `https://evial-sudo.github.io/cpa-losalerces/` (nivel de corrección de errores M).
Se puede volver a generar con:

```bash
pip3 install qrcode pillow
python3 generar-qr.py
python3 verificar-qr.py   # confirma que el QR apunta a la URL correcta
```

**Si cambia la URL del sitio, hay que regenerar el QR.**