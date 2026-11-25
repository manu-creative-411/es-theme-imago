#!/usr/bin/env python3
"""Generates assets/ui/shadow.png: the soft drop shadow of the cards (nine-patch, used with <ninepatch> cornerSize 40).
Black, alpha only: the colour set tints it (variable shadowColor). 96x96 px at 1080p; the card sits 24 px inside it, corner radius 24."""
import os
from PIL import Image, ImageDraw, ImageFilter
S, M, R, SIGMA, PEAK = 96, 24, 24, 8, 0.62
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([M, M, S - M - 1, S - M - 1], R, fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(SIGMA)).point(lambda v: int(v * PEAK))
img = Image.new("RGBA", (S, S), (0, 0, 0, 0)); img.putalpha(mask)
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "ui", "shadow.png")
img.save(out); print("written", out)
