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
Color set (6) / Branding (3) / System view (grid 1-5 rows or carousel) / Console logo region (default, US, JP, EU) /
Game list (1-5 rows, with or without banner: 10 values). Then pick the **Imago** gamelist view.
No ifSubset is used: it did not filter in Batocera ES (all variants got merged), so every option is an include-level subset.

## Game list, top to bottom
photo banner + marquee (or rounded box with the name when the game has no marquee) > info strip
(name 2-33% | developer from 34% | year from 50%, three text shades) > grid. Name truncates with "..." (no horizontal text scroll in this ES).

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
