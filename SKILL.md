---
name: pixel-belle-epoque
description: Create source-grounded Belle Epoque pixel newspaper front pages from this repository's six era definitions. Use when the user invokes pixel_belle_epoque or asks for pixel art from a country plus date for France, the United States, Japan, China, Hong Kong, or Korea, with historical date research, era vibe, 20+ color palette, parallel sprite generation using pixel-art-creator, a large lead image, country-specific pixel newspaper layout, period advertising sprites, and final newspaper compositing.
---

# Pixel Belle Epoque

## Overview

Turn a country plus date into a historically anchored Belle Epoque pixel-art newspaper front page. The skill researches a memorable event from that country's defined Belle Epoque, generates a rich lead image as an internal frozen component, creates a country-specific pixel newspaper around it, delegates scene sprites and newspaper/advertising sprites to parallel workers, then composites the final newspaper artifact.

Invoking this skill is a request for the full from-zero newspaper workflow described here. Use `pixel-art-creator` as the drawing skill for the lead image, scene sprites, newspaper frame, text panels, and advertising sprites.

## Invocation Contract

The user should only need to provide this skill plus a country/region and date, for example:

```text
Use $pixel-belle-epoque for France on July 1.
```

Do not make the user specify canvas size, worker count, sprite count, output path, watermark, research behavior, or palette behavior unless they want to override the defaults. Treat those details as this skill's responsibility.

Default full-scale behavior:

- Search the web for the date/event anchor.
- Use the repository's six Belle Epoque definitions.
- Use a 1920x1080 lead image unless tool limits require 1600x900.
- Create 12-20 lead-image sprites and 6-10 newspaper advertising sprites, distributed across parallel worker agents.
- Choose morning/day/dusk/night palette from event + vibe.
- Add the lead-image watermark, then embed the lead image into a country-specific pixel newspaper front page.
- Write outputs under `output/pixel-belle-epoque/<country>-<date-or-monthday>-<event-slug>/`.

For quick tests, accept short user overrides like "small test", "dry run", "6 sprites", or "no agents"; otherwise run the default full workflow.

## Project Anchors

Use the local project files as source of truth:

- `six-belle-epoques/*.md`: canonical era definitions.
- - - `references/era-index.md`: quick pixel-specific era, vibe, and palette map.
- `references/time-palettes.md`: morning/day/dusk/night palettes and palette-selection logic.
- `references/newspaper-styles.md`: country-specific mastheads, page styles, and advertising sprite categories.
- `references/newspaper-layout-research.md`: compact source notes for classic newspaper layout heuristics.
- `references/masthead-assets.md`: current real masthead assets and update rules.
- `references/pixel-font.md`: shared 5x7 pixel-font rules for all readable text.
- `references/final-illustration-prompts.json`: optional final GPT Image edit prompts for non-pixel commercial-illustration variants.
- `assets/pixel-font-5x7.json`: canonical glyph source for watermarks, signs, posters, and labels.
- `assets/newspaper/layout-templates.json`: country slot grids, five real masthead choices, static dividers, badges, and emergency fallback ad assets.
- `assets/newspaper/<style-key>/*.png`: reusable pixel mastheads, divider rules, special badges, and emergency fallback advertising panels.
- `assets/newspaper/<style-key>/real-mastheads/*.png`: default real newspaper masthead/logo assets, pixelized and recolored at render time.
- `assets/newspaper/<style-key>/historical-mastheads/*.png`: optional pixelized masthead crops made from historical scans or user-provided licensed images.
- `scripts/pixelize_masthead_asset.py`: helper for cropping, background removal, and pixelization of masthead scan assets.
- `scripts/compose_manifest.py`: helper for compositing exported PNG sprites over a background.
- `scripts/render_newspaper.py`: helper for rendering the final newspaper front page.

If `pixel-art-creator` is not already loaded, read `${CODEX_HOME:-$HOME/.codex}/skills/pixel-art-creator/SKILL.md` before drawing.

## Workflow

