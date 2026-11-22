# es-theme-imago (working name)

EmulationStation theme for Batocera / RetroBat / Retrobox, inspired by Cocoon (Android) and the 3DS home screen.
Format version 7 (batocera-emulationstation).

## Layout
```
theme.xml                        entry point; declares the options (subsets)
_inc/colorsets/*.xml             6 palettes (variables: bg, tile, accent, text, subText, dimText, box, tone, scheme)
_inc/branding/*.xml              brand logo selection (variables only)
_inc/options/                    option variable files (logoRegion, banner geometry, wallpaper, tiles)
_inc/layout/common.xml           background, brand, clock, help, tiles, console logo (top-left), menu
_inc/layout/system-grid-rows-N.xml  system view: icon grid, N rows (1..5); tile size = sC<N>/sH<N> in _inc/options/banner-*.xml
_inc/layout/system-carousel.xml  system view: single-row carousel (fallback option)
_inc/layout/gamelist-rows-N.xml  game list, N rows (1..5), with the photo+marquee banner (1-2 rows)
_inc/layout/gamelist-common.xml  base of the Basic/Detailed views: background, brand, clock, console logo, help
_inc/layout/gamelist-basic.xml   custom view "Imago Basic": list in a centred panel + developer/year under it
_inc/layout/gamelist-detailed.xml  custom view "Imago Detailed": game info on the left, list on the right
assets/list/                     list panels from es-theme-iconic (7 rows, dark/light); "centered-*" = shifted 490 px for Imago Basic
_inc/system_icons/               <system>.svg         square icon of each system (system view tiles)
_inc/system_bg/                  <system>.png|svg|jpg Carbon console art (system view; fallback for games without image)
_inc/system_logos/               console logo, ordered <path> chain (see README.txt there)
assets/ui/                       white.png, round.png, corner-bl/br.png, box-<set>-h12|h15|h17.svg
assets/branding/                 retrobat.svg, batocera.svg, retrobox.svg (PLACEHOLDERS)
```

## Options (UI Settings > Theme Configuration)
Color set (6) / Help icons (9) / Branding (3) / Console logo region (Europe [default], USA, Japan) / Banner (on, off) / System view (grid 1-5 rows, carousel) /
Game list (1-5 rows). Then pick the **Imago**, **Imago Basic** or **Imago Detailed** gamelist view (UI Settings > Game List > view style).

## Banner
Only exists with 1 or 2 rows (system view and game list). On: bottom-anchored grid, info strip above it, banner above the strip with a gap.
Off, or 3-5 rows: info strip + grid, the grid vertically centred, slightly wider column spacing.
Implementation: no ifSubset (it did not filter in Batocera ES). Each option is an include-level subset; the Banner option files define
the geometry as variables (gY1..gY5, ...) and visibility flags (bVis...) that the layouts read.

## Artwork lookup
- icon: _inc/system_icons/<system.theme>.svg
- console art: _inc/system_bg/<system.theme>.jpg
- console logo: ordered list of `<path>` in the layouts (last existing file wins), same logic as es-theme-iconic. Variables `logoRegion`
  (eu/us/jp, option "Console logo region") and `logoColorScheme` (dark/light, set per colour set). Full order in `_inc/system_logos/README.txt`.
  No generated folders. NOTE: `firstfile()` only works inside expressions (`<visible>`), never as a `<path>` value.
- `python3 tools/build_assets.py` only copies system_bg/collections, creates icon aliases and the wallpaper crops.

## Known limits / to verify
- System grid: in Batocera ES the system-view grid is `<imagegrid name="imagegrid">` (confirmed in es-theme-tiled, systemview/grid.xml;
  `systemgrid` and `systemcarousel` do NOT work: the latter logs "mismatched theme type ... expected carousel").
  Still unverified: tile image source (assumed `<image name="logo">`), `autoLayout`/`scrollDirection` support in this view.
  Carousel stays as fallback.
