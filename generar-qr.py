#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el código QR (PNG de alta resolución, corrección de errores nivel M)
que apunta a la página pública con los datos de transferencia del
Centro de Padres Colegio Los Alerces.

Uso:
    pip3 install qrcode pillow
    python3 generar-qr.py

Salidas:
    qr-cpa-losalerces.png         -> QR puro, listo para escanear o imprimir
    qr-cpa-losalerces-poster.png  -> QR con encabezado y URL para imprimir/pegar
"""

from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_M

URL = "https://evial-sudo.github.io/cpa-losalerces/"
BOSQUE = (20, 83, 45)        # verde bosque
BLANCO = (255, 255, 255)
GRIS = (76, 99, 87)

MIN_PX = 1000                # tamaño mínimo exigido
BOX_SIZE = 40                # px por módulo -> QR de ~1480 px de lado
BORDER = 4                   # zona silenciosa estándar (4 módulos)


def build_qr():
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=BOX_SIZE, border=BORDER)
    qr.add_data(URL)
    qr.make(fit=True)
    return qr


def font(size, bold=False):
    candidatos = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidatos:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def main():
    qr = build_qr()
    qr_img = qr.make_image(fill_color=BOSQUE, back_color=BLANCO).convert("RGB")

    # --- 1) QR puro -------------------------------------------------------
    qr_img.save("qr-cpa-losalerces.png", "PNG", optimize=True)
    ancho, alto = qr_img.size
    print("qr-cpa-losalerces.png       -> %dx%d px, %d módulos, nivel M"
          % (ancho, alto, qr.modules_count))

    assert ancho >= MIN_PX and alto >= MIN_PX, "El QR debe medir al menos %d px" % MIN_PX

    # --- 2) Póster con encabezado ----------------------------------------
    pad = 90
    f_titulo = font(58, bold=True)
    f_sub = font(40)
    f_url = font(38, bold=True)

    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    lineas = [
        ("Centro de Padres", f_titulo, BOSQUE),
        ("Colegio Los Alerces", f_titulo, BOSQUE),
        ("Datos para transferencia bancaria", f_sub, GRIS),
    ]
    alto_texto = 0
    for texto, f, _ in lineas:
        alto_texto += tmp.textbbox((0, 0), texto, font=f)[3] + 18
    alto_url = tmp.textbbox((0, 0), URL, font=f_url)[3] + 22

    W = max(ancho + pad * 2, 1200)
    H = pad + alto_texto + 40 + alto + 34 + alto_url + pad
    poster = Image.new("RGB", (W, H), BLANCO)
    d = ImageDraw.Draw(poster)

    y = pad
    for texto, f, color in lineas:
        w = d.textbbox((0, 0), texto, font=f)[2]
        d.text(((W - w) / 2, y), texto, font=f, fill=color)
        y += d.textbbox((0, 0), texto, font=f)[3] + 18

    y += 40
    poster.paste(qr_img, (int((W - ancho) / 2), y))
    y += alto + 34

    w = d.textbbox((0, 0), URL, font=f_url)[2]
    d.text(((W - w) / 2, y), URL, font=f_url, fill=BOSQUE)

    poster.save("qr-cpa-losalerces-poster.png", "PNG", optimize=True)
    print("qr-cpa-losalerces-poster.png -> %dx%d px" % poster.size)
    print("URL codificada: %s" % URL)


if __name__ == "__main__":
    main()