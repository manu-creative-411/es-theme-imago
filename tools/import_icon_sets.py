#!/usr/bin/env python3
"""Build the alternative system icon sets (_inc/icons_iisu, _inc/icons_alekfull) from the upstream repos.

Only consoles, handhelds, computers and arcade platforms are imported (see SYSTEMS); publishers,
franchises, genres, collections, ports and emulators are skipped. Each icon is written as
<es system theme name>.jpg, so the layouts can look it up with ${system.theme}.

Sources (clone them first, both are artwork by their authors, see NOTICE.md):
  iiSU:     https://github.com/VictorUnlocked/iisu-interpreted-es-de   (_inc/systems/artwork/*.webp)
  Alekfull: https://github.com/fagnerpc/Alekfull-NX                    (assets/logos/*.jpg)

Usage: python3 tools/import_icon_sets.py --iisu PATH --alekfull PATH [--size 400] [--quality 88]
Requires Pillow.
"""
import argparse
import os
import shutil

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SYSTEMS = """
nes famicom fds snes sfc satellaview sufami n64 n64dd gamecube gc wii wiiu switch gb gbc gba nds
3ds virtualboy pokemini gameandwatch
sg1000 mastersystem mark3 megadrive genesis segacd megacd sega32x saturn dreamcast gamegear
psx ps2 ps3 ps4 psp psvita xbox xbox360 xboxone windows dos
atari2600 atari5200 atari7800 atari800 atarist atarijaguar atarijaguarcd atarilynx xegs
pcengine pcenginecd tg16 tg16cd supergrafx pcfx pc88 pc98 neogeo neogeocd ngp ngpc
wswan wswanc 3do cdi amigacd32 amigacdtv colecovision intellivision vectrex odyssey2 videopac
channelf supervision gamecom gamate megaduck gp32 gmaster arduboy pico8 tic80 lowresnx uzebox
vsmile scv pv1000 supracan creativision astrocade arcadia ngage multivision amstradgx4000
amiga amiga500 amiga600 amiga1000 amiga1200 amiga3000 amiga4000 amstradcpc apple2 apple2gs atom
bbcmicro c64 c128 c16 vic20 cplus4 pet coco dragon32 electron fm7 fmtowns macintosh msx msx1 msx2
msx2plus msxturbor oric samcoupe spectravideo thomson to8 ti99 tutor x1 x68000 zx81 zxspectrum
zxnext adam archimedes trs80
arcade mame fbneo fba naomi naomi2 naomigd atomiswave model2 model3 hikaru lindbergh triforce
chihiro cps1 cps2 cps3 pgm daphne teknoparrot typex segastv
""".split()

# ES system name -> other names the same system has in the source repos
ALIASES = {
    "3ds": ["n3ds"], "cdi": ["cdimono1"], "amigacdtv": ["cdtv"], "xegs": ["atarixe"],
    "sg1000": ["sg-1000"], "tg16cd": ["tg-cd"], "wswan": ["wonderswan"],
    "wswanc": ["wonderswancolor"], "creativision": ["crvision"], "trs80": ["trs-80"],
    "gamecube": ["gc"], "gc": ["gamecube"], "cplus4": ["plus4"], "typex": ["type-x"],
    "amstradgx4000": ["gx4000"], "segastv": ["stv"], "msx2plus": ["msx2+"],
    "famicom": ["nes"], "sfc": ["snes"], "genesis": ["megadrive"], "megadrive": ["genesis"],
    "megacd": ["segacd"], "segacd": ["megacd"],
}

SOURCES = {  # set name -> (sub folder in the clone, extension)
    "iisu": (os.path.join("_inc", "systems", "artwork"), ".webp"),
    "alekfull": (os.path.join("assets", "logos"), ".jpg"),
}


def find_source(folder, ext, name):
    """Return the path of the source image for an ES system name, or None."""
    for candidate in [name] + ALIASES.get(name, []):
        path = os.path.join(folder, candidate + ext)
        if os.path.isfile(path):
            return path
    return None


def import_set(label, clone, size, quality):
    """Write _inc/icons_<label>/<system>.jpg for every wanted system the source has."""
    sub, ext = SOURCES[label]
    out_dir = os.path.join(ROOT, "_inc", "icons_" + label)
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir)
    done, missing = 0, []
    for name in SYSTEMS:
        src = find_source(os.path.join(clone, sub), ext, name)
        if src is None:
            missing.append(name)
            continue
        image = Image.open(src).convert("RGB")
        if max(image.size) > size:
            image = image.resize((size, size), Image.LANCZOS)
        image.save(os.path.join(out_dir, name + ".jpg"), quality=quality, optimize=True)
        done += 1
    print(f"{label}: {done} icons written, {len(missing)} systems without one")


def main():
    """Command line entry point."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", maxsplit=1)[0])
    parser.add_argument("--iisu", help="clone of iisu-interpreted-es-de")
    parser.add_argument("--alekfull", help="clone of Alekfull-NX")
    parser.add_argument("--size", type=int, default=400, help="max side in px (default 400)")
    parser.add_argument("--quality", type=int, default=88, help="JPEG quality (default 88)")
    args = parser.parse_args()
    for label in ("iisu", "alekfull"):
        clone = getattr(args, label)
        if clone:
            import_set(label, clone, args.size, args.quality)


if __name__ == "__main__":
    main()