1. Parse the user's country and date.
   - Accept country names, region names, or aliases: France, United States/USA/America, Japan, China/Mainland China, Hong Kong, Korea/South Korea.
   - Accept dates as full dates, month/day, year, or loose phrases. If the user gives month/day without a year, search across all years in the matched era. If the user gives a full date outside the era, use its month/day across the era and state the interpretation.

2. Match the country to one of the six local Belle Epoque definitions.
   - Read `references/era-index.md` first.
   - Read the matching `six-belle-epoques/*.md` when the scene needs more historical nuance.

3. Research the date anchor.
   - Browse the web for historically meaningful events on that date, in any year within the matched era.
   - Prefer official archives, museums, libraries, newspapers, sports/event archives, encyclopedia entries, and institutional histories.
   - Pick the event with the strongest visual potential, not merely the most famous event.
   - Also collect 4-10 source-grounded secondary events from the same country/era/date search. Use these as newspaper filler, side briefs, small boxed notices, and lower-column copy, not as competing lead-image subjects.
   - Expand the researched material into 6-10 paragraph-ready `newspaper_paragraphs`. Each paragraph should be 45-90 local-language words for Latin-script pages or a visually comparable amount for Japanese, Chinese, and Korean. Write them as compact newspaper paragraphs, not fragments: one paragraph can combine a secondary event, witness/street texture, civic context, weather/market detail, and why the date matters.
   - Avoid bare headline rows, phonebook-like item lists, or one-sentence filler. The renderer uses drop caps, so too many tiny paragraphs will create too many large initials.
   - Save the chosen lead item as `primary_event`, the filler items as `secondary_events` with date/year, short local-language headline, expanded note, and source URL when available, and the prose-ready body as `newspaper_paragraphs`.
   - Save a concise `research.md` and `sources.json` in the output folder.
   - If the user has not supplied an output folder, derive one from the matched country, input date, and chosen event slug.

4. Define the art direction.
   - Name one tight vibe: 5-12 words, era-specific and event-specific.
   - Select one primary time-of-day palette from `references/time-palettes.md`: `morning`, `day`, `dusk`, or `night`.
   - Use the event and vibe to choose the time palette. Use the logic in "Palette Selection Logic" below; if two palettes fit, choose a primary palette and borrow up to 6 accent colors from the secondary palette.
   - Build the final palette with at least 20 hex colors. Preserve the selected era palette's dominant colors, then tune accents for the event, weather, season, and emotional temperature.
   - Save `palette.json` with `time_of_day`, `selection_rationale`, `primary_palette`, optional `secondary_accents`, color names, hex values, and intended uses.

5. Define rich lead-image pixel sprites.
   - Target 12-20 sprites for a serious scene.
   - Include at least: date/event anchor sprites, era people, vehicles/transit, storefront/signage, consumer/media objects, street furniture, plants or weather, and at least one subtle shadow/tension motif from the era.
   - Make sprites composable: transparent background, crisp silhouette, clear size, placement intent, and no long readable real-world text.
   - Any intentionally readable text inside sprites must use the shared 5x7 pixel font from `assets/pixel-font-5x7.json`; read `references/pixel-font.md` before planning signage or labels.
   - Save `sprite-plan.json`.

