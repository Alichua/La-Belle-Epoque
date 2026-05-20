# La Belle Epoque

[English](README.en-US.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-HK.md) | [한국어](README.ko.md)

![After image generation](../examples/stage2-after-image-gen.png)

Pick a country. Pick a date.

La Belle Epoque turns that moment into a retro front page: first as a pixel newspaper, then, if your session supports image generation, as a glossy commercial illustration.

Part archive, part city-pop poster, part nostalgia trip.

Six Belle Epoques, loosely defined:

- 🇫🇷 France, 1870s-1914: Paris boulevards, Art Nouveau, cabarets, posters, electricity, and modern crowds.
- 🇺🇸 United States, 1980-2001: malls, cable TV, finance, early computers, neon optimism, and the long consumer boom.
- 🇯🇵 Japan, 1955-1991: Tokyo lights, City Pop, department stores, records, taxis, and fragile abundance.
- 🇨🇳 China, 1978-2012: reform and opening, construction dust, factories, new towers, appliances, markets, and rapid modernization.
- 🇭🇰 Hong Kong, 1970s-1997: harbor neon, cinema, finance, density, taxis, wet streets, and the handover countdown.
- 🇰🇷 Korea, 1988-1997: post-Olympic Seoul, apartments, electronics, department stores, middle-class acceleration, and the IMF shock nearby.

## What It Does

Give the skill a country and date:

```text
Use $pixel-belle-epoque for Japan on October 23.
```

It researches a date-specific event inside that country's Belle Epoque, creates a pixel-art lead image, builds a country-specific newspaper front page, adds ad sprites, applies a retro print finish, and optionally makes a smooth GPT Image illustration variant.

Supported countries: France, United States, Japan, China, Hong Kong, Korea.

## Gallery

Stage 1 is the native output of the skill: a source-grounded pixel newspaper assembled from research, sprites, mastheads, ads, and the retro print renderer.

Stage 2 is optional. When image generation/editing is available, the finished newspaper is restyled into a cleaner commercial-illustration version while keeping the same layout.

| Stage 1: Pixel Newspaper | Stage 2: After Image Generation |
| --- | --- |
| <img src="../examples/stage1-pixel-newspaper.png" width="420" alt="Stage 1 pixel newspaper"> | <img src="../examples/stage2-after-image-gen.png" width="420" alt="Stage 2 after image generation"> |

## Install

Install the required skill first:

```text
Use $skill-installer to install pixel-art-creator.
```

Install this skill:

```text
Use $skill-installer to install git@github.com:Alichua/La-Belle-Epoque.git
```

Restart Codex after installing.

The renderer scripts need Python 3 and Pillow:

```bash
python3 -m pip install pillow
```

The optional commercial illustration variant depends on `$imagegen`; the CLI/API fallback may require `OPENAI_API_KEY`.

## Use

```text
Use $pixel-belle-epoque for the United States on April 30.
Use $pixel-belle-epoque for Japan on October 23. Also create the final commercial illustration variant if image_gen is available.
```

Output folder:

```text
output/pixel-belle-epoque/<country>-<date>-<event-slug>/
```

Main files: `newspaper.png`, `newspaper-commercial-illustration.png`, `final.png`, `research.md`, `sources.json`, `palette.json`.
