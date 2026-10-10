#!/usr/bin/env python3
"""Generates the derived assets of the theme. Run it from anywhere:  python3 tools/build_assets.py
  system_bg/<theme>.jpg          <- copied from system_bg/collections/ when missing
  system_icons/<alias>.svg       <- alias copies (theme name differs from the file name, e.g. gc -> gamecube)
  assets/wallpapers/<name>-b1/b2.svg  <- wallpaper crops below the banner (1 and 2 rows)
Console logos need NO generation: they are resolved by the ordered <path> list in the layouts (see README)."""
import os, re, shutil
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
inc = os.path.join(root, "_inc")
bg, icons = os.path.join(inc, "system_bg"), os.path.join(inc, "system_icons")

# --- backgrounds: one <theme>.jpg per system
n_bg = 0
col = os.path.join(bg, "collections")
if os.path.isdir(col):
    for f in os.listdir(col):
        if f.lower().endswith(".jpg") and not os.path.exists(os.path.join(bg, f)):
            shutil.copy(os.path.join(col, f), os.path.join(bg, f)); n_bg += 1

# --- icon aliases
for a, b in {"gc": "gamecube"}.items():
    s, d = os.path.join(icons, b + ".svg"), os.path.join(icons, a + ".svg")
    if os.path.isfile(s) and not os.path.exists(d): shutil.copy(s, d)

# --- wallpapers: <name>-b1.svg / -b2.svg = crop of the area BELOW the banner (must match bH1/bH2 in banner-on.xml)
BH = {"b1": 0.506, "b2": 0.386}
wp = os.path.join(root, "assets", "wallpapers")
for f in sorted(os.listdir(wp)):
    if not f.endswith(".svg") or re.search(r"-b[12]\.svg$", f): continue
    s = open(os.path.join(wp, f), encoding="utf-8").read()
    root_tag = re.search(r"<svg\b[^>]*>", s).group(0)
    x0, y0, w, h = (float(v) for v in re.search(r'viewBox="([\d.\s-]+)"', root_tag).group(1).split())
    for k, bh in BH.items():
        ny, nh = y0 + h * bh, h * (1 - bh)
        t = re.sub(r'viewBox="[^"]*"', f'viewBox="{x0:g} {ny:.2f} {w:g} {nh:.2f}"', root_tag)
        t = re.sub(r'\bheight="[^"]*"', f'height="{nh:.2f}"', t, count=1)
        t = re.sub(r'(?<![-\w])width="[^"]*"', f'width="{w:g}"', t, count=1)
        open(os.path.join(wp, f[:-4] + f"-{k}.svg"), "w", encoding="utf-8").write(s.replace(root_tag, t, 1))
print(f"backgrounds copied: {n_bg}; wallpaper crops regenerated")
