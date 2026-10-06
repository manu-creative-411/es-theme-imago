#!/usr/bin/env python3
"""Aplana un SVG de Inkscape para EmulationStation (NanoSVG no soporta <use>, <clipPath>, filtros ni capas ocultas).
Uso:  python3 tools/flatten_svg.py entrada.svg assets/wallpapers/<nombre>.svg
Expande los <use> en copias directas, elimina capas con display:none, clip-path y metadatos de Inkscape,
y conserva solo los degradados. Luego ejecuta  python3 tools/build_assets.py  para generar los recortes -b1/-b2."""
import sys, copy
import xml.etree.ElementTree as ET
SVG, XL = "http://www.w3.org/2000/svg", "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG); ET.register_namespace("xlink", XL)
q = lambda t: "{%s}%s" % (SVG, t)
src, dst = sys.argv[1], sys.argv[2]
root = ET.parse(src).getroot()
ids = {e.get("id"): e for e in root.iter() if e.get("id")}
skip_attr = lambda k: "inkscape" in k or "sodipodi" in k or k in ("id", "clip-path") or k.endswith("}space")
def flat(e, out):
    tag = e.tag.split("}")[-1]
    if "display:none" in (e.get("style") or "").replace(" ", ""): return
    if tag in ("namedview", "metadata", "clipPath", "defs") or "sodipodi" in e.tag or "inkscape" in e.tag: return
    if tag == "use":
        g = ET.SubElement(out, q("g"))
        g.set("transform", ((e.get("transform") or "") + " translate(%s %s)" % (e.get("x", "0"), e.get("y", "0"))).strip())
        flat(ids[e.get("{%s}href" % XL)[1:]], g); return
    n = ET.SubElement(out, q(tag))
    for k, v in e.attrib.items():
        if not skip_attr(k): n.set(k, v)
    for c in e: flat(c, n)
vb = root.get("viewBox") or "0 0 %s %s" % (root.get("width"), root.get("height"))
w, h = vb.split()[2:]
out = ET.Element(q("svg"), {"width": w, "height": h, "viewBox": vb, "version": "1.1"})
defs = ET.SubElement(out, q("defs"))
for g in root.iter(q("linearGradient")):
    g = copy.deepcopy(g)
    for el in g.iter():
        for k in list(el.attrib):
            if "inkscape" in k or "sodipodi" in k: del el.attrib[k]
    defs.append(g)
for c in root:
    if c.tag in (q("g"), q("rect"), q("circle"), q("path"), q("ellipse")): flat(c, out)
ET.indent(out); ET.ElementTree(out).write(dst, encoding="utf-8", xml_declaration=True)
print("ok:", dst)