- Photo crop: `md_image` uses minSize 1x0.5 centred; overflow below 50% is covered by `e_overflow`; the bottom corners
  (36px @1080p) are bg-coloured masks (corner-bl/br.png).
- Console logo: `assets/systems/<system.theme>.svg`, top-left over the photo; the header text is hidden.
- Background is a single flat colour (`bg` in each colorset). Brand logo moved to the top-right.
- "developer - year" is built from three elements (developer, "-", year); a missing developer leaves a dangling dash.
- md_image / md_marquee inside a custom view inheriting `grid`, `displayName` on subsets and the 1-4 row geometry
  must be checked on a real Batocera/RetroBat build (F5 reloads the theme; use `--windowed`).
- No fonts are bundled (default ES font). Add a TTF and a `<fontPath>` if wanted.
- Logos in assets/branding are placeholders; use the official artwork you are allowed to use.

Renaming the theme = renaming the folder; all paths use `${themePath}` or are relative.

## Wallpapers (assets/wallpapers/)
- `<name>.svg` 16:9 (p. ej. 1280x720) = fondo a pantalla completa, capa `e_wallpaper` (z 1, sobre el color plano `bg`). **Debe estar aplanado** (sin `<use>`, `<clipPath>`, filtros ni capas ocultas: NanoSVG no los soporta). Si lo exportas de Inkscape: `python3 tools/flatten_svg.py original.svg assets/wallpapers/<nombre>.svg`.
- Cada colorset elige el suyo en `_inc/colorsets/*.xml` (`wallpaper`, `wallpaperB1`, `wallpaperB2`). Hoy: Black -> `dark.svg`; el resto -> `none.png` (transparente).
- `<name>-b1.svg` / `-b2.svg` los genera `python3 tools/build_assets.py`: recorte de la zona bajo el banner (1 y 2 filas) para que el fondo sea continuo
  bajo la foto de consola (capa `e_overflow_wp`, z 31.5). Si cambias `bH1/bH2` en `banner-on.xml`, actualiza `BH` en el script.
- Opcion de tema `Wallpaper: on/off` (off = usa `none.png`).
- Para anadir otro: copia `assets/wallpapers/<name>.svg`, ejecuta el script y apunta las 3 variables del colorset a `<name>.svg`, `<name>-b1.svg`, `<name>-b2.svg`.

## Iconos de sistema (_inc/system_icons/)
- Se editan directamente estos SVG (Inkscape). Sin capas multiply ni modos de mezcla (ES/NanoSVG no los soporta): la carpeta son dos formas
  (pestana + cuerpo) con degradado ya tintado, y encima los glifos.
- Plantillas: `_template.svg` (carpeta con pestana) y `_template_app.svg` (carpeta de apps). Cada una trae **13 grupos de color** (capas de Inkscape,
  una por combo) con su nombre en ingles; solo uno esta visible y los demas llevan `display:none`.
  Para elegir color: panel Capas (Ctrl+Shift+L), muestra el combo que quieras y **borra los demas** antes de guardar el icono.
  Cada grupo lleva en `desc` (Propiedades del objeto) los sistemas que ya usan ese color.
  Combos: Vivid Red #ff3b3b, Vivid Orange #ff8a2b, Amber Yellow #ffc61a, Spring Green #22e066, Azure Blue #1fa0ff, Royal Blue #1f7bff,
  Navy Blue #305591, Electric Violet #8347ff, Neon Magenta #d924ff, Slate Gray #6b7a88, Dusk Blue #47617a, Silver #d3dce6, Pure Magenta #ff00ff (marcador).
- Degradado de cada combo: gris `#e5e5e5 -> #a8a8a8` multiplicado por el color base (arriba mas claro, abajo mas oscuro).

## Selector neon y tiles (assets/ui/neon.png, _inc/options/tiles.xml)
- Los tiles ya no tienen placa: icono/caratula a todo el ancho o alto del tile (`imageSizeMode=maxSize`). El seleccionado lleva un contorno neon que rodea
  solo la imagen (`selectionMode=image`), tenido con `${neon}` (variable de cada color set). Si tu ES ignora `selectionMode`, el neon rodeara el tile entero.