6. Select and plan the newspaper.
   - Read `references/newspaper-styles.md`.
   - Read `references/newspaper-layout-research.md` if the country's layout needs more grounding.
   - Search layout references as historical newspaper scans, page images, archives, microfilm views, IIIF images, or library digitization records. Avoid relying on modern newspaper homepages, modern brand pages, or current responsive web layouts as layout references.
   - Load `assets/newspaper/layout-templates.json`; choose the matching `style_key`, divider, badge, page palette, layout family, slot grid, and advertising categories.
   - Let the renderer randomly select one of the five country `real_masthead_assets` on every run unless the user or manifest explicitly sets `masthead_index`, `masthead_asset`, or `masthead_seed` for reproducibility.
   - Use local pixelized real masthead assets under `real-mastheads/` or `historical-mastheads/` by default. Use fictional masthead assets only as emergency fallback when no real masthead asset exists.
   - Keep the newspaper's `paper_color`, `ink_color`, `accent_color`, and `muted_color` from the layout template unless the user explicitly overrides them; do not let a vivid event image palette recolor the whole paper surface.
   - Plan one local-language headline, one local-language deck, 2-4 short snippets, a caption, 6-10 expanded newspaper paragraphs, 4-8 short report-fill lines, 6-10 ad-copy lines, and 6-10 live advertising sprite briefs.
   - Write newspaper text in the country's local newspaper language/script: French for France, English for the United States, Japanese for Japan, simplified Chinese for China, traditional Chinese for Hong Kong, and Korean for Korea. The lead-image watermark remains English.
   - Use `secondary_events` from the research phase to fill the page. Convert them first into paragraph-ready `newspaper_paragraphs`; use shorter side notes, weather/market/civic lines, and tiny boxed notices only as secondary texture.
   - Report fill should read like compact front-page matter: tiny civic note, market/weather line, witness line, cultural aside, archive caption, or secondary-event note. Keep these short, but do not rely on them as the main body copy.
   - Ad-copy fill should be invented and period-plausible in the local language/script: short labels/taglines for the ad workers and for renderer fallback text. No real logos, real slogans, or long copy.
   - Advertising briefs must be generated at run time from the selected country, event, vibe, season, newspaper style, and local commercial motifs. Do not reuse the same default ad list mechanically.
   - Advertising briefs should match the country's Belle Epoque economy and the event's date: period transport, theatres, cafés, patent medicines, department stores, cameras, bicycles, shipping lines, schoolbooks, bank notices, telecom/electrical services, or other plausible local commerce depending on country/era. Avoid generic modern coupon language.
   - Treat static newspaper assets as the house style. The masthead, divider, badge, and layout ratios come from the template. Static ad assets are emergency fallback only, not the default path.
   - The newspaper is the final artifact. The lead image remains dominant and should align to the newspaper's image frame.
   - Save `newspaper-plan.json`.

7. Launch parallel workers.
   - Spawn 4-8 worker agents, each responsible for a disjoint batch of sprites.
   - Tell every worker they are not alone in the codebase, must not revert others' work, and must write only inside their assigned `sprites/<worker-id>/` folder.
   - At minimum, split work into lead-image scene sprite workers plus one worker per advertising sprite brief. For full-scale runs, also use a worker for newspaper frame/text ornaments.
   - Advertising workers are one-brief-per-agent: one agent owns exactly one ad sprite and writes only inside `ads/<ad-slug>/` or its assigned folder. Full-scale runs should spawn 6-10 ad workers unless the user asks for a small test.
   - Each worker must use `pixel-art-creator` plus the shared vibe, newspaper style, and palette.
   - Require each worker to return: changed files, sprite PNG paths, dimensions, anchor points, placement recommendations, and any failed sprites.

8. Generate the large lead-image background in the main thread.
   - Use `pixel-art-creator` plus the same vibe and palette.
   - Recommended canvas: 1920x1080 or 1600x900 RGB/indexed-style pixel art. Use smaller only when tool limits require it.
   - The background should be a full setting, not an empty stage: skyline, street/harbor/interior depth, lighting, architectural era cues, and blank zones reserved for sprites.
   - Use the shared 5x7 pixel font for any readable background signage, posters, station labels, or date markers.
   - Save `background.png`.

9. Composite and harmonize the lead image.
   - Gather worker sprites, inspect them, and reject or regenerate sprites that break the palette, read as anachronistic, have opaque unwanted backgrounds, or duplicate another sprite.
   - Build `composition-manifest.json` with the background path and every sprite path, position, size, anchor, and z-order.
   - Add a small pixel-text watermark in a random corner. Text must be English: `La Belle Epoque - <Place Name> - <Date>`.
   - Use `scripts/compose_manifest.py` when exported PNG files are available.
   - Run a visual pass. Adjust positions, scale, contrast, and z-order until the lead image reads as one scene.
   - Save this internal lead image as `final.png` and `preview.png`.

