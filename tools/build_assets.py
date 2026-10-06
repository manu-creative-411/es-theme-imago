#!/usr/bin/env python3
"""Genera la estructura plana que usa el tema (sin firstfile()).
Ejecutar desde la carpeta del tema:  python3 tools/build_assets.py
  system_bg/<theme>.jpg                     <- sale de system_bg/ o system_bg/collections/
  system_logos/<tone>-<region>/<theme>.svg  <- sale de system_logos/<theme>/... o system_logos/<theme>.svg
"""
import os, shutil, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") if os.path.basename(os.path.dirname(os.path.abspath(__file__)))=="tools" else os.path.dirname(os.path.abspath(__file__))
inc = os.path.join(root, "_inc")
bg, logos, icons = (os.path.join(inc, d) for d in ("system_bg", "system_logos", "system_icons"))
TONES, REGIONS = ("dark", "light"), ("none", "us", "jp", "eu", "br")
skip = set(f"{t}-{r}" for t in TONES for r in REGIONS + ("none",))
for t in TONES:                      # limpia carpetas generadas antes
    for r in REGIONS + ("none",):
        shutil.rmtree(os.path.join(logos, f"{t}-{r}"), ignore_errors=True)

# --- fondos: un <theme>.jpg por sistema
n_bg = 0
col = os.path.join(bg, "collections")
if os.path.isdir(col):
    for f in os.listdir(col):
        if f.lower().endswith(".jpg") and not os.path.exists(os.path.join(bg, f)):
            shutil.copy(os.path.join(col, f), os.path.join(bg, f)); n_bg += 1

# --- logos
themes = {}
for e in os.listdir(logos):
    p = os.path.join(logos, e)
    if e in skip or e.lower() == "readme.txt": continue
    if os.path.isdir(p): themes.setdefault(e, {})["dir"] = p
    elif e.endswith(".svg"): themes.setdefault(e[:-4], {})["flat"] = p

def pick(t, info, tone, region):
    """Prioridad: <tone>-<region> > <region> > <tone> > plano > otras regiones (eu, us, jp)."""
    d, flat = info.get("dir"), info.get("flat")
    c = []
    if d:
        c += [f"{tone}-{region}.svg", f"{region}.svg", f"{tone}.svg"]
        c += [f"{tone}-{x}.svg" for x in ("eu", "us", "jp") if x != region]
        c += [f"{x}.svg" for x in ("eu", "us", "jp") if x != region]
        c = [os.path.join(d, x) for x in c]
    if flat: c.insert(len(c) if not d else 3, flat)
    return next((x for x in c if os.path.isfile(x)), None)

n_logo = 0
for tone in TONES:
    for region in REGIONS:
        out = os.path.join(logos, f"{tone}-{region}"); os.makedirs(out, exist_ok=True)
        for t, info in themes.items():
            src = pick(t, info, tone, region)
            if src: shutil.copy(src, os.path.join(out, t + ".svg")); n_logo += 1
        if not os.listdir(out): os.rmdir(out)

# --- alias de iconos (nombres de tema distintos del archivo)
ALIAS = {"gc": "gamecube"}
for a, b in ALIAS.items():
    s, d = os.path.join(icons, b + ".svg"), os.path.join(icons, a + ".svg")
    if os.path.isfile(s) and not os.path.exists(d): shutil.copy(s, d)
print(f"fondos copiados: {n_bg}, logos generados: {n_logo}")

# --- fondos de pantalla: para cada assets/wallpapers/<name>.svg genera <name>-b1.svg y <name>-b2.svg,
# recortados a la zona que queda DEBAJO del banner (1 y 2 filas). Sirven de "mascara" para que el
# fondo se vea continuo bajo la foto de consola.  bH1/bH2 deben coincidir con _inc/options/banner-on.xml
import re
BH = {"b1": 0.506, "b2": 0.386}
wp = os.path.join(root, "assets", "wallpapers")
for f in sorted(os.listdir(wp)):
    if not f.endswith(".svg") or re.search(r"-b[12]\.svg$", f): continue
    s = open(os.path.join(wp, f), encoding="utf-8").read()
    m = re.search(r"<svg\b[^>]*>", s)
    root_tag = m.group(0)
    vb = re.search(r'viewBox="([\d.\s-]+)"', root_tag)
    x0, y0, w, h = (float(v) for v in vb.group(1).split())
    for k, bh in BH.items():
        ny, nh = y0 + h * bh, h * (1 - bh)
        t = re.sub(r'viewBox="[^"]*"', f'viewBox="{x0:g} {ny:.2f} {w:g} {nh:.2f}"', root_tag)
        t = re.sub(r'\bheight="[^"]*"', f'height="{nh:.2f}"', t, count=1)
        t = re.sub(r'(?<![-\w])width="[^"]*"', f'width="{w:g}"', t, count=1)
        open(os.path.join(wp, f[:-4] + f"-{k}.svg"), "w", encoding="utf-8").write(s.replace(root_tag, t, 1))
print("fondos recortados generados")
