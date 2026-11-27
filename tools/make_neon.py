#!/usr/bin/env python3
"""Generate the selection frames: assets/ui/neon-<set>.png (grid tiles) and assets/ui/neon-row-<set>.png (list rows).

Each PNG is a nine-patch holding a crisp rounded-rectangle frame: 1 px white outline, then a band that goes from the
<neon> colour (outside) to <neon2> (inside) and fades into white at its inner edge. The colours are baked in, so the layouts tint with white (FFFFFFFF).
One pair of files per colour set in _inc/colorsets/ (<neon> and <neon2> are read from each XML).

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
TILE_THICK = 10   # px of the gradient band on tiles (between the outer white line and the inner blend)
TILE_GAP = 1      # px between the frame and the image
TILE_RADIUS = 12  # outer corner radius
ROW_BAND = 12
ROW_THICK = 6
ROW_RADIUS = 11
BLEND = 0.35      # fraction of the band, at its inner side, that fades smoothly to white
CENTRE = 32       # stretchable centre


def hex_rgb(value):
    return np.array([int(value[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255


def frame(band, thick, offset, radius, col1, col2):
    """RGBA nine-patch: 1 px white outline, a band going from col1 (outside) to col2 (inside) whose inner part
    blends into white, all in a rounded rectangle whose outer edge is `offset` px from the patch edge."""
    size = band * 2 + CENTRE
    big = size * SS
    yy, xx = np.mgrid[0:big, 0:big]
    px, py = (xx + 0.5) / SS - size / 2, (yy + 0.5) / SS - size / 2
    half = size / 2 - offset
    qx, qy = np.abs(px) - (half - radius), np.abs(py) - (half - radius)
    sd = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - radius
    depth = -sd                                   # px inwards from the outer edge
    inside = (depth >= 0) & (depth < 1 + thick)
    t = np.clip((depth - 1) / thick, 0, 1)[..., None]
    rgb = col1 * (1 - t) + col2 * t
    w = np.clip((t - (1 - BLEND)) / BLEND, 0, 1)  # 0 -> 1 across the inner part of the band
    w = w * w * (3 - 2 * w)
    rgb = rgb * (1 - w) + w
    rgb = np.where((depth < 1)[..., None], 1.0, rgb)   # crisp 1 px white outline
    acc = np.zeros((big, big, 4), np.float32)
    acc[..., :3] = rgb * inside[..., None]
    acc[..., 3] = inside
    small = acc.reshape(size, SS, size, SS, 4).mean(axis=(1, 3))
    alpha = small[..., 3:4]
    out = np.concatenate([np.where(alpha > 0, small[..., :3] / np.maximum(alpha, 1e-6), 1.0), alpha], axis=2)
    return Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")


def main():
    sets_dir = os.path.join(ROOT, "_inc", "colorsets")
    ui_dir = os.path.join(ROOT, "assets", "ui")
    for fname in sorted(os.listdir(sets_dir)):
        if not fname.endswith(".xml"):
            continue
        name = fname[:-4]
        with open(os.path.join(sets_dir, fname), encoding="utf-8") as fh:
            text = fh.read()
        match = re.search(r"<neon>([0-9A-Fa-f]{6})</neon>", text)
        match2 = re.search(r"<neon2>([0-9A-Fa-f]{6})</neon2>", text)
        if not match or not match2:
            continue
        col1, col2 = hex_rgb(match.group(1)), hex_rgb(match2.group(1))
        tile = frame(TILE_BAND, TILE_THICK, TILE_BAND - TILE_GAP - 1 - TILE_THICK, TILE_RADIUS, col1, col2)
        row = frame(ROW_BAND, ROW_THICK, 0, ROW_RADIUS, col1, col2)
        tile.save(os.path.join(ui_dir, f"neon-{name}.png"))
        row.save(os.path.join(ui_dir, f"neon-row-{name}.png"))
        print("ok:", name, match.group(1), match2.group(1))


if __name__ == "__main__":
    main()