10. Render the newspaper front page.
   - Gather newspaper advertising sprites and any frame/text ornament sprites.
   - Build `newspaper-manifest.json` with `source_image: final.png`, country/place/date/event, `style_key`, optional `language`, optional `font_key`, optional `masthead_index`, `masthead_seed`, or `masthead_asset`, local-language headline, deck, snippets, `reports`, `secondary_events`, `newspaper_paragraphs`, caption, generated ad paths with optional labels/copy/aspect, `ad_copy`, `ad_count`, `use_static_ads: false`, and paper palette only when it should override the template.
   - Let `render_newspaper.py` load `assets/newspaper/layout-templates.json` and paste a randomly selected country masthead, divider, and badge. Include generated ad paths from the advertising workers. Use static ads only for explicit fallback/debug runs.
   - The renderer must fuse real mastheads into the printed page: sample the already-rendered paper color under the masthead slot, recolor the masthead ink against that sampled color, and avoid visible rectangular scan/background patches.
   - Use a compact front-page canvas when the lead image is too small: reduce the internal newspaper layout size, then use nearest-neighbor `output_scale` for the deliverable so the masthead, lead image, and text remain crisp instead of over-compressed.
   - Ad sprites must render as floating ad illustrations inside dense printed matter, not centered images inside large empty cards. The renderer reads each ad sprite's dimensions/aspect, pastes generated ad PNGs directly as large floats, then wraps local-language newspaper body text around the actual pasted sprite bounds.
   - Ad sprites should sit left-aligned within their local sub-column or sub-panel, with a small gutter between the sprite and wrapped text. Do not center an ad in a large reserved slot unless the ad itself fills the slot.
   - Text must not overlap. Prefer stopping a column early over forcing another paragraph into a crowded slot. In dense lower-body flow, use collision-aware line placement, one text segment per row, no narrow fragments around ads, and a bottom safety band.
   - Put the selected year/date in a visible front-page badge near the section title or lead image. Use a complete English date with year in `display_date` or `date_label` whenever the user only supplied month/day.
   - Add a visibly colored `La Belle Epoque` watermark on the newspaper page, not only inside the lead image. Treat it as a front-page label: palette-colored, prominent, crisp, and placed where it does not cover lead-scene focal subjects.
   - The layout should feel like a newspaper page scan: use uneven columns, side notes, lower rails, boxed notices, staggered ad floats, and text flowing around images instead of a centered hero plus regular card grid.
   - For `society_broadsheet` templates, follow the compact reference structure: giant real masthead across the top, narrow issue line, a centered `BREAKING NEWS` section title, left story column, right lead image, small caption, and a dense lower body where ad floats interrupt multi-column text.
   - Keep the outer newspaper margin tight enough to avoid empty border fields. Use the template margin by default; if a manifest from older tests contains a large `margin`, the renderer may cap it unless `preserve_margin` is explicitly set.
   - Apply the renderer's final print finish before saving: first the aged-newspaper wash, then the `belle-epoque-print` retro filter. This adds subtle warm paper tint, edge wear, folds, scanline/halftone texture, tiny scratches, and slight chromatic press misregistration while preserving pixel-text readability.
   - Run `scripts/render_newspaper.py --manifest newspaper-manifest.json --out newspaper.png`.
   - Inspect for cropped text, cramped ads, off-style masthead, and lead-image framing. Iterate until the page reads as a coherent pixel newspaper.
   - Save the final deliverable as `newspaper.png`; the lead image remains available as `final.png`.

11. Optionally create a non-pixel commercial-illustration variant.
   - This is an optional final stage only. Run it when the current Codex session exposes usable image editing through the built-in `image_gen` tool or when the user explicitly confirms the fallback CLI/API path described by the installed `$imagegen` skill.
   - The model ID to use for the fallback CLI/API path is `gpt-image-2`. In Codex, the callable surface may be named `image_gen`, not `gpt-image-2`; do not fail just because no literal `gpt-image-2` tool name is visible.
   - Before running this stage, read `references/final-illustration-prompts.json` and select the prompt for the current `style_key`.
   - Treat `newspaper.png` as the edit target. Preserve the original newspaper layout and composition. The variant should restyle the rendered bitmap into the selected country's main Belle Epoque commercial-illustration aesthetic, replacing pixel-art rendering with smooth vector-like shapes and airbrush gradients.
   - Save the edited variant as `newspaper-commercial-illustration.png` in the same output folder. Do not overwrite `newspaper.png`.
   - If image editing is unavailable in the session, skip this stage quietly in execution notes or `qa.md`; the normal `newspaper.png` remains the final deliverable.

