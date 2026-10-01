#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Revisa index.html antes de publicarlo.

Comprueba la estructura del HTML (etiquetas equilibradas), que el logo y el
favicon estén incrustados, y —lo más importante— que el texto visible de cada
dato coincida con su atributo data-value, que es lo que realmente se copia.

Uso:
    python3 verificar-pagina.py [index.html]

Sale con código 1 si encuentra algún problema.
"""

import re
import sys
from html.parser import HTMLParser

ARCHIVO = sys.argv[1] if len(sys.argv) > 1 else "index.html"

fallas = []
avisos = []


class Revisor(HTMLParser):
    """Comprueba que las etiquetas de bloque principales estén equilibradas."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pila = []
        self.errores = []
        self.texto_fuera_de_etiqueta = []

    def handle_starttag(self, tag, attrs):
        if tag in ("br", "meta", "link", "img", "input", "hr", "source"):
            return
        self.pila.append(tag)

    def handle_endtag(self, tag):
        if tag in ("br", "meta", "link", "img", "input", "hr", "source"):
            return
        if not self.pila:
            self.errores.append("cierre </%s> sin apertura" % tag)
        elif self.pila[-1] != tag:
            self.errores.append("se esperaba </%s> y llegó </%s>" % (self.pila[-1], tag))
            if tag in self.pila:
                while self.pila and self.pila.pop() != tag:
                    pass
        else:
            self.pila.pop()

    def handle_data(self, data):
        limpio = data.strip()
        # texto suelto dentro de <head> o del documento que no debería estar visible
        if self.pila and self.pila[-1] in ("html", "head") and limpio:
            self.texto_fuera_de_etiqueta.append(limpio[:60])


html = open(ARCHIVO, encoding="utf-8").read()

# --- estructura básica ----------------------------------------------------
if html.lstrip().startswith("<!DOCTYPE html>"):
    print("OK    doctype")
else:
    fallas.append("falta <!DOCTYPE html> al inicio")

if '<html lang="es-CL">' in html:
    print("OK    idioma es-CL declarado")
else:
    avisos.append("no se declara lang=es-CL")

# --- etiquetas de estilo --------------------------------------------------
for etiqueta in ("<style>", "</style>", "<head>", "</head>", "<body>", "</body>"):
    cuenta = html.count(etiqueta)
    if cuenta == 1:
        print("OK    %s aparece una vez" % etiqueta)
    else:
        fallas.append("%s aparece %d veces (debería ser 1)" % (etiqueta, cuenta))

# --- estructura del árbol ------------------------------------------------
revisor = Revisor()
revisor.feed(html)
if revisor.errores:
    fallas.extend(revisor.errores[:5])
else:
    print("OK    etiquetas equilibradas")
if revisor.pila:
    fallas.append("quedaron etiquetas sin cerrar: %s" % ", ".join(revisor.pila))
if revisor.texto_fuera_de_etiqueta:
    fallas.append("texto suelto en <head>/<html>: %s" % " | ".join(revisor.texto_fuera_de_etiqueta))
else:
    print("OK    sin texto suelto en <head>")

# --- recursos incrustados -------------------------------------------------
if html.count('class="logo-img"') == 1 and 'src="data:image/png;base64,' in html:
    print("OK    logo incrustado (data URI)")
else:
    fallas.append("falta el logo incrustado")

if html.count('rel="icon"') == 1 and html.count('rel="apple-touch-icon"') == 1:
    print("OK    favicon e icono de inicio")
else:
    fallas.append("los iconos del navegador no están bien")

if html.count("PLACEHOLDER") or html.count("data:image/png;base64,") < 3:
    fallas.append("quedaron marcadores sin reemplazar")

# --- JavaScript necesario para copiar ------------------------------------
if "navigator.clipboard" in html and "execCommand(\"copy\")" in html:
    print("OK    portapapeles: API moderna + respaldo execCommand")
else:
    fallas.append("falta alguna de las dos vías de copiado")

# --- filas de datos: visible vs. data-value ------------------------------
filas = re.findall(
    r'<button class="row"[^>]*data-field="([^"]*)"[^>]*data-value="([^"]*)"[^>]*>(.*?)</button>',
    html, flags=re.S)

if not filas:
    fallas.append("no se encontró ninguna fila de datos")
else:
    print("OK    %d filas de datos" % len(filas))
    for campo, valor, cuerpo in filas:
        visible = re.search(r'<span class="value">(.*?)</span>', cuerpo, flags=re.S)
        etiqueta = re.search(r'<span class="label">(.*?)</span>', cuerpo, flags=re.S)
        visible = visible.group(1).strip() if visible else None
        etiqueta = etiqueta.group(1).strip() if etiqueta else None
        if etiqueta != campo:
            fallas.append("fila %r: la etiqueta visible dice %r" % (campo, etiqueta))
        if visible != valor:
            fallas.append("fila %r: se copia %r pero se ve %r" % (campo, valor, visible))
    if not any("se copia" in f for f in fallas):
        print("OK    cada dato visible coincide con lo que se copia")

# --- botón y pie ----------------------------------------------------------
if 'id="copyAll"' in html and "Copiar todos los datos" in html:
    print("OK    botón 'Copiar todos los datos'")
else:
    fallas.append("falta el botón 'Copiar todos los datos'")

if "centrodepadres@colegiolosalerces.cl" in html and "Envía el comprobante" in html:
    print("OK    pie con el correo para enviar el comprobante")
else:
    fallas.append("falta el pie con el correo")

# --- resumen --------------------------------------------------------------
print()
for aviso in avisos:
    print("AVISO %s" % aviso)
if fallas:
    for falla in fallas:
        print("FALLA %s" % falla)
    print("\n%d problema(s) encontrado(s). NO publicar todavía." % len(fallas))
    sys.exit(1)

print("Página correcta: %.1f KB, lista para publicar." % (len(html.encode()) / 1024))