#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica que los PNG de QR se decodifiquen a la URL esperada."""

import sys

import cv2

ESPERADA = "https://cpa-losalerces.netlify.app/"
ARCHIVOS = ["qr-cpa-losalerces.png", "qr-cpa-losalerces-poster.png"]

detector = cv2.QRCodeDetector()
todo_ok = True

for archivo in ARCHIVOS:
    img = cv2.imread(archivo)
    if img is None:
        print("FALLA  %-30s no se pudo leer" % archivo)
        todo_ok = False
        continue
    alto, ancho = img.shape[:2]
    datos, puntos, _ = detector.detectAndDecode(img)
    ok = datos == ESPERADA
    todo_ok = todo_ok and ok
    print("%s  %-30s %dx%d px  ->  %s"
          % ("OK    " if ok else "FALLA ", archivo, ancho, alto, datos or "(sin lectura)"))

if not todo_ok:
    print("\nLa verificación falló.")
    sys.exit(1)

print("\nAmbos QR apuntan correctamente a: %s" % ESPERADA)
