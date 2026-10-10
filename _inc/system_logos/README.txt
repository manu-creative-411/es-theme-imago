Console logos (system view banner + top-left of the game list). Same logic as es-theme-iconic.

The layouts list several <path> elements, from LOWEST to HIGHEST priority; the LAST one whose file exists wins.
Variables: logoRegion = eu (default) | us | jp   (option "Console logo region")
           logoColorScheme = dark | light        (set by the colour set)

  1  <system>.svg                          generic
  2  <system>-<region>.svg                 generic, regional
  3  <system>/jp.svg
  4  <system>/<scheme>-jp.svg
  5  <system>/us.svg
  6  <system>/<scheme>-us.svg
  7  <system>/eu.svg
  8  <system>/<scheme>-eu.svg              (3-8 = fallback chain jp < us < eu, whatever the chosen region is)
  9  <system>/<scheme>.svg
 10  <system>/<region>.svg
 11  <system>/<scheme>-<region>.svg        most specific: chosen scheme AND chosen region

No generated folders: just drop the files in place. Missing files are skipped.