## Worker Prompt Contract

Each worker prompt should include:

```text
Use $pixel-art-creator to create the assigned transparent-background pixel sprites or newspaper components.
Country/era:
Date anchor:
Event:
Vibe:
Palette:
Newspaper style:
Assigned sprites:
Output folder:
Sprite requirements:
- Use only the shared palette or nearest colors.
- Keep crisp 1x pixel edges and transparent backgrounds.
- Avoid modern anachronisms, real logos, and long readable text.
- Use the requested local-language label/copy for advertising text. For ASCII text, use `assets/pixel-font-5x7.json`; for French accents, Japanese, Chinese, or Korean, render with the skill's country font key or a matching pixelized local script.
- For advertising sprites, use the assigned `label` and one short `copy`/`tagline`; draw a large self-contained printed ad object with product/sign art and minimal label. Do not draw a tiny product inside a large blank poster, and do not depend on the renderer to provide an outer ad frame.
- Match the requested target aspect and dimensions. A wide ad should be genuinely wide, a tall ad genuinely vertical, and a square ad close to square so the renderer can place it without cropping.
- Return file paths, dimensions, anchor point, and recommended placement.
You are not alone in the codebase. Do not edit outside your assigned folder and do not revert others' work.
```

## Newspaper Stage

The newspaper stage is part of this skill, not a separate user action. Treat the lead image as a frozen internal asset once `final.png` is composed, then build the newspaper around it.

Use `references/newspaper-styles.md`, `references/newspaper-layout-research.md`, and `assets/newspaper/layout-templates.json` together:

- real country-specific mastheads
- page tone and rules
- short headline cues
- period advertising sprite categories
- newspaper palette hints
- static masthead/divider/badge/default-ad assets
- normalized slot grids for masthead, issue line, headline, deck, lead image, caption, snippets, and ads
- page height, columns, gutters, lead-image, and ad-column ratios

Search protocol for newspaper layout:

- Query historical scans, not modern websites. Use phrases like `front page scan`, `newspaper archive`, `page image`, `microfilm`, `IIIF`, `masthead crop`, `digitized newspaper`, and target years inside the country's era.
- Favor libraries, national archives, newspaper archives, university collections, Wikimedia Commons, LOC/Chronicling America, Gallica/BnF, NDL/Japan archives, HKPL/SCMP archive descriptions, KCI/Korean studies records, and other scan-bearing sources.
- Do not infer layout from a modern newspaper homepage, current marketing page, or mobile web article page.
- Save the chosen layout reference URLs in `sources.json` and summarize what came from actual scans versus secondary descriptions.

The built-in style keys are `france`, `united-states`, `japan`, `china`, `hong-kong`, and `korea`.

Country layout translations:

- France: illustrated popular half-format; tall decorative masthead, airy lead image, Art Nouveau rules, lower columns with poster-like ads.
- United States: modular color-section front; bold boxes, color chips, ticker/sidebar feel, ad-heavy lower rail.
- Japan: compact evening grid; orderly column rhythm, small accent tabs, abstract vertical glyph texture, city-pop ad panels.
- China: civic grid announcement; sturdy title rule, red accent bars, practical columns, boxed notices, development-era ad rail.
- Hong Kong: dense commercial color tabloid; large lead, compressed boxes, neon ad strip, harbor/finance ticker energy.
- Korea: clean developmental daily; orderly masthead, civic/sport sidebars, Olympic color dots, bank/electronics ad rhythm.

Advertising sprites should be substantial pixel product/sign illustrations that sit directly inside text flow, not modern banners and not images centered inside renderer-made blank frames. Use invented brands and short labels only. No real logos. No long readable text. Use abstract local glyph blocks for ambience, but any deliberately readable text must use the shared 5x7 font.

