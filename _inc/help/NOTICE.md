# Notice - help icons (`_inc/help/`)

This folder mixes works from **different sources and licences**. They are separate works: each part keeps its own licence.

| Part | Files | Source | Licence |
|---|---|---|---|
| SNES face buttons | `icons/snes/*` | Own work of the theme author | Author's licence for own work (see root `NOTICE.md`) |
| Xbox set | `icons/xbox/*` | Wikimedia Commons (mostly by **VictorPines**) | **CC BY-SA 4.0** (a few files are public domain, e.g. *Xbox Menu button*). The file page on Commons is authoritative. |
| PlayStation set | `icons/playstation/*` | Wikimedia Commons (mostly by **VictorPines**) | **CC BY-SA 4.0** (check each file page on Commons) |
| Xbox One, SNES alt, Arcade | `icons/xboxone/*`, `icons/snesalt/*`, `icons/arcade/*` (PNG) | Recalbox (*recalbox-multi*), through es-theme-recalboxy | **CC BY-NC-SA** (non-commercial) |
| Generic buttons | `icons/6buttons_*`, `8buttons_*`, `buttons_*`, `button_*`, `dpad_*`, `analog_*` (SVG) | Recalbox (*recalbox-multi*), through es-theme-recalboxy | **CC BY-NC-SA** (non-commercial) |
| Presets | `*.xml` | es-theme-recalboxy (https://github.com/manu-creative-411/es-theme-recalboxy), derived from ES-DE *Slate* / recalbox-multi | **CC BY-NC-SA** |

Verified on Wikimedia Commons (sample): Xbox Back button, Xbox button X, Xbox A/X/Y (B+W), Xbox Share button, Xbox Left stick button -> CC BY-SA 4.0;
Xbox Menu button -> public domain; PlayStation Down / Directional / R1 / R2 / R3 / L2 / S buttons -> CC BY-SA 4.0 (author VictorPines).

## What this means
- **Attribution** is required for all of it (this notice provides it): *VictorPines, Wikimedia Commons, CC BY-SA 4.0* for the Xbox/PlayStation sets; *Recalbox / es-theme-recalboxy, CC BY-NC-SA* for the rest.
- **Non-commercial only** for the Recalbox-derived part. Because it is in this package, do not sell or monetise the package.
- **ShareAlike:** if you *modify* a CC BY-SA / CC BY-NC-SA icon, your modified copy must carry the same (or a compatible) licence. CC BY-SA 4.0 and CC BY-NC-SA 4.0 are not
  interchangeable, so the Xbox/PlayStation icons are shipped **unmodified** here. Keep them unmodified, or replace them with your own.
- Presets: recalboxy's, with one change: icon paths adapted from `${themePath}/help/icons/...` to `${themePath}/_inc/help/icons/...`. `default.xml` was added (empty preset = Batocera's own icons).
  `icons/F1.svg` of recalboxy was not copied.
- Replacing an icon: delete the file and drop yours in its place; the preset falls back to Batocera's icon when a file is missing.
- Console / controller names and logos are trademarks of their owners; the icons are used only to identify the buttons.
