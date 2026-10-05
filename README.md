# es-theme-imago (working name)

EmulationStation theme for Batocera / RetroBat / Retrobox, inspired by Cocoon (Android) and the 3DS home screen.
Format version 7 (batocera-emulationstation).

## Layout
```
theme.xml                      entry point; declares the options (subsets)
_inc/colorsets/*.xml           6 colour palettes (variables only)
_inc/branding/*.xml            brand logo selection (variables only)
_inc/layout/common.xml         background, brand logo, clock, help bar, tiles, menu
_inc/layout/system-view.xml    system view (icon carousel)
_inc/layout/gamelist-rows-N.xml  game list with N rows (1..5)
assets/ui/                     white.png (flat fills), round.png (9-patch, 16px corners)
assets/branding/               retrobat.svg, batocera.svg, retrobox.svg (PLACEHOLDERS)
assets/systems/                <system>.svg, one per system (drawn by hand)
```

## Options (UI Settings > Theme Configuration)
Color set (6) / Branding (3) / Game rows (1-5). Then pick the **Imago** gamelist view.

## System icons
Name them after the system's `<theme>` tag in es_systems.cfg: `assets/systems/snes.svg`, `assets/systems/psx.svg`...
If a file is missing, the system name is shown as text.

## Known limits / to verify
- System view is a single-row carousel: stock ES has no multi-row grid for systems.
- Marquee vs. info box: XML cannot hide the box when a marquee exists. The marquee is drawn over the box.
- "developer - year" is built from three elements (developer, "-", year); a missing developer leaves a dangling dash.
- md_image / md_marquee inside a custom view inheriting `grid`, `displayName` on subsets and the 1-4 row geometry
  must be checked on a real Batocera/RetroBat build (F5 reloads the theme; use `--windowed`).
- No fonts are bundled (default ES font). Add a TTF and a `<fontPath>` if wanted.
- Logos in assets/branding are placeholders; use the official artwork you are allowed to use.

Renaming the theme = renaming the folder; all paths use `${themePath}` or are relative.
