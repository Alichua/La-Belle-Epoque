#!/usr/bin/env python3
"""Turn a scanned masthead crop into a transparent pixel asset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageColor, ImageOps


def rgba(value: str) -> tuple[int, int, int, int]:
    return ImageColor.getcolor(value, "RGBA")


def trim_alpha(image: Image.Image) -> Image.Image:
    bbox = image.getbbox()
    return image.crop(bbox) if bbox else image


def transparent_from_light(image: Image.Image, threshold: int) -> Image.Image:
    image = ImageOps.exif_transpose(image).convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            if (r + g + b) // 3 >= threshold:
                pixels[x, y] = (r, g, b, 0)
    return trim_alpha(image)


def monochrome_ink(image: Image.Image, ink: str, threshold: int) -> Image.Image:
    gray = ImageOps.grayscale(image.convert("RGBA"))
    alpha = gray.point(lambda value: 255 if value <= threshold else 0)
    result = Image.new("RGBA", image.size, rgba(ink))
    result.putalpha(alpha)
    return trim_alpha(result)


def quantize_pixel(image: Image.Image, width: int, colors: int) -> Image.Image:
    image = image.convert("RGBA")
    scale = max(1, round(image.width / width))
    small_w = max(1, image.width // scale)
    small_h = max(1, image.height // scale)
    small = image.resize((small_w, small_h), Image.Resampling.BOX)
    method = Image.Quantize.FASTOCTREE if small.mode == "RGBA" else Image.Quantize.MEDIANCUT
    quantized = small.quantize(colors=max(2, colors), method=method).convert("RGBA")
    return quantized.resize((small_w * scale, small_h * scale), Image.Resampling.NEAREST)


def process(args: argparse.Namespace) -> dict[str, object]:
    source = Path(args.input).resolve()
    out = Path(args.out).resolve()
    image = Image.open(source)
    if args.crop:
        image = image.crop(tuple(int(v) for v in args.crop.split(",")))
    if args.remove_light_background:
        image = transparent_from_light(image, args.light_threshold)
    if args.monochrome:
        image = monochrome_ink(image, args.ink, args.ink_threshold)
    image = quantize_pixel(image, args.pixel_width, args.colors)
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out)
    summary = {
        "source": str(source),
        "output": str(out),
        "size": [image.width, image.height],
        "crop": args.crop,
        "pixel_width": args.pixel_width,
        "colors": args.colors,
        "monochrome": args.monochrome,
        "remove_light_background": args.remove_light_background,
    }
    out.with_suffix(".json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Scanned masthead crop or page image.")
    parser.add_argument("--out", required=True, help="Output transparent PNG asset.")
    parser.add_argument("--crop", help="Optional crop box: left,top,right,bottom.")
    parser.add_argument("--pixel-width", type=int, default=720)
    parser.add_argument("--colors", type=int, default=4)
    parser.add_argument("--remove-light-background", action="store_true", default=True)
    parser.add_argument("--keep-light-background", action="store_false", dest="remove_light_background")
    parser.add_argument("--light-threshold", type=int, default=228)
    parser.add_argument("--monochrome", action="store_true", help="Convert dark scan ink into a single color.")
    parser.add_argument("--ink", default="#2a1d1b")
    parser.add_argument("--ink-threshold", type=int, default=45)
    args = parser.parse_args()
    print(json.dumps(process(args), indent=2))


if __name__ == "__main__":
    main()
