#!/usr/bin/env python3
"""Soft drop shadow (offset 0,0) baked into the folder system icons.

ES draws grid tiles without shaders and its SVG rasteriser (NanoSVG) has no filters, so the blur is faked: the folder silhouette is
repeated RADII times as a black shape with a growing round stroke and a very low opacity, which stacks into a smooth falloff.
The shadow group (id="imago-shadow") sits before the folder, inside the same transform, and the viewBox is widened by --pad units on
every side so the halo is not clipped. Running the script again replaces the previous shadow, so --pad / --strength can be tuned.

Run it AFTER make_folder_icons.py (that script rebuilds _folder.svg from the unpadded template).

Usage: python3 tools/make_icon_shadow.py [--pad 10] [--radius 9] [--strength 0.05]
"""
import argparse
import glob
import os
import re

ICONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_inc", "system_icons")
SIZE = 135.46666  # the original (unpadded) viewBox side
OLD = re.compile(r'<g id="imago-shadow".*?</g>', re.S)
FOLDER = re.compile(r'<g id="g50[\w-]*"((?: transform="[^"]+")?)>\s*<path id="path46[\w-]*"[^>]*?\sd="([^"]+)"[^>]*?/>\s*<path id="path50[\w-]*"[^>]*?\sd="([^"]+)"', re.S)
SCALE = re.compile(r"matrix\(([\d.]+),")


def shadow_group(transform, paths, radius, strength):
    """Build the stacked-stroke halo for the given silhouette paths."""
    found = SCALE.search(transform)
    scale = float(found.group(1)) if found else 1.0
    out = [f'<g id="imago-shadow"{transform} style="fill:#000000;stroke:#000000;stroke-linejoin:round">']
    for step in range(radius, 0, -1):
        width = 2 * step / scale
        for path in paths:
            out.append(f'<path d="{path}" style="fill-opacity:{strength};stroke-opacity:{strength};stroke-width:{width:.3f}"/>')
    out.append("</g>")
    return "".join(out)


def process(text, pad, radius, strength):
    """Return the SVG text with the shadow (re)generated, or None if the file has no folder."""
    text = OLD.sub("", text)
    match = FOLDER.search(text)
    if not match:
        return None
    group = shadow_group(match.group(1), (match.group(2), match.group(3)), radius, strength)
    start = text.index(match.group(0))
    text = text[:start] + group + text[start:]
    box = f"{-pad:g} {-pad:g} {SIZE + 2 * pad:.5f} {SIZE + 2 * pad:.5f}"
    return re.sub(r'viewBox="[^"]+"', f'viewBox="{box}"', text, count=1)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pad", type=float, default=10)
    parser.add_argument("--radius", type=int, default=9)
    parser.add_argument("--strength", type=float, default=0.05)
    args = parser.parse_args()
    for name in sorted(glob.glob(os.path.join(ICONS, "*.svg"))):
        if os.path.basename(name).startswith("_template"):
            continue  # sources of make_folder_icons.py: keep them unpadded
        with open(name, encoding="utf-8") as src:
            result = process(src.read(), args.pad, args.radius, args.strength)
        if result is not None:
            with open(name, "w", encoding="utf-8") as dst:
                dst.write(result)


if __name__ == "__main__":
    main()