Ad planning:

- Create 6-10 ad briefs per full run after the event/vibe/palette is known; use 3-4 only for explicit small tests.
- Make every ad brief specific to the country, event mood, and newspaper style: e.g. a Paris theatre scent card, a USA mall electronics coupon, a Ginza record-shop tile, a reform-era appliance notice, a Hong Kong ferry/cinema block, or a Seoul bank/TV-set ad.
- Each ad brief needs `slug`, short local-language `label`, one short local-language `copy` or `tagline`, product/service category, visual icon idea, color emphasis, target aspect (`square`, `wide`, or `tall`), target dimensions, and one-line placement intent. Prefer large readable sprites: about 360x140 or 420x160 for wide ads, 220x220 or 260x220 for square ads, and 180x320 or 220x340 for tall ads.
- The ad sprite is the whole printed ad object. It may include its own tiny rule, border, product art, price mark, or label if historically plausible, but it should not rely on the renderer to supply a surrounding blank card.
- Spawn one worker agent for each ad brief. The worker must use `pixel-art-creator`, produce a transparent-background PNG panel/sprite, and return path, dimensions, anchor, and notes.
- Generated ads should be passed to the renderer as `ads`; static `default_ad_assets` are emergency fallback only.
- Do not leave large blank ad rectangles. The renderer pastes generated ad sprites left-aligned inside their assigned local area and wraps body text around their actual visible bounds with a small gutter; if the run has too few generated ads, spawn more ad workers rather than padding with empty boxes.

Text filling, local language, and font weights:

- Use the shared 5x7 pixel font for ASCII/English newspaper text.
- For local scripts, `render_newspaper.py` pixelizes system fonts through country `font_key` settings: `latin-serif`, `japanese-gothic`, `chinese-heiti`, `hong-kong-heiti`, and `korean-gothic`. Use these for French accents, Japanese, Chinese, and Korean rather than dropping text or transliterating everything into English.
- `render_newspaper.py` supports three weights: `bold` for headline/section/ad labels, `regular` for decks and snippet headings, and `thin` for issue lines, captions, report fill, and ad copy.
- For ASCII 5x7 text, bold is implemented by a one-pixel horizontal offset and thin remains dark enough to read after nearest upscaling. For local scripts, the renderer draws native fonts into an alpha layer, hard-thresholds that layer, and pastes crisp single-color pixels so text does not become gray or blurry after nearest upscaling.
- Newspaper filler should be paragraph-like, not phonebook-like short entries. Convert secondary events and report fill into compact paragraphs, use drop caps at paragraph starts, and avoid repeating bare years or headline fragments as isolated rows.
- Prepare `newspaper_paragraphs` as the main body copy: 6-10 dense local-language paragraphs, each long enough to occupy several wrapped lines. Keep `reports` and `ad_copy` compact; they are texture, not the main article body.
- Use drop caps sparingly. The renderer defaults to one drop cap every two paragraphs, so do not split a single idea into many tiny paragraphs.
- When testing layout, any visible text collision is a failure. Reduce paragraph count, skip narrow flow segments, stop columns early, or leave empty paper texture rather than allowing overlapping text.

When rendering, prefer this manifest shape:

