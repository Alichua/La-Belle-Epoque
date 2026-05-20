# Newspaper Styles

Use real newspaper masthead assets by default, recolored into the page palette so they feel printed into the paper. Each country has five local real masthead choices, and the renderer randomly selects one on every run unless pinned. Fictional mastheads and static ads are fallback assets only.

## France

- Style key: `france`
- Fictional mastheads: `LE BOULEVARD MODERNE`, `LA GAZETTE ELECTRIQUE`, `LE PETIT BELLE EPOQUE`
- Page feel: cream paper, black ink, red rule accents, Art Nouveau curves, dense but elegant columns.
- Typography feel: tall masthead, thin dividers, tiny poster-like drop caps.
- Ad sprite brief themes: perfume bottle, bicycle shop, cabaret ticket, department-store glove, metro token, chocolate box, theatre poster, absinthe glass.
- Palette: `#2a1d1b`, `#4f3828`, `#8f642f`, `#c79a3c`, `#d94d3f`, `#1f4b4a`, `#2f766f`, `#b85f82`, `#f1d27a`, `#fff0d0`, `#f8f4e8`, `#e7e0d2`
- Headline cues: boulevard, electric lamps, metro, exposition, theatre, morning edition, cafe society.

## United States

- Style key: `united-states`
- Fictional mastheads: `THE AMERICAN SIGNAL`, `MARKET STREET DAILY`, `THE NEON CHRONICLE`
- Page feel: high-contrast tabloid/broadsheet hybrid, bold boxes, ticker strips, ad-heavy lower rail.
- Typography feel: blocky headline, boxed sidebars, small stock/weather snippets.
- Ad sprite brief themes: personal computer, mall sale tag, VHS tape, sneaker, boxy sedan, diner coffee, payphone, brokerage card.
- Palette: `#050712`, `#111a33`, `#1f3b73`, `#2952a3`, `#39d3ff`, `#ff2f92`, `#ffd13b`, `#f28b30`, `#c8d0da`, `#f6f7fb`, `#222222`, `#ffffff`
- Headline cues: markets, malls, screens, highways, broadcast, boom years, special report.

## Japan

- Style key: `japan`
- Fictional mastheads: `TOKYO EVENING PRESS`, `GINZA CITY TIMES`, `SHOWA SIGNAL`
- Page feel: compact metropolitan evening paper, neat vertical rhythm translated into pixel blocks, neon accent tabs.
- Typography feel: clean grids, small label boxes, city-pop advertisement energy.
- Ad sprite brief themes: cassette tape, record shop tag, taxi, vending machine, camera, department-store bag, train ticket, karaoke microphone.
- Palette: `#060817`, `#101d3a`, `#245f8f`, `#2aa7c8`, `#74e3d8`, `#f4f2d6`, `#ffd49a`, `#ff5f6d`, `#d92f8a`, `#7e3fb3`, `#2c2c35`, `#ffffff`
- Headline cues: night edition, tower lights, rail, city pop, bubble, department store, station crowds.

## China

- Style key: `china`
- Fictional mastheads: `OPEN CITY DAILY`, `REFORM MORNING NEWS`, `THE RIVERFRONT BUILDER`
- Page feel: practical civic paper, construction-line grid, red title rules, development-zone optimism.
- Typography feel: sturdy masthead, boxed notices, public announcement rhythm.
- Ad sprite brief themes: appliance ad, bicycle, crane, real-estate board, pager/mobile shop, factory gate, market stall sign, bus ticket.
- Palette: `#071b24`, `#123746`, `#1d6070`, `#2e9aa0`, `#77d1c8`, `#f2e3bf`, `#f1c232`, `#f08b32`, `#d9482e`, `#a42020`, `#5b6970`, `#ffffff`
- Headline cues: opening, building, riverfront, factories, new road, trade, city change.

## Hong Kong

- Style key: `hong-kong`
- Fictional mastheads: `HARBOUR EVENING`, `NEON HARBOUR DAILY`, `THE COUNTDOWN POST`
- Page feel: dense commercial tabloid, wet-ink contrast, neon ad strip, harbor weather ticker.
- Typography feel: compressed boxes, stacked ad panels, cinematic headline.
- Ad sprite brief themes: taxi panel, watch shop, tea restaurant cup, ferry ticket, cinema poster, electronics sign, minibus placard, jewelry case.
- Palette: `#030914`, `#071b33`, `#0b3f5f`, `#0c7f96`, `#20d2d6`, `#ffd33d`, `#f39a24`, `#ff4b38`, `#ff2aa3`, `#8526b8`, `#1c1c22`, `#ffffff`
- Headline cues: harbor, neon, countdown, finance, cinema, ferry, humid night, late edition.

## Korea

- Style key: `korea`
- Fictional mastheads: `SEOUL OLYMPIC DAILY`, `GANGNAM MORNING`, `THE HAN RIVER STANDARD`
- Page feel: clean developmental daily, Olympic accent rings as abstract color dots, apartment and department-store ad rhythm.
- Typography feel: orderly masthead, sport/civic sidebars, bank/electronics ad blocks.
- Ad sprite brief themes: sedan, Olympic pennant, TV set, bank window, department-store bag, school notebook, apartment key, coffee cup.
- Palette: `#070912`, `#11192b`, `#273550`, `#46546a`, `#c6ccd0`, `#ffffff`, `#f3e4bd`, `#f5c057`, `#d7472f`, `#214aa5`, `#38aeea`, `#15945f`
- Headline cues: Olympic city, middle class, apartments, broadcast, banks, export, pre-IMF confidence.

## Layout Defaults

- Newspaper width: about source image width * 1.08 unless the manifest overrides it.
- Newspaper height: at least source image height * 1.30 to 1.40, but the renderer may grow taller so the lead image can remain at or near original size.
- Margins: 3-4% of page width.
- Lead image: preserve source aspect ratio and original pixel dimensions when page geometry allows; never crop the lead image.
- Lead image height: usually 54-62% of page height after the page has grown around it.
- Header height: 18-22% of page height.
- Lower rail: 18-22% of page height for snippets and ad sprites.
- Ads: 4-8 small panels, placed in lower rail and side gaps if available. Generate them live from run-specific briefs with one worker per ad sprite.
- Paper texture: subtle pixel speckles, 1-color or 2-color only.

## Static Assets

Use `assets/newspaper/layout-templates.json` as the executable layout registry. It maps each style key to:

- `layout_family` and `decor`
- `real_masthead_name`
- `paper_color`, `ink_color`, `accent_color`, and `muted_color` for the newspaper surface
- fallback `masthead_names`
- five `real_masthead_assets`
- optional `historical_masthead_assets`
- `masthead_assets`, `divider_asset`, and `badge_asset`
- `advertising_labels` and `default_ad_assets` for fallback/debug only
- `use_static_ads_default: false`
- page width/height, header, lower rail, lead image, masthead, headline, and ad-column ratios
- normalized scan-derived slots for masthead, issue line, headline, deck, lead image, caption, snippets, and ads

The renderer should paste the static masthead/divider/badge assets first. Generated worker ads should fill ad slots. Default static ad assets fill slots only when `use_static_ads` is explicitly true.

Real masthead/logo choices live under `assets/newspaper/<style-key>/real-mastheads/` and are recolored by the renderer. Additional scan crops can live under `historical-mastheads/`. Fictional mastheads are used only if no real masthead asset exists.

Keep the newspaper paper/ink colors separate from the event image palette. The lead image may use a vivid morning/day/dusk/night palette, but the page surface should use the template's paper, ink, accent, and muted rule colors so real mastheads and default ads fuse into one printed object.
