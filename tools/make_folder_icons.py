#!/usr/bin/env python3
"""Pastel folder colours for the system icons + the generic fallback folder.

1. Every gradient that paints a folder (ids linearGradient16/18 + "_tint" or "-<combo>") gets its stops blended towards white and slightly
   desaturated (the glyph gradients are left alone). The gradient is flagged with data-pastel="1", so running the script again is harmless.
2. _inc/system_icons/_folder.svg (generic folder used when a system has no icon of its own) is built from _template.svg:
   one colour combo kept visible, the others removed.

Usage: python3 tools/make_folder_icons.py [--mix 0.30] [--sat 1.05] [--combo azure-blue]
"""
import argparse
import colorsys
import glob
import os
import re
import xml.etree.ElementTree as ET

ICONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_inc", "system_icons")
GRADIENT = re.compile(r'<linearGradient\b[^>]*?\bid="linearGradient1[68](?:_tint|-[\w-]+)"[^>]*>.*?</linearGradient>', re.S)
STOP = re.compile(r"stop-color:#([0-9a-fA-F]{6})")


def pastel(hex6, mix, sat):
    """Blend a colour with white (mix) and scale its saturation (sat)."""
    red, green, blue = (int(hex6[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hue, light, satur = colorsys.rgb_to_hls(red, green, blue)
    red, green, blue = colorsys.hls_to_rgb(hue, light, satur * sat)
    red, green, blue = (c + (1 - c) * mix for c in (red, green, blue))
    return "".join(f"{round(c * 255):02x}" for c in (red, green, blue))


def pastelize(text, mix, sat):
    """Return the SVG text with every not-yet-processed folder gradient made pastel."""
    def fix(match):
        block = match.group(0)
        if 'data-pastel="1"' in block:
            return block
        block = STOP.sub(lambda m: "stop-color:#" + pastel(m.group(1), mix, sat), block)
        return block.replace("<linearGradient", '<linearGradient data-pastel="1"', 1)
    return GRADIENT.sub(fix, text)


def build_folder(combo):
    """Generic folder: _template.svg with a single colour combo left (and visible)."""
    ink = "http://www.inkscape.org/namespaces/inkscape"
    for prefix, uri in (("", "http://www.w3.org/2000/svg"), ("inkscape", ink), ("xlink", "http://www.w3.org/1999/xlink"),
                        ("sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")):
        ET.register_namespace(prefix, uri)
    tree = ET.parse(os.path.join(ICONS, "_template.svg"))
    root = tree.getroot()
    layer = next(g for g in root if g.get("id") == "layer1")
    for grp in list(layer):
        gid = grp.get("id", "")
        if gid.startswith("color-"):
            if gid == "color-" + combo:
                grp.set("style", "display:inline")
            else:
                layer.remove(grp)
    for grad in list(root.find("{http://www.w3.org/2000/svg}defs")):
        gid = grad.get("id", "")
        if re.match(r"linearGradient1[68]-", gid) and not gid.endswith("-" + combo):
            root.find("{http://www.w3.org/2000/svg}defs").remove(grad)
    tree.write(os.path.join(ICONS, "_folder.svg"), encoding="utf-8", xml_declaration=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--mix", type=float, default=0.30, help="blend with white, 0..1")
    parser.add_argument("--sat", type=float, default=1.05, help="saturation factor")
    parser.add_argument("--combo", default="azure-blue", help="colour combo of the generic folder")
    args = parser.parse_args()
    for path in sorted(glob.glob(os.path.join(ICONS, "*.svg"))):
        if os.path.basename(path) == "_folder.svg":
            continue
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        new = pastelize(text, args.mix, args.sat)
        if new != text:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(new)
    build_folder(args.combo)


if __name__ == "__main__":
    main()
