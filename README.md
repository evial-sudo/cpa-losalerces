# cpa-losalerces

Página pública con los datos de transferencia bancaria del **Centro de Padres Colegio Los Alerces**.

| | |
|---|---|
| **Dirección principal** | https://cpa-losalerces.netlify.app/ |
| Dirección de respaldo | https://evial-sudo.github.io/cpa-losalerces/ |
| Publicado con | Netlify (principal) y GitHub Pages (respaldo), ambos gratis, permanentes y HTTPS |
| Archivo único | `index.html` (HTML + CSS + JS + logo y favicon incrustados, sin dependencias ni CDN) |

Las dos direcciones sirven la **misma página**. La principal (Netlify) es la que se comparte y la que
apunta el código QR; la de respaldo (GitHub Pages) se actualiza sola al subir cambios al repositorio.

> Importante: el repositorio usa **una sola rama, `gh-pages`**. No crees ni edites otra rama: si
> editas una copia en otra rama, el sitio no se actualizará y podrías confundir versiones.

## Archivos

| Archivo | Para qué sirve |
|---|---|
| `index.html` | El sitio completo. Es el único archivo que se publica. |
| `logo-original.png` | Logo del Centro de Padres tal como se recibió. |
| `actualizar-logo.py` | Vuelve a incrustar el logo dentro de `index.html`. |
| `generar-qr.py` | Genera los PNG del código QR. |
| `verificar-qr.py` | Comprueba que los QR apunten a la URL correcta. |
| `verificar-pagina.py` | Revisa `index.html` antes de publicar (estructura, logo y que cada dato visible coincida con lo que se copia). |
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

Antes de publicar, conviene revisar que todo quedó bien:

```bash
python3 verificar-pagina.py
```

### 1. Editar (desde el navegador, lo más simple)

1. Abre https://github.com/evial-sudo/cpa-losalerces/blob/gh-pages/index.html
2. Haz clic en el lápiz (Edit this file), aplica los cambios y confirma con **Commit changes**.
3. El respaldo de GitHub Pages se actualiza solo en 1–2 minutos.

### 2. Publicar en la dirección principal (Netlify)

Netlify **no** está enlazado al repositorio, así que un cambio en GitHub no llega solo a
`cpa-losalerces.netlify.app`. Hay dos formas de publicarlo:

- **Manual (sin instalar nada):** entra a https://app.netlify.com/projects/cpa-losalerces,
  abre la pestaña **Deploys** y arrastra la carpeta que contiene `index.html` al recuadro de
  despliegue ("drag and drop"). Netlify publica de inmediato.
- **Automática (recomendada, se hace una sola vez):** en Netlify, entra a
  **Project configuration → Build & deploy → Link repository** y elige
  `evial-sudo/cpa-losalerces`, rama `gh-pages`, directorio de publicación `/` (la raíz).
  Desde ahí, cada cambio en `index.html` se publica solo.

### 3. Verificar después de publicar

- La página abre en el celular sin iniciar sesión y sin avisos de "sitio no seguro".
- El botón **"Copiar todos los datos"** muestra "Copiado" y al pegar aparecen las 6 líneas.
- Cada fila copia solo su valor y muestra "Copiado".
- Abre la página con `Ctrl+Shift+R` (o borrando caché en el celular) para no ver la versión antigua.

## Cómo cambiar el logo

1. Guarda el logo nuevo como `logo-original.png` (reemplazando el actual).
2. Ejecuta:

```bash
pip3 install pillow
python3 actualizar-logo.py logo-original.png index.html
```

El script recorta el margen blanco, comprime la imagen, la incrusta en `index.html` junto con
el favicon y verifica que el HTML no quede roto. También deja `logo-web.png` y `favicon.png`
por si los necesitas sueltos.

3. Publica el cambio (pasos 1 y 2 de arriba).

El logo se muestra dentro de un recuadro blanco para que se vea bien también en modo oscuro.

## Código QR

El QR apunta a `https://cpa-losalerces.netlify.app/` (nivel de corrección de errores M).
Se puede volver a generar con:

```bash
pip3 install qrcode pillow
python3 generar-qr.py
python3 verificar-qr.py   # confirma que el QR apunta a la URL correcta
```

**Si cambia la dirección del sitio, hay que regenerar el QR.**