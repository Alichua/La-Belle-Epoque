#!/usr/bin/env python3
"""Generate five real-masthead pixel choices for every newspaper style."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
FONT = json.loads((ROOT / "assets" / "pixel-font-5x7.json").read_text(encoding="utf-8"))
OUT = ROOT / "assets" / "newspaper"


REAL_MASTHEADS: dict[str, dict[str, Any]] = {
    "france": {
        "name": "Le Petit Journal",
        "slug": "le-petit-journal",
        "source": "source-scans/le-petit-journal-header-1919.png",
        "palette": ["#2a1d1b", "#f8f4e8", "#d94d3f"],
        "script": "latin-serif",
    },
    "united-states": {
        "name": "USA TODAY",
        "slug": "usa-today",
        "source": "source-scans/usa-today-commons-2012.png",
        "palette": ["#050712", "#f6f7fb", "#2952a3"],
        "script": "latin-modern",
    },
    "japan": {
        "name": "THE ASAHI SHIMBUN",
        "slug": "asahi-shimbun",
        "source": "source-scans/asahi-shimbun-commons.png",
        "palette": ["#060817", "#f4f2d6", "#d92f8a"],
        "script": "latin-compact",
    },
    "china": {
        "name": "PEOPLE'S DAILY",
        "slug": "peoples-daily",
        "source": "source-scans/peoples-daily-commons.png",
        "palette": ["#071b24", "#f2e3bf", "#d9482e"],
        "script": "latin-civic",
    },
    "hong-kong": {
        "name": "APPLE DAILY",
        "slug": "apple-daily",
        "source": "source-scans/apple-daily-commons.png",
        "palette": ["#030914", "#ffffff", "#ff4b38"],
        "script": "latin-tabloid",
    },
    "korea": {
        "name": "CHOSUN ILBO",
        "slug": "chosun-ilbo",
        "source": "source-scans/chosun-ilbo-commons.png",
        "palette": ["#070912", "#ffffff", "#214aa5"],
        "script": "latin-clean",
    },
}

VARIANTS: list[dict[str, Any]] = [
    {"label": "archive-clean", "threshold": 232, "pixel_width": 1040, "thicken": 0, "distress": 0.00, "rules": "none"},
    {"label": "press-bold", "threshold": 220, "pixel_width": 960, "thicken": 1, "distress": 0.01, "rules": "none"},
    {"label": "faded-scan", "threshold": 238, "pixel_width": 900, "thicken": 0, "distress": 0.08, "rules": "bottom"},
    {"label": "ruled-edition", "threshold": 228, "pixel_width": 980, "thicken": 0, "distress": 0.02, "rules": "double"},
    {"label": "boxed-print", "threshold": 225, "pixel_width": 920, "thicken": 1, "distress": 0.04, "rules": "box"},
]


def rgba(value: str) -> tuple[int, int, int, int]:
    return ImageColor.getcolor(value, "RGBA")


def normalize(text: str) -> str:
    return "".join(ch if ch.upper() in FONT else " " for ch in text).upper()


def glyph_width(ch: str) -> int:
    return len(FONT.get(ch, FONT[" "])[0])


def measure(text: str, scale: int) -> tuple[int, int]:
    text = normalize(text).rstrip()
    width = sum(glyph_width(ch) + 1 for ch in text)
    return max(0, width - 1) * scale, 7 * scale


def draw_text(image: Image.Image, xy: tuple[int, int], text: str, scale: int, fill: str) -> tuple[int, int]:
    draw = ImageDraw.Draw(image)
    ink = rgba(fill)
    x, y = xy
    for ch in normalize(text):
        glyph = FONT.get(ch, FONT[" "])
        for row, pattern in enumerate(glyph):
            for col, enabled in enumerate(pattern):
                if enabled == "1":
                    draw.rectangle(
                        (x + col * scale, y + row * scale, x + (col + 1) * scale - 1, y + (row + 1) * scale - 1),
                        fill=ink,
                    )
        x += (len(glyph[0]) + 1) * scale
    return measure(text, scale)


def trim_alpha(image: Image.Image) -> Image.Image:
    bbox = image.getbbox()
    return image.crop(bbox) if bbox else image


def scan_to_ink(source: Path, threshold: int, thicken: int, distress: float, seed: str) -> Image.Image:
    image = ImageOps.exif_transpose(Image.open(source)).convert("RGBA")
    gray = ImageOps.grayscale(image)
    src_alpha = image.getchannel("A")
    alpha = Image.new("L", image.size, 0)
    alpha_pixels = alpha.load()
    gray_pixels = gray.load()
    src_alpha_pixels = src_alpha.load()
    for y in range(image.height):
        for x in range(image.width):
            if src_alpha_pixels[x, y] == 0:
                continue
            value = gray_pixels[x, y]
            if value <= threshold:
                alpha_pixels[x, y] = max(55, min(255, 280 - value))
    for _ in range(thicken):
        alpha = alpha.filter(ImageFilter.MaxFilter(3))
    if distress > 0:
        rng = random.Random(seed)
        alpha_pixels = alpha.load()
        for y in range(alpha.height):
            for x in range(alpha.width):
                value = alpha_pixels[x, y]
                if value and rng.random() < distress:
                    alpha_pixels[x, y] = max(0, value - rng.randrange(80, 190))
    result = Image.new("RGBA", image.size, (0, 0, 0, 255))
    result.putalpha(alpha)
    return trim_alpha(result)


def pixelize(image: Image.Image, pixel_width: int) -> Image.Image:
    image = trim_alpha(image.convert("RGBA"))
    scale = max(1, round(image.width / pixel_width))
    small_w = max(1, image.width // scale)
    small_h = max(1, image.height // scale)
    small = image.resize((small_w, small_h), Image.Resampling.BOX)
    return small.resize((small_w * scale, small_h * scale), Image.Resampling.NEAREST)


def add_variant_rules(image: Image.Image, rules: str) -> Image.Image:
    if rules == "none":
        return image
    pad_x = 24 if rules in {"double", "box"} else 12
    pad_y = 16 if rules in {"double", "box"} else 10
    canvas = Image.new("RGBA", (image.width + pad_x * 2, image.height + pad_y * 2), (0, 0, 0, 0))
    canvas.alpha_composite(image, (pad_x, pad_y))
    draw = ImageDraw.Draw(canvas)
    ink = (0, 0, 0, 210)
    if rules == "bottom":
        draw.rectangle((pad_x, canvas.height - 7, canvas.width - pad_x, canvas.height - 5), fill=ink)
    elif rules == "double":
        draw.rectangle((pad_x, 5, canvas.width - pad_x, 7), fill=ink)
        draw.rectangle((pad_x, canvas.height - 8, canvas.width - pad_x, canvas.height - 6), fill=ink)
    elif rules == "box":
        draw.rectangle((4, 4, canvas.width - 5, canvas.height - 5), outline=ink, width=2)
        draw.rectangle((pad_x, canvas.height - 12, canvas.width - pad_x, canvas.height - 10), fill=ink)
    return trim_alpha(canvas)


def draw_fallback_masthead(style_key: str, config: dict[str, Any]) -> str:
    ink, paper, accent = config["palette"]
    image = Image.new("RGBA", (860, 150), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    script = config["script"]
    name = config["name"]
    if style_key == "united-states":
        draw.ellipse((28, 32, 112, 116), fill=rgba(accent))
        draw.rectangle((126, 42, 810, 112), outline=rgba(ink), width=4)
    elif style_key == "hong-kong":
        draw.rectangle((20, 26, 840, 120), fill=rgba(accent))
        draw.rectangle((28, 34, 832, 112), outline=rgba(paper), width=3)
    elif style_key == "china":
        draw.rectangle((20, 24, 840, 42), fill=rgba(accent))
        draw.rectangle((20, 110, 840, 116), fill=rgba(accent))
    elif style_key == "japan":
        for i, c in enumerate([accent, "#2aa7c8", "#ffd49a"]):
            draw.rectangle((24 + i * 42, 22, 54 + i * 42, 36), fill=rgba(c))
        draw.rectangle((20, 118, 840, 122), fill=rgba(accent))
    elif style_key == "korea":
        for i, c in enumerate([accent, "#d7472f", "#15945f"]):
            draw.ellipse((28 + i * 38, 22, 58 + i * 38, 52), outline=rgba(c), width=4)
        draw.rectangle((20, 116, 840, 121), fill=rgba(ink))
    else:
        draw.rectangle((20, 26, 840, 30), fill=rgba(ink))
        draw.rectangle((20, 116, 840, 120), fill=rgba(ink))

    scale = 7 if len(name) < 12 else 6
    while measure(name, scale)[0] > 700 and scale > 2:
        scale -= 1
    text_w, text_h = measure(name, scale)
    fill = paper if style_key == "hong-kong" else ink
    draw_text(image, ((image.width - text_w) // 2, 58 if scale >= 6 else 64), name, scale, fill)
    if script in {"latin-modern", "latin-tabloid"}:
        draw.rectangle((150, 124, 710, 130), fill=rgba(accent if style_key != "hong-kong" else paper))
    elif script == "latin-serif":
        draw.arc((390, 28, 470, 108), 80, 460, fill=rgba(accent), width=3)

    path = OUT / style_key / "real-mastheads" / f"{config['slug']}-fallback-pixel.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)
    return str(path.relative_to(ROOT))


def draw_choice_mastheads(style_key: str, config: dict[str, Any]) -> list[str]:
    source = OUT / style_key / config["source"]
    if not source.exists():
        return [draw_fallback_masthead(style_key, config)]
    outputs: list[str] = []
    for index, variant in enumerate(VARIANTS, 1):
        image = scan_to_ink(
            source,
            int(variant["threshold"]),
            int(variant["thicken"]),
            float(variant["distress"]),
            f"{style_key}-{variant['label']}",
        )
        image = pixelize(image, int(variant["pixel_width"]))
        image = add_variant_rules(image, str(variant["rules"]))
        path = OUT / style_key / "real-mastheads" / f"{config['slug']}-choice-{index:02d}-{variant['label']}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path)
        outputs.append(str(path.relative_to(ROOT)))
    draw_fallback_masthead(style_key, config)
    return outputs


def main() -> None:
    outputs = {style_key: draw_choice_mastheads(style_key, config) for style_key, config in REAL_MASTHEADS.items()}
    print(json.dumps(outputs, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