```json
{
  "source_image": "final.png",
  "style_key": "france",
  "language": "fr",
  "font_key": "latin-serif",
  "place": "Paris",
  "date": "July 1",
  "display_date": "July 1, 1903",
  "event": "Short event anchor",
  "headline": "TITRE LOCAL COURT",
  "deck": "UNE LIGNE DE CHAPEAU COMPACTE",
  "snippets": ["NOTE DE VILLE", "NOTE DU MARCHÉ", "NOTE DU TEMPS"],
  "reports": ["LES CAFÉS LISENT L ÉDITION DU MATIN", "LE MARCHÉ SURVEILLE LA RIVIÈRE"],
  "secondary_events": [{"date": "1900", "headline": "BRÈVE LOCALE", "note": "Un fait court pour remplir la page"}],
  "newspaper_paragraphs": ["Autour du boulevard, la nouvelle circule comme une dépêche que chacun veut vérifier. Les ateliers parlent du départ, les cafés comparent les horaires, et les kiosques replacent l'événement parmi les autres signes d'une ville qui apprend à se regarder dans la presse illustrée."],
  "caption": "LÉGENDE COURTE",
  "ad_copy": [{"label": "THÉÂTRE", "copy": "CE SOIR"}, {"label": "VÉLO", "copy": "LAMPE NEUVE"}],
  "ads": [{"path": "ads/perfume-theatre/perfume-theatre.png", "label": "THÉÂTRE", "copy": "CE SOIR", "aspect": "wide", "target_dimensions": [420, 160]}],
  "ad_count": 6,
  "age_filter_strength": 0.72,
  "retro_filter": "belle-epoque-print",
  "retro_filter_strength": 0.42,
  "optional_final_illustration": true,
  "use_static_ads": false
}
```

Do not ask workers to redraw the masthead from scratch. The renderer selects from five local real masthead assets for the country. Ask workers for live ad panels or tiny ornaments only, and let static assets preserve the country newspaper identity.

## Masthead Assets

Mastheads are image assets, not just text, and real mastheads are the default. Use this order:

1. Use one of the five local real masthead/logo PNG choices under `assets/newspaper/<style-key>/real-mastheads/`.
2. If the user supplied a better masthead scan/crop, process it with `scripts/pixelize_masthead_asset.py` into `assets/newspaper/<style-key>/historical-mastheads/` and use it.
3. If an openly licensed historical masthead crop already exists locally, use it.
4. Only if no real asset exists, use the fictional fallback PNGs from `assets/newspaper/<style-key>/masthead-*.png`.

Real masthead assets must be visually fused into the paper. `render_newspaper.py` recolors mastheads to the current newspaper ink/paper treatment at paste time; do not paste a raw modern RGB logo with its original colors unless the user asks for faithful reproduction.

To create a masthead asset from a scan:

```text
python3 scripts/pixelize_masthead_asset.py \
  --input source-scan.png \
  --out assets/newspaper/france/historical-mastheads/example.png \
  --crop left,top,right,bottom \
  --pixel-width 720 \
  --colors 5
```

After adding assets, rerun:

```text
python3 scripts/generate_newspaper_assets.py
```

The generated `layout-templates.json` keeps five `real_masthead_assets` per country. `render_newspaper.py` randomly selects one on every run unless the manifest pins `masthead_index`, `masthead_seed`, or `masthead_asset`.

## Shared Pixel Font

Use the bundled 5x7 font for ASCII intentionally readable text in the lead artwork. This includes the watermark, signs, posters, storefront names, station labels, banners, and short date/event markers.

- Font asset: `assets/pixel-font-5x7.json`
- Usage guide: `references/pixel-font.md`
- Style: uppercase 5x7 bitmap, integer-scaled, no antialiasing.
- Scope: readable ASCII text only. For newspaper body text and ads, use the renderer's country `font_key` support when French accents, Japanese, Chinese, or Korean are needed.

Keep readable lead-image phrases short. Prefer tiny labels like `JULY 1`, `PARIS`, `EXPO`, `METRO`, `OPEN`, `BELL`, `TV`, or invented initials over full sentences. For newspaper sprites, allow local-language pixelized text when the ad brief requires it.

## Palette Selection Logic

Choose the time-of-day palette after researching the event, before generating the background or spawning workers.

- `morning`: use for openings, launches, first services, school/work departures, parades starting early, optimism, recovery, construction beginnings, market awakenings, and events whose visual metaphor is "a new era starts."
- `day`: use for official ceremonies, sports, elections, exhibitions, factory/office life, public infrastructure, trade, crowds, shopping, and events that need documentary clarity or civic scale.
- `dusk`: use for premieres, nightlife beginning, finance/market tension, farewells, handovers, countdowns, strikes, late-afternoon public drama, romance, nostalgia, and events that feel suspended between confidence and fracture.
- `night`: use for cinema, music, cabaret, neon streets, broadcast/media culture, disasters after dark, anxiety, crisis, surveillance, hidden labor, speculative finance, harbor/city lights, and events whose memory is electric or uneasy.

