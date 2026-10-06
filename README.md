# es-theme-imago (working name)

EmulationStation theme for Batocera / RetroBat / Retrobox, inspired by Cocoon (Android) and the 3DS home screen.
Format version 7 (batocera-emulationstation).

## Layout
```
theme.xml                        entry point; declares the options (subsets)
_inc/colorsets/*.xml             6 palettes (variables: bg, tile, accent, text, subText, dimText, box, tone, scheme)
_inc/branding/*.xml              brand logo selection (variables only)
_inc/options/                    variable files for the 'Console logo region' option
_inc/layout/common.xml           background, brand, clock, help, tiles, console logo (top-left), menu
_inc/layout/system-grid-rows-N.xml  system view: icon grid, N rows (1..5)
_inc/layout/system-carousel.xml  system view: single-row carousel (fallback option)
_inc/layout/gamelist-N-banner.xml | gamelist-N-plain.xml   game list, N rows (1..5), with / without the photo+marquee banner
_inc/system_icons/               <system>.svg         square icon of each system (system view tiles)
_inc/system_bg/                  <system>.png|svg|jpg Carbon console art (system view; fallback for games without image)
_inc/system_logos/               console logo, see README.txt there (scheme-region > tone > generic)
assets/ui/                       white.png, round.png, corner-bl/br.png, box-<set>-h12|h15|h17.svg
assets/branding/                 retrobat.svg, batocera.svg, retrobox.svg (PLACEHOLDERS)
```

## Options (UI Settings > Theme Configuration)
Color set (6) / Branding (3) / Console logo region (default, US, JP, EU, BR) / Banner (on, off) / System view (grid 1-5 rows, carousel) /
Game list (1-5 rows). Then pick the **Imago** gamelist view.

## Banner
Only exists with 1 or 2 rows (system view and game list). On: bottom-anchored grid, info strip above it, banner above the strip with a gap.
Off, or 3-5 rows: info strip + grid, the grid vertically centred, slightly wider column spacing.
Implementation: no ifSubset (it did not filter in Batocera ES). Each option is an include-level subset; the Banner option files define
the geometry as variables (gY1..gY5, ...) and visibility flags (bVis...) that the layouts read.

## Artwork lookup (first existing file wins)
- icon (system view tile): _inc/system_icons/<system.theme>.svg
- console art (system banner; game banner when the game has no image): _inc/system_bg/<region>/<theme>.jpg > <theme>.jpg|png|svg|webp > collections/<theme>.jpg > collections/<system name>.jpg
- console logo (game list top-left, system banner): _inc/system_logos/<theme>/<tone>-<region>.svg > <region>.svg > <tone>.svg > <theme>.svg > <theme>/us.svg
  (tone = light for the light-gray set, dark otherwise; region from the option, 'default' skips it)

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
