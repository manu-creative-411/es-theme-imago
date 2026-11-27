#!/usr/bin/env python3
"""Colour-set wallpapers (3DS-style grid of squares) derived from the black one.

assets/wallpapers/dark*.svg is the black set's wallpaper (plain page, grey-blue squares, darker fade on the right). For every other colour set this
script copies it with three colours swapped (matched by role, not by value, so it can be run again with other settings):
  - base     = the page rectangle     -> the set's flat background colour (bg) blended towards black by "dim"
  - squares  = the 112 grid squares   -> that base blended towards white
  - shade    = the edge vignette (both stops of its gradient) -> that base blended towards black
It writes <set>.svg, <set>-b1.svg and <set>-b2.svg (full screen and the two crops used under the banner).

Usage: python3 tools/make_wallpapers.py
"""
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
WALL = os.path.join(ROOT, "assets", "wallpapers")
SETS = {  # set -> (bg, white blend for the squares, black blend for the fade, dim of the base)
    "light-gray": ("D4D4DA", 0.65, 0.10, 0.0),
    "vivid-red": ("E10B24", 0.30, 0.45, 0.35),
    "deep-blue": ("0A56D6", 0.30, 0.45, 0.35),
    "gamecube-purple": ("6F4DE0", 0.30, 0.45, 0.42),
    "aqua-green": ("14C9B0", 0.30, 0.45, 0.0),
}
BASE = re.compile(r'fill:#[0-9a-fA-F]{6}(;fill-opacity:1;stroke-width:20;paint-order:stroke fill markers" width="1920")')
SQUARE = re.compile(r"fill:#[0-9a-fA-F]{6}(;fill-opacity:1;stroke:none;stroke-width:7\.28019)")
SHADE = re.compile(r"stop-color:#[0-9a-fA-F]{6}(;stop-opacity:(?:0\.52403355|0);\" offset=\"[01]\" id=\"stop44[45]\")")


def blend(hex6, other, amount):
    """Mix a colour with white (255) or black (0)."""
    return "".join(f"{round(int(hex6[i:i + 2], 16) * (1 - amount) + other * amount):02x}" for i in (0, 2, 4))


def recolor(text, bg, white, black, dim=0.0):
    """Swap the three role colours of a wallpaper SVG."""
    bg = blend(bg, 0, dim)
    text = BASE.sub(lambda m: f"fill:#{bg.lower()}{m.group(1)}", text)
    text = SQUARE.sub(lambda m: f"fill:#{blend(bg, 255, white)}{m.group(1)}", text)
    return SHADE.sub(lambda m: f"stop-color:#{blend(bg, 0, black)}{m.group(1)}", text)


def main():
    for name, (bg, white, black, dim) in SETS.items():
        for suffix in ("", "-b1", "-b2"):
            with open(os.path.join(WALL, f"dark{suffix}.svg"), encoding="utf-8") as src:
                text = src.read()
            with open(os.path.join(WALL, f"{name}{suffix}.svg"), "w", encoding="utf-8") as dst:
                dst.write(recolor(text, bg, white, black, dim))


if __name__ == "__main__":
    main()
