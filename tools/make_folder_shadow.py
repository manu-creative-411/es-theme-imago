#!/usr/bin/env python3
"""Soft drop shadow (offset 0,0) under the whole folder shape, baked into the system icons.

ES draws a grid tile from one image without shaders and NanoSVG has no filters, so the blur is faked: the silhouette of the folder
(the back panel, which is the whole outline with the tab) is repeated as black shapes with a growing round stroke and a very low opacity, which stack into a smooth
falloff. The group (id="folder-shadow") goes before the folder. The icons' folders fill their whole viewBox, so the viewBox is widened by
--pad units per side to make room (the folder looks that much smaller; _folder.svg already has a margin and is not widened).
Idempotent: the previous shadow is replaced and the viewBox is recomputed, so --radius / --strength can be tuned. Run it LAST, after
make_folder_icons.py (which rebuilds _folder.svg).

Usage: python3 tools/make_folder_shadow.py [--radius 3.5] [--strength 0.05] [--pad 4]      (--strength 0 removes the shadow)
"""
import argparse
import glob
import os
import xml.etree.ElementTree as ET

ICONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_inc", "system_icons")
SVG = "http://www.w3.org/2000/svg"
FRAME = 135.46666
STEPS_PER_UNIT = 2


def load(path):
    """Parse a file keeping its namespace prefixes."""
    for _event, (prefix, uri) in ET.iterparse(path, events=("start-ns",)):
        ET.register_namespace(prefix, uri)
    return ET.parse(path)


def find_folder(root):
    """Return (parent, folder group, [d of the outline]) or None."""
    for parent in root.iter():
        for group in parent:
            if group.tag == f"{{{SVG}}}g" and group.get("id", "").startswith("g50"):
                paths = [p.get("d") for p in group if p.tag == f"{{{SVG}}}path" and p.get("id", "").startswith("path46")]
                if len(paths) == 1:
                    return parent, group, paths
    return None


def scale_of(group):
    """Scale factor of the group's matrix transform (1 without transform)."""
    transform = group.get("transform", "")
    return float(transform[7:].split(",")[0]) if transform.startswith("matrix(") else 1.0


def shadow_group(group, paths, radius, strength):
    """Build the stacked-stroke halo with the same transform as the folder."""
    attrs = {"id": "folder-shadow", "style": "fill:#000000;stroke:#000000;stroke-linejoin:round"}
    if group.get("transform"):
        attrs["transform"] = group.get("transform")
    shadow = ET.Element(f"{{{SVG}}}g", attrs)
    scale = scale_of(group)
    for step in range(int(radius * STEPS_PER_UNIT), 0, -1):
        width = 2 * (step / STEPS_PER_UNIT) / scale
        for path in paths:
            ET.SubElement(shadow, f"{{{SVG}}}path", {"d": path, "style": f"fill-opacity:{strength};stroke-opacity:{strength};"
                                                                        f"stroke-width:{width:.3f}"})
    return shadow


def process(path, radius, strength, pad):
    """Rewrite one icon; returns False when it has no folder."""
    tree = load(path)
    root = tree.getroot()
    for parent in list(root.iter()):
        for child in list(parent):
            if child.get("id") == "folder-shadow":
                parent.remove(child)
    found = find_folder(root)
    if found is None:
        return False
    parent, group, paths = found
    widen = os.path.basename(path) != "_folder.svg"
    margin = pad if widen else 0
    root.set("viewBox", f"{-margin:g} {-margin:g} {FRAME + 2 * margin:.5f} {FRAME + 2 * margin:.5f}")
    if strength > 0:
        parent.insert(list(parent).index(group), shadow_group(group, paths, radius, strength))
    ET.indent(tree)
    tree.write(path, encoding="utf-8", xml_declaration=True)
    return True


def main():
    """Patch every icon."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--radius", type=float, default=3.5, help="blur radius in folder units")
    parser.add_argument("--strength", type=float, default=0.05, help="opacity of each layer (0 = remove)")
    parser.add_argument("--pad", type=float, default=4, help="viewBox margin added to the icons, in viewBox units")
    args = parser.parse_args()
    for path in sorted(glob.glob(os.path.join(ICONS, "*.svg"))):
        if not os.path.basename(path).startswith("_template"):
            process(path, args.radius, args.strength, args.pad)


if __name__ == "__main__":
    main()
