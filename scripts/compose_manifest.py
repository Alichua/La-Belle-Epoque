#!/usr/bin/env python3
"""Composite Belle Epoque pixel sprites over a background from a JSON manifest."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

from PIL import Image, ImageColor, ImageDraw, ImageOps


PIXEL_FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10011", "10001", "10001", "01110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
    "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "/": ["00001", "00001", "00010", "00100", "01000", "10000", "10000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "01100", "01100", "01000"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    "'": ["01100", "01100", "01000", "00000", "00000", "00000", "00000"],
    "&": ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    " ": ["000", "000", "000", "000", "000", "000", "000"],
}
FONT_PATH = Path(__file__).resolve().parents[1] / "assets" / "pixel-font-5x7.json"


def load_pixel_font() -> dict[str, list[str]]:
    if not FONT_PATH.exists():
        return PIXEL_FONT
    data = json.loads(FONT_PATH.read_text(encoding="utf-8"))
    return {str(key): list(value) for key, value in data.items()}


PIXEL_FONT = load_pixel_font()


def resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def load_rgba(path: Path) -> Image.Image:
    image = Image.open(path)
    image.load()
    return ImageOps.exif_transpose(image).convert("RGBA")


def anchored_xy(x: int, y: int, width: int, height: int, anchor: str) -> tuple[int, int]:
    if anchor == "center":
        return x - width // 2, y - height // 2
    if anchor == "bottom-center":
        return x - width // 2, y - height
    if anchor == "bottom-left":
        return x, y - height
    if anchor == "top-center":
        return x - width // 2, y
    return x, y


def sprite_size(sprite: dict[str, Any], image: Image.Image) -> tuple[int, int]:
    if "width" in sprite and "height" in sprite:
        return int(sprite["width"]), int(sprite["height"])
    scale = float(sprite.get("scale", 1.0))
    return max(1, round(image.width * scale)), max(1, round(image.height * scale))


def normalize_watermark_text(text: str) -> str:
    return "".join(ch if ch.upper() in PIXEL_FONT else " " for ch in text).upper()


def glyph_width(ch: str) -> int:
    glyph = PIXEL_FONT.get(ch, PIXEL_FONT[" "])
    return len(glyph[0])


def measure_pixel_text(lines: list[str], scale: int) -> tuple[int, int]:
    if not lines:
        return 0, 0
    widths = []
    for line in lines:
        width = sum(glyph_width(ch) + 1 for ch in line.rstrip())
        widths.append(max(0, width - 1))
    return max(widths) * scale, (len(lines) * 7 + max(0, len(lines) - 1) * 2) * scale


def wrap_pixel_text(text: str, max_width: int, scale: int) -> list[str]:
    words = normalize_watermark_text(text).split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if measure_pixel_text([candidate], scale)[0] <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [normalize_watermark_text(text)]


def draw_pixel_text(
    image: Image.Image,
    xy: tuple[int, int],
    lines: list[str],
    scale: int,
    color: tuple[int, int, int, int],
) -> None:
    draw = ImageDraw.Draw(image)
    x0, y = xy
    for line in lines:
        x = x0
        for ch in line:
            glyph = PIXEL_FONT.get(ch, PIXEL_FONT[" "])
            for row, pattern in enumerate(glyph):
                for col, enabled in enumerate(pattern):
                    if enabled == "1":
                        draw.rectangle(
                            (
                                x + col * scale,
                                y + row * scale,
                                x + (col + 1) * scale - 1,
                                y + (row + 1) * scale - 1,
                            ),
                            fill=color,
                        )
            x += (len(glyph[0]) + 1) * scale
        y += 9 * scale


def watermark_text(manifest: dict[str, Any]) -> str:
    watermark = manifest.get("watermark", {})
    if watermark.get("text"):
        return str(watermark["text"])
    place = watermark.get("place") or manifest.get("place") or manifest.get("city") or manifest.get("country")
    date = watermark.get("date") or manifest.get("date") or manifest.get("date_anchor")
    pieces = ["La Belle Epoque"]
    if place:
        pieces.append(str(place))
    if date:
        pieces.append(str(date))
    return " - ".join(pieces)


def apply_watermark(final: Image.Image, manifest: dict[str, Any]) -> dict[str, Any] | None:
    config = manifest.get("watermark", {})
    if config is False or config.get("enabled") is False:
        return None

    width, height = final.size
    scale = int(config.get("scale") or max(1, min(width, height) // 360))
    margin = int(config.get("margin") or max(4, scale * 5))
    max_text_width = max(24, width - margin * 2)
    lines = wrap_pixel_text(watermark_text(manifest), max_text_width, scale)
    text_width, text_height = measure_pixel_text(lines, scale)

    if text_width > max_text_width and scale > 1:
        scale = 1
        lines = wrap_pixel_text(watermark_text(manifest), max_text_width, scale)
        text_width, text_height = measure_pixel_text(lines, scale)

    corners = ["top-left", "top-right", "bottom-left", "bottom-right"]
    corner = str(config.get("corner", "random"))
    if corner == "random" or corner not in corners:
        seed = config.get("seed")
        rng = random.Random(seed) if seed is not None else random.SystemRandom()
        corner = rng.choice(corners)

    x = margin if "left" in corner else max(margin, width - margin - text_width)
    y = margin if "top" in corner else max(margin, height - margin - text_height)

    color = ImageColor.getcolor(str(config.get("color", "#f8f4e8")), "RGBA")
    opacity = float(config.get("opacity", 0.78))
    color = (color[0], color[1], color[2], round(color[3] * opacity))
    shadow_color = ImageColor.getcolor(str(config.get("shadow_color", "#05040a")), "RGBA")
    shadow_opacity = float(config.get("shadow_opacity", 0.58))
    shadow_color = (
        shadow_color[0],
        shadow_color[1],
        shadow_color[2],
        round(shadow_color[3] * shadow_opacity),
    )

    layer = Image.new("RGBA", final.size, (0, 0, 0, 0))
    draw_pixel_text(layer, (x + scale, y + scale), lines, scale, shadow_color)
    draw_pixel_text(layer, (x, y), lines, scale, color)
    final.alpha_composite(layer, (0, 0))

    return {
        "text": watermark_text(manifest),
        "rendered_text": " / ".join(lines),
        "corner": corner,
        "box": [x, y, text_width, text_height],
        "scale": scale,
    }


def composite(manifest_path: Path, out_path: Path, preview_scale: int | None) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    base_dir = manifest_path.parent

    background_value = manifest.get("background") or manifest.get("canvas", {}).get("background")
    if not background_value:
        raise SystemExit("Manifest must include 'background' or 'canvas.background'.")

    background = load_rgba(resolve(base_dir, background_value))
    canvas = manifest.get("canvas", {})
    width = int(canvas.get("width", background.width))
    height = int(canvas.get("height", background.height))
    if background.size != (width, height):
        background = background.resize((width, height), Image.Resampling.NEAREST)

    final = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    final.alpha_composite(background, (0, 0))

    placed: list[dict[str, Any]] = []
    for sprite in sorted(manifest.get("sprites", []), key=lambda item: int(item.get("z", 0))):
        image = load_rgba(resolve(base_dir, sprite["path"]))
        target_size = sprite_size(sprite, image)
        if image.size != target_size:
            image = image.resize(target_size, Image.Resampling.NEAREST)
        opacity = float(sprite.get("opacity", 1.0))
        if opacity < 1.0:
            alpha = image.getchannel("A").point(lambda value: round(value * opacity))
            image.putalpha(alpha)
        x, y = anchored_xy(
            int(sprite.get("x", 0)),
            int(sprite.get("y", 0)),
            image.width,
            image.height,
            str(sprite.get("anchor", "top-left")),
        )
        final.alpha_composite(image, (x, y))
        placed.append(
            {
                "id": sprite.get("id"),
                "path": sprite["path"],
                "box": [x, y, image.width, image.height],
                "z": int(sprite.get("z", 0)),
            }
        )

    watermark = apply_watermark(final, manifest)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    final.convert("RGBA").save(out_path)

    summary = {
        "output": str(out_path),
        "size": [width, height],
        "sprite_count": len(placed),
        "placed": placed,
    }
    if watermark:
        summary["watermark"] = watermark
    summary_path = out_path.with_suffix(".json")
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    scale = preview_scale if preview_scale is not None else int(canvas.get("preview_scale", 0) or 0)
    if scale > 1:
        preview = final.resize((width * scale, height * scale), Image.Resampling.NEAREST)
        preview_path = out_path.with_name(f"{out_path.stem}-preview-{scale}x{out_path.suffix}")
        preview.save(preview_path)
        summary["preview"] = str(preview_path)
        summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path, help="Path to composition-manifest.json")
    parser.add_argument("--out", required=True, type=Path, help="Output final PNG path")
    parser.add_argument("--preview-scale", type=int, default=None, help="Optional nearest-neighbor preview multiplier")
    args = parser.parse_args()

    summary = composite(args.manifest.resolve(), args.out.resolve(), args.preview_scale)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