Decision order:

1. If the event has a documented time of day, use that unless it weakens the composition.
2. If the event is tied to a venue with a strong light identity, let the venue steer: stadium/expo/official square usually `day`; cinema/cabaret/neon harbor usually `night`; opening commute/station usually `morning`; closing bell/handover/premiere queue usually `dusk`.
3. If the vibe contains words like fresh, opening, dawn, hopeful, rebuilding, school, commute, use `morning`.
4. If the vibe contains words like civic, booming, official, industrial, consumer, crowded, transparent, use `day`.
5. If the vibe contains words like nostalgic, farewell, countdown, speculative, glamorous, uncertain, use `dusk`.
6. If the vibe contains words like neon, cinematic, cabaret, crisis, secret, humid, electric, sleepless, use `night`.
7. If no clue dominates, default by era: France `dusk`, United States `day`, Japan `night`, China `day`, Hong Kong `night`, Korea `day`.

## Output Folder

Use:

```text
output/pixel-belle-epoque/<country>-<date-or-monthday>-<event-slug>/
```

Expected files:

- `research.md`
- `sources.json`
- `palette.json`
- `sprite-plan.json`
- `background.png`
- `sprites/<worker-id>/*.png`
- `composition-manifest.json`
- `final.png`
- `preview.png`
- `newspaper-plan.json`
- `newspaper-manifest.json`
- `newspaper.png`
- `newspaper-commercial-illustration.png` if the optional final image-edit stage ran
- `newspaper-preview.png`
- `newspaper-render.json`
- `ads/<worker-id>/*.png`
- `qa.md`

## Watermark

Every final image should include a small pixel-style text watermark in one random corner. Keep it legible but subordinate, like a printed corner mark on a memory postcard.

Text format:

```text
La Belle Epoque - <Place Name> - <Date>
```

Use English place names and the user's date or the resolved date anchor. Examples:

```text
La Belle Epoque - Hong Kong - July 1
La Belle Epoque - Tokyo - August 1, 1987
La Belle Epoque - Paris - May 6, 1889
```

When using `compose_manifest.py`, include watermark metadata in `composition-manifest.json`:

```json
{
  "place": "Hong Kong",
  "date": "July 1",
  "watermark": {
    "enabled": true,
    "corner": "random"
  }
}
```

The script will auto-render `La Belle Epoque - <place> - <date>` if `watermark.text` is omitted. Use `watermark.text` only when the place/date need a special English spelling. The script records the chosen corner in `final.json`.

The watermark renderer uses the same bundled `pixel-font-5x7.json`; do not replace it with a system font.

## Quality Bar

- The final image must feel like a Belle Epoque memory object, not a generic retro scene.
- The final deliverable is `newspaper.png`; `final.png` is the embedded lead image.
- The newspaper page must read immediately as a country-specific period front page, not a poster or scrapbook.
- The embedded lead image must remain visually dominant and unaltered except for being fitted into the newspaper frame.
- Include at least 4 period advertising sprites or ad panels in the newspaper.
- Every visible detail should either support the date event, the era vibe, local urban texture, or the era's hidden tension.
- Include at least 8 visible clues tied to the chosen date/event.
- Include at least 5 depth layers: sky/background skyline, far architecture, midground street or venue, foreground sprite action, near props/texture.
- Use the selected time-of-day palette with restraint: dominant, secondary, accent, shadow, and highlight roles should be clear. Do not flatten all four palettes into one undirected color dump.
- The watermark must not cover the central subject, faces, date-event clues, or dense signage. If the random corner collides with important detail, move it to another corner and note that adjustment in `qa.md`.
- All ASCII lead-image text must share the bundled 5x7 pixel font. Newspaper text uses either the bundled 5x7 font for English/ASCII or the renderer's country-specific pixelized local font key.
- Keep source URLs in the final response, along with the final image path and a short note on the event selected.