- `neon.png` es un nine-patch (nucleo + resplandor solo hacia fuera). Se regenera con `python3 tools/make_neon.py [BAND] [STROKE]`;
  `BAND` debe ser igual a `tPad` (px entre la imagen y el borde del tile = `backgroundCornerSize`).
- `tiles.xml`: `tPad` (20), `tZoom` (1.06, zoom del seleccionado) y `gPad` (holgura izq/arriba/dcha/abajo del grid, relativa a la pantalla).
  Si el zoom o el neon se cortan en los bordes del grid, sube `gPad`; si quieres iconos mas grandes, baja `tPad` (y regenera el PNG con el mismo BAND).
- El grid ocupa el 100 % del ancho (`pos 0`, `size 1`) y, en vertical, `gPad` extra arriba y abajo (la zona util es la de antes). Geometria en `banner-on/off.xml`
  (`gY/gH/gC/gM`). Con banner: 1 fila = 6 columnas, 2 filas = 7.

## Fonts (assets/fonts/, _inc/options/fonts.xml)
Poppins, all 18 files. Elements never hard-code a file: they use a **role variable** from `_inc/options/fonts.xml`, so a weight can be changed in one place.

| Role variable | Weight | Used by |
|---|---|---|
| `fontMenuItem` | Light | main menu selectable entries (`menutext`) |
| `fontMenuGroup` | Medium | menu group names (`menugroup`, coloured with `${neon}`) |
| `fontMenuTitle` | Medium | menu title (`menutitle`) |
| `fontMenuSmall` | Regular | menu small text and footer (`menutextsmall`, `menufooter`) |
| `fontTitle` | Bold | console and game titles: info strip, name over the banner box, carousel title |
| `fontInfo` | Regular | maker, developer, year, game count |
| `fontUI` | Medium | clock, help bar |

Raw weights (`fontThin` ... `fontBlack`) are also defined for new elements. Poppins is much wider than the default ES font, so sizes were reduced
(titles 0.030, info 0.024, help 0.026, banner box name 0.040 via `bFS1/bFS2` in `banner-on/off.xml`, menu 0.021-0.036). Poppins is released under the SIL Open Font License:
keep its license text if you redistribute the theme.

## Menu icons (assets/icons/)
The 14 menu icons come from es-theme-iconic (white SVG, 24x24; ES tints them with the menu text colour, so they work on dark and light colour sets),
wired in the `menu` view of `_inc/layout/common.xml` (`menuIcons` + `menuTextEdit`). `menu-icon-controller.svg` and `gamepad.svg` are the custom controller icon
(glyph scaled to 22/24 of the box so it matches the others). Use that same icon for anything related to controllers/gamepads
(`gamepad.svg` is not used by a layout yet: it is reserved for a controller-activity indicator).

## Help icons (_inc/help/, option "Help icons")
Same option and logic as es-theme-recalboxy (subset `helpicons`): Default (Batocera) / Xbox / PlayStation / SNES / Generic 4, 6 and 8 buttons / SNES alt / Xbox One / Arcade.
`default.xml` is an empty preset (Batocera's own icons, tinted with the help colour). The others override the `helpsystem name="help"` icons and are included in `theme.xml`
AFTER `common.xml`. Xbox, PlayStation and SNES map the *physical position* of Batocera's buttons (A = east, B = south, X = north, Y = west) and are full-colour icons
(`iconColor` FFFFFFFF, not tinted); the generic sets keep the theme tint (`${subText}`). Font and size of the help bar stay in `common.xml`.

**Licence:** the package mixes licences (own work, CC BY-SA 4.0 from Wikimedia Commons, CC BY-NC-SA from Recalbox/Carbon/Iconic). Read `NOTICE.md`, `_inc/help/NOTICE.md` and `_inc/help/CREDITS-wikimedia.txt` before redistributing: the package is non-commercial because of its third-party parts.
