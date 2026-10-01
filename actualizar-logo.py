#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Incrusta el logo del Centro de Padres dentro de index.html (auto-contenido).

Qué hace, en orden:
  1. Recorta el margen blanco del logo original.
  2. Lo comprime con una paleta de 256 colores (el logo es plano: se ve igual y pesa mucho menos).
  3. Genera un favicon cuadrado de 64x64.
  4. Sustituye el logo y el favicon dentro de index.html como data URI base64.

Se puede volver a ejecutar siempre que cambie el logo: es idempotente
(reemplaza el data URI anterior, no lo acumula).

Uso:
    python3 actualizar-logo.py ruta/al/logo.png [ruta/index.html]
Por defecto usa ./logo-original.png e ./index.html
"""

import base64
import io
import re
import sys

from PIL import Image

ANCHO_WEB = 460        # ancho máximo del logo para la web (px reales del PNG)
COLORES = 256          # paleta: el logo es plano, no necesita más
LADO_FAVICON = 64


def recortar_margen(im, tolerancia=246):
    """Quita el marco blanco que rodea al logo."""
    rgb = im.convert("RGB")
    ancho, alto = rgb.size
    px = rgb.load()

    def vacia(x, y):
        r, g, b = px[x, y]
        return r >= tolerancia and g >= tolerancia and b >= tolerancia

    arriba = 0
    while arriba < alto - 1 and all(vacia(x, arriba) for x in range(ancho)):
        arriba += 1
    abajo = alto - 1
    while abajo > arriba and all(vacia(x, abajo) for x in range(ancho)):
        abajo -= 1
    izquierda = 0
    while izquierda < ancho - 1 and all(vacia(izquierda, y) for y in range(alto)):
        izquierda += 1
    derecha = ancho - 1
    while derecha > izquierda and all(vacia(derecha, y) for y in range(alto)):
        derecha -= 1

    return im.crop((izquierda, arriba, derecha + 1, abajo + 1))


def b64_png(im):
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii"), buf.tell()


def main():
    origen = sys.argv[1] if len(sys.argv) > 1 else "logo-original.png"
    destino = sys.argv[2] if len(sys.argv) > 2 else "index.html"

    # --- 1 y 2: logo para la web -----------------------------------------
    original = Image.open(origen)
    recortado = recortar_margen(original).convert("RGB")
    ancho = min(ANCHO_WEB, recortado.size[0])
    alto = round(recortado.size[1] * ancho / recortado.size[0])
    web = recortado.resize((ancho, alto), Image.LANCZOS).quantize(
        colors=COLORES, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    web.save("logo-web.png", "PNG", optimize=True)
    b64_logo, peso_logo = b64_png(web)
    print("logo: %sx%s -> %sx%s, %.1f KB (base64 %.1f KB)"
          % (original.size[0], original.size[1], ancho, alto,
             peso_logo / 1024, len(b64_logo) / 1024))

    # --- 3: favicon cuadrado ---------------------------------------------
    lado = max(recortado.size)
    lienzo = Image.new("RGB", (lado, lado), (255, 255, 255))
    lienzo.paste(recortado, ((lado - recortado.size[0]) // 2,
                             (lado - recortado.size[1]) // 2))
    favicon = lienzo.resize((LADO_FAVICON, LADO_FAVICON), Image.LANCZOS)
    favicon.save("favicon.png", "PNG", optimize=True)
    b64_fav, peso_fav = b64_png(favicon)
    print("favicon: %dx%d, %.1f KB" % (LADO_FAVICON, LADO_FAVICON, peso_fav / 1024))

    # --- 4: incrustar en el HTML -----------------------------------------
    html = open(destino, encoding="utf-8").read()
    cambios = 0

    # 4a. iconos del navegador
    nuevo_iconos = (
        '<link rel="icon" type="image/png" href="data:image/png;base64,%s">\n'
        '<link rel="apple-touch-icon" href="data:image/png;base64,%s">' % (b64_fav, b64_fav)
    )
    html, n = re.subn(r'<link rel="icon".*?</?\s*>?\n?', nuevo_iconos + "\n", html,
                      count=1, flags=re.S)
    cambios += n
    if n == 0:
        raise SystemExit("No se encontró la línea del favicon en %s" % destino)

    # 4b. el bloque <img> del logo
    nuevo_img = ('<img class="logo-img" src="data:image/png;base64,%s" '
                 'width="%d" height="%d" alt="Centro de Padres Colegio Los Alerces">'
                 % (b64_logo, ancho, alto))
    html, n = re.subn(r'<img class="logo-img"[^>]*>', nuevo_img, html, count=1)
    cambios += n
    if n == 0:
        raise SystemExit("No se encontró <img class=\"logo-img\"> en %s" % destino)

    open(destino, "w", encoding="utf-8").write(html)
    print("index.html actualizado (%d sustituciones)." % cambios)


if __name__ == "__main__":
    main()