# Masthead Assets

Real mastheads are the default newspaper identity assets. Each country keeps five pixelized real masthead choices. `scripts/render_newspaper.py` randomly selects one on every run and recolors it so it matches the selected newspaper paper/ink colors, not the raw event image palette.

## Current Assets

- France: `Le Petit Journal`
  - Choices: `assets/newspaper/france/real-mastheads/le-petit-journal-choice-01-archive-clean.png` through `choice-05-boxed-print.png`
  - Source: Wikimedia Commons, `Le Petit Journal Header`
- United States: `USA Today`
  - Choices: `assets/newspaper/united-states/real-mastheads/usa-today-choice-01-archive-clean.png` through `choice-05-boxed-print.png`
  - Source: Wikimedia Commons, `2012 USA Today logo`
- Japan: `The Asahi Shimbun`
  - Choices: `assets/newspaper/japan/real-mastheads/asahi-shimbun-choice-01-archive-clean.png` through `choice-05-boxed-print.png`
  - Source: Wikimedia Commons, `The Asahi Shimbun logo`
- China: `People's Daily`
  - Choices: `assets/newspaper/china/real-mastheads/peoples-daily-choice-01-archive-clean.png` through `choice-05-boxed-print.png`
  - Source: Wikimedia Commons, `People's Daily logo`
- Hong Kong: `Apple Daily`
  - Choices: `assets/newspaper/hong-kong/real-mastheads/apple-daily-choice-01-archive-clean.png` through `choice-05-boxed-print.png`
  - Source: Wikimedia Commons, `Apple Daily Title`
- Korea: `Chosun Ilbo`
  - Choices: `assets/newspaper/korea/real-mastheads/chosun-ilbo-choice-01-archive-clean.png` through `choice-05-boxed-print.png`
  - Source: Wikimedia Commons, `Chosun Ilbo Logo`

## Update Rule

When adding a better scan or logo asset:

1. Save source files under `assets/newspaper/<style-key>/source-scans/`.
2. Convert with `scripts/pixelize_masthead_asset.py`.
3. Place output under `real-mastheads/` for default assets or `historical-mastheads/` for extra scan crops.
4. Run `scripts/generate_real_mastheads.py` to refresh the five default choices when source scans change.
5. Run `scripts/generate_newspaper_assets.py` so `layout-templates.json` discovers the five choices.

Renderer behavior:

- Five `real_masthead_assets` are used before generated fictional fallback mastheads.
- The renderer randomly chooses one asset unless `masthead_index`, `masthead_seed`, or `masthead_asset` is set.
- Mastheads are recolored at paste time to match newspaper ink and paper, with the surrounding slot cleared first so scan/grid lines do not cut through the logo.
- Do not paste raw RGB logo colors unless the user asks for faithful logo color reproduction.
