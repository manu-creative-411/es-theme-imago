#!/usr/bin/env python3
"""Generate the selection frames: assets/ui/neon-<set>.png (grid tiles) and assets/ui/neon-row-<set>.png (list rows).

Each PNG is a nine-patch holding a crisp rounded-rectangle frame: 1 px white outline, a band in the colour set's
<neon> colour, and a 1 px white inner line. The colours are baked in, so the layouts tint with white (FFFFFFFF).
One pair of files per colour set in _inc/colorsets/ (the <neon> value is read from each XML).

Usage: python3 tools/make_neon.py            (all sets)
Constraint: TILE_BAND must equal <tPad> in _inc/options/tiles.xml; ROW_BAND must equal cornerSize in gen lists (12).
"""
import os
import re
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SS = 8            # supersampling
TILE_BAND = 14    # px of the tile nine-patch border (== tPad)
TILE_THICK = 4    # px of the coloured band on tiles
TILE_GAP = 1      # px between the inner white line and the image
TILE_RADIUS = 9   # outer corner radius
ROW_BAND = 12
ROW_THICK = 3
ROW_RADIUS = 8
CENTRE = 32       # stretchable centre


def hex_rgb(value):
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def frame(band, thick, offset, radius, colour):
    """Return an RGBA image: white / colour / white rounded frame whose outer edge is `offset` px from the edge."""
    size = band * 2 + CENTRE
    big = size * SS
    acc = np.zeros((big, big, 4), np.float32)   # premultiplied

    def paint(inset, rad, rgb, alpha):
        img = np.zeros((big, big), bool)
        yy, xx = np.mgrid[0:big, 0:big]
        lo, hi = inset * SS, big - inset * SS
        r = max(rad, 0.01) * SS
        cx = np.clip(xx + 0.5, lo + r, hi - r)
        cy = np.clip(yy + 0.5, lo + r, hi - r)
        img = ((xx + 0.5 - cx) ** 2 + (yy + 0.5 - cy) ** 2 <= r * r) & (xx >= lo) & (xx < hi) & (yy >= lo) & (yy < hi)
        acc[img, :3] = np.array(rgb, np.float32) / 255 * alpha
        acc[img, 3] = alpha

    paint(offset, radius, (255, 255, 255), 1.0)
    paint(offset + 1, radius - 1, colour, 1.0)
    paint(offset + 1 + thick, radius - 1 - thick, (255, 255, 255), 1.0)
    paint(offset + 2 + thick, radius - 2 - thick, (0, 0, 0), 0.0)
    small = acc.reshape(size, SS, size, SS, 4).mean(axis=(1, 3))
    alpha = small[..., 3:4]
    rgb = np.where(alpha > 0, small[..., :3] / np.maximum(alpha, 1e-6), 1.0)
    out = np.concatenate([rgb, alpha], axis=2)
    return Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")


def main():
    sets_dir = os.path.join(ROOT, "_inc", "colorsets")
    ui_dir = os.path.join(ROOT, "assets", "ui")
    for fname in sorted(os.listdir(sets_dir)):
        if not fname.endswith(".xml"):
            continue
        name = fname[:-4]
        with open(os.path.join(sets_dir, fname), encoding="utf-8") as fh:
            match = re.search(r"<neon>([0-9A-Fa-f]{6})</neon>", fh.read())
        if not match:
            continue
        colour = hex_rgb(match.group(1))
        tile = frame(TILE_BAND, TILE_THICK, TILE_BAND - TILE_GAP - 2 - TILE_THICK, TILE_RADIUS, colour)
        row = frame(ROW_BAND, ROW_THICK, 0, ROW_RADIUS, colour)
        tile.save(os.path.join(ui_dir, f"neon-{name}.png"))
        row.save(os.path.join(ui_dir, f"neon-row-{name}.png"))
        print("ok:", name, match.group(1))


if __name__ == "__main__":
    main()
