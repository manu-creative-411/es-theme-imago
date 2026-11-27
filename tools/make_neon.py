#!/usr/bin/env python3
"""Genera assets/ui/neon.png: nine-patch blanco con un contorno de neon (nucleo fino + resplandor SOLO hacia fuera).
Se tine en el layout con <backgroundColor>${neon}</backgroundColor>. Debe cumplirse  BAND == tCorner == tPad  (_inc/options/tiles.xml).
Uso: python3 tools/make_neon.py [BAND] [STROKE] [NAME] [FILL]      (por defecto 14, 3.0, neon.png y 0.16; px a 1080p)
FILL = opacidad (0..1) del interior, teñido con el mismo color (une el halo con el icono; 0 = interior transparente).
Tiles: python3 tools/make_neon.py 14 3.0 neon.png 0.16;  filas de lista: python3 tools/make_neon.py 12 3.0 neon-row.png 0"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
BAND = float(sys.argv[1]) if len(sys.argv) > 1 else 14
STROKE = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
NAME = sys.argv[3] if len(sys.argv) > 3 else "neon.png"
FILL = float(sys.argv[4]) if len(sys.argv) > 4 else 0.16
GAP = 1.0               # px entre la linea y la imagen (antes 2.5: el aro se veia despegado)
RADIUS = 7.0            # radio de las esquinas de la linea
SS = 4                  # supermuestreo
S = int(BAND * 2 + 32)  # banda + centro estirable (32px) + banda
W = S * SS
inset = BAND - GAP - STROKE / 2           # centro de la linea (queda GAP px de hueco hasta la imagen)
def rr(draw, d, fill):
    draw.rounded_rectangle([d * SS, d * SS, W - d * SS - 1, W - d * SS - 1], radius=RADIUS * SS, fill=fill)
core = Image.new("L", (W, W), 0); d = ImageDraw.Draw(core)
rr(d, inset - STROKE / 2, 255); rr(d, inset + STROKE / 2, 0)               # anillo
inside = Image.new("L", (W, W), 0); rr(ImageDraw.Draw(inside), inset, 255)  # todo lo de dentro de la linea
c = np.asarray(core, np.float32) / 255
g1 = np.asarray(core.filter(ImageFilter.GaussianBlur(2.2 * SS)), np.float32) / 255
g2 = np.asarray(core.filter(ImageFilter.GaussianBlur(6.0 * SS)), np.float32) / 255
a = np.clip(c + 2.0 * g1 + 3.4 * g2, 0, 1) ** 0.85
ins = np.asarray(inside, np.float32) / 255
a *= 1 - ins * (1 - c)                                                      # sin resplandor hacia dentro
a = np.maximum(a, ins * (1 - c) * FILL)                                     # velo del interior
yy, xx = np.mgrid[0:W, 0:W] / SS                                            # ventana: el resplandor llega a 0 en el borde del parche
edge = np.minimum.reduce([xx, yy, S - xx, S - yy])
a *= np.clip(edge / 4.0, 0, 1) ** 1.5
img = np.zeros((W, W, 4), np.uint8); img[..., :3] = 255; img[..., 3] = (a * 255).astype(np.uint8)
out = Image.fromarray(img, "RGBA").resize((S, S), Image.LANCZOS)
dst = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "ui", NAME)
out.save(dst); print("ok:", dst, out.size, "cornerSize =", int(BAND))
