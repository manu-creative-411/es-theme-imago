#!/usr/bin/env python3
"""Soft shadow of the front panel on the tab of the folder (inside the icon, so the size and the neon selector are not affected).

Every folder in _inc/system_icons/*.svg is two shapes (back panel with the tab = path46*, front panel = path50*). This script puts a
black rectangle with a vertical gradient between them: transparent at the top, darkest along the top edge of the front panel. It lies inside
the tab (no clipping in NanoSVG), so it stops at the flat part of the tab.
It is idempotent (the previous shadow, marked tab-shade / tabShade, is replaced), so the strength can be changed at any time.
Run it after editing icons or _template.svg, before make_folder_icons.py (which builds _folder.svg from the template) and make_folder_shadow.py.

Usage: python3 tools/make_tab_shadow.py [--strength 0.30] [--height 6]      (--strength 0 removes the shadow)
"""
import argparse
import glob
import os
import re

ICONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_inc", "system_icons")
EDGE_Y = 18.520832  # top edge of the front panel, in folder units
X_FROM, X_TO = 10.5, 64.0  # horizontal extent: inside the back panel for the whole height of the band
OLD_GRADIENT = re.compile(r'\s*<linearGradient id="tabShade".*?</linearGradient>', re.S)
OLD_SHAPE = re.compile(r'<rect id="tab-shade[^"]*"[^>]*/>')
FRONT = re.compile(r'(<path id="path50[\w-]*")')
DEFS_EMPTY = re.compile(r"<defs([^>]*?)\s*/>")


def gradient(strength, height):
    """The vertical gradient: transparent at the top of the band, black at the front panel."""
    return (f'<linearGradient id="tabShade" x1="0" y1="{EDGE_Y - height}" x2="0" y2="{EDGE_Y}" gradientUnits="userSpaceOnUse">'
            '<stop offset="0" style="stop-color:#000000;stop-opacity:0"/>'
            f'<stop offset="1" style="stop-color:#000000;stop-opacity:{strength}"/></linearGradient>')


def process(text, strength, height):
    """Return the SVG text with the shadow replaced (or removed when strength is 0); None if it has no folder."""
    if 'id="path50' not in text:
        return None
    text = OLD_SHAPE.sub("", OLD_GRADIENT.sub("", text))
    if strength <= 0:
        return text
    text = DEFS_EMPTY.sub(lambda m: f"<defs{m.group(1)}></defs>", text, count=1)
    text = text.replace("</defs>", gradient(strength, height) + "</defs>", 1)
    shape = (f'<rect id="tab-shade" x="{X_FROM}" y="{EDGE_Y - height}" width="{X_TO - X_FROM}" height="{height}" '
             'style="fill:url(#tabShade)"/>')
    return FRONT.sub(lambda m: shape + m.group(1), text)


def main():
    """Patch every icon and the template."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strength", type=float, default=0.30, help="opacity next to the front panel, 0..1 (0 = remove)")
    parser.add_argument("--height", type=float, default=6, help="height of the band in folder units (the tab is 12 high)")
    args = parser.parse_args()
    for path in sorted(glob.glob(os.path.join(ICONS, "*.svg"))):
        if os.path.basename(path) == "_folder.svg":
            continue
        with open(path, encoding="utf-8") as handle:
            result = process(handle.read(), args.strength, args.height)
        if result is not None:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(result)


if __name__ == "__main__":
    main()
