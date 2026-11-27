# Notice - licences in this package (es-theme-imago)

This theme is a **collection of separate works under different licences**. Nothing here relicenses a third-party part.
Informational only, not legal advice; check each source before redistributing.

## 1. Own work of the theme author
Layouts and options XML, colour sets, `tools/`, `assets/ui/neon-*.png`, the wallpaper `assets/wallpapers/dark.svg` (made by the author),
`assets/icons/menu-icon-controller.svg` and `gamepad.svg` (author's controller icon), the console folder icons `_inc/system_icons/` (author's work: folder shapes, gradients and glyphs),
and the SNES help icons `_inc/help/icons/snes/`.

**Licence: CC0-1.0** (public domain dedication; chosen by the author: *the least restrictive of the licences present in the package*, and no attribution is required for these files).
To the extent possible under law, the author has waived all copyright and related rights to the files listed above.
https://creativecommons.org/publicdomain/zero/1.0/
Limit of the rule: it only applies to files that are really the author's own. A file that is an *adaptation* of a ShareAlike / NonCommercial work
(e.g. a layout copied from another theme) must keep that licence. The console glyphs drawn on the folder icons depict trademarks of their owners; the licence covers the author's drawing, not the trademarks.

## 2. Help icons - `_inc/help/`
Mixed sources (own work, Wikimedia Commons CC BY-SA 4.0, Recalbox CC BY-NC-SA). See `_inc/help/NOTICE.md`.

## 3. Menu icons, status icons and text-input images - `assets/icons/menu-icon-*.svg`, `menu-textinput*.png`, `battery-icon-*.svg`, `network-icon-*.svg`, `gun.svg`, `wheel.svg`
Taken from **es-theme-iconic** (author's fork https://github.com/manu-creative-411/es-theme-iconic), forked from **Delgan/iconic-es** (https://github.com/Delgan/iconic-es),
a port of **Siddy212/iconic-es-de** (https://github.com/Siddy212/iconic-es-de).
- Delgan/iconic-es: repository `LICENSE` is **CC0-1.0**; its README names the artists whose artwork the theme uses.
- Siddy212/iconic-es-de: repository `LICENSE` is **CC0-1.0**, but its README states **CC BY-NC-SA** ("not to be used for commercial purposes"). The two statements conflict.
- The authorship of the individual menu icons is not documented in those repositories. Until the authors confirm otherwise, treat them conservatively as **CC BY-NC-SA** (attribution, non-commercial).
- `menu-icon-controller.svg` was replaced by the author's own controller icon (see section 1).

### 3b. Loading screen artwork - `assets/splash/`
Copied from **es-theme-iconic** (`_inc/splash`, `_inc/other`; CC0-1.0, except its `_default.png`, which is not used). The distribution logos (Retrobox, Batocera, RetroBat, Knulli, Recalbox, EmuELEC) are trademarks of their owners; the licence covers only the drawing, not the marks.

## 4. Console artwork - `_inc/system_bg`, `_inc/system_logos`
Stated by the author to come from **es-theme-carbon** by fabricecaruso (https://github.com/fabricecaruso/es-theme-carbon), a fork of RetroPie/es-theme-carbon
(theme "Carbon" by **Rookervik**, based on *simple* by Nils Bonenberger).
- Licence of Carbon: **CC BY-NC-SA 4.0** (the repository README reproduces the Attribution-NonCommercial-ShareAlike text). Attribution + **non-commercial** + ShareAlike for adaptations.
- Carbon's images are in turn collected from other places (some Carbon forks credit *Viking* and *dragon57* / Launchbox *Nostalgia* for logo images), and the console logos
  are trademarks of their owners. Carbon's licence does not clear those rights.
- Some backgrounds in `_inc/system_bg/collections/` look like game artwork (e.g. *Aladdin*, *Arkanoid*) rather than Carbon console art. Confirm their origin.

## 5. Fonts - `assets/fonts/`
**Poppins**, Copyright 2014-2017 Indian Type Foundry, SIL Open Font License 1.1 (https://openfontlicense.org). Notice and licence URL are embedded in the font files and repeated in `assets/fonts/FONT-LICENSE.txt`.

## 6. Obligations of the third-party parts and how this package meets them
| Part | Licence | Obligations | Done here |
|---|---|---|---|
| Recalbox help icons and presets (recalboxy) | CC BY-NC-SA (https://creativecommons.org/licenses/by-nc-sa/4.0/) | credit + licence link + say what was changed; non-commercial; adaptations under the same licence | credited here and in `_inc/help/NOTICE.md`; changes stated (paths, `default.xml`, `F1.svg` omitted); presets stay BY-NC-SA |
| Carbon console art (`system_bg`, `system_logos`) | CC BY-NC-SA 4.0 | same as above | credited in section 4; **if any Carbon file was altered (resized, recoloured, converted, renamed), write it here: ______** |
| Xbox / PlayStation help icons | CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/) | credit author + licence link + source link; say if changed; adaptations under BY-SA | per-file credits in `_inc/help/CREDITS-wikimedia.txt`; shipped unmodified |
| Iconic menu icons / text-input images | treated as CC BY-NC-SA (authorship undocumented) | credit + non-commercial | credited in section 3 |
| Poppins | SIL OFL 1.1 | keep copyright + licence with the fonts; do not sell the fonts alone; no modified version named "Poppins" | `assets/fonts/FONT-LICENSE.txt`; files unmodified |

Because of the NonCommercial parts, the package as a whole must not be sold or monetised. The author's own files (section 1) are CC0 and impose nothing on anyone.

## 7. Open items
- Origin of some `system_bg/collections` images (e.g. *Aladdin*, *Arkanoid*): not Carbon console art as far as can be told. Document or remove them.
- Authorship of the Iconic menu icons: replace them with own or clearly licensed icons to remove the uncertainty.
- Official `OFL.txt` text next to the fonts (optional; the notice is already in the font files).
