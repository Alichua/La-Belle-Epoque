#!/usr/bin/env python3
"""Render a compact pixel-art newspaper front page around a source image."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageFilter, ImageFont, ImageOps


SKILL_ROOT = Path(__file__).resolve().parents[1]
FONT_PATH = SKILL_ROOT / "assets" / "pixel-font-5x7.json"
TEMPLATE_PATH = SKILL_ROOT / "assets" / "newspaper" / "layout-templates.json"
ACTIVE_FONT_KEY = "latin-serif"
DEFAULT_PALETTE = [
    "#2a1d1b",
    "#4f3828",
    "#8f642f",
    "#c79a3c",
    "#d94d3f",
    "#1f4b4a",
    "#2f766f",
    "#f1d27a",
    "#fff0d0",
    "#f8f4e8",
    "#e7e0d2",
    "#1c1c22",
]

STYLE_ALIASES = {
    "america": "united-states",
    "china-mainland": "china",
    "fr": "france",
    "hk": "hong-kong",
    "hong kong": "hong-kong",
    "japanese": "japan",
    "korea": "korea",
    "south korea": "korea",
    "u.s.": "united-states",
    "u.s.a.": "united-states",
    "united states": "united-states",
    "usa": "united-states",
    "us": "united-states",
}

FONT_STACKS = {
    "ascii-pixel": [],
    "latin-serif": [
        "/System/Library/Fonts/Times.ttc",
        "/System/Library/Fonts/Palatino.ttc",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/NewYork.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ],
    "japanese-gothic": [
        "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc",
        "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ],
    "chinese-heiti": [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ],
    "hong-kong-heiti": [
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ],
    "korean-gothic": [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ],
    "unicode-fallback": [
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    ],
}

LOCALE_TEXT = {
    "france": {
        "language": "fr",
        "font_key": "latin-serif",
        "section_label": "DERNIÈRE HEURE",
        "edition_line": "ÉDITION BELLE ÉPOQUE",
        "fallback_reports": [
            "La rédaction rassemble les dépêches du jour.",
            "Les cafés lisent les nouvelles à voix basse.",
            "La ville garde la trace de cette matinée.",
            "Les affiches annoncent une époque en mouvement.",
        ],
        "fallback_snippets": [
            "ÉCHOS DE LA VILLE",
            "MARCHÉ ET BOULEVARD",
            "LE TEMPS DU JOUR",
        ],
        "fallback_headline": "LA VILLE RETIENT L INSTANT",
        "fallback_deck": "Une mémoire de la Belle Époque revient en pixels.",
        "fallback_caption": "Image principale tirée de l archive imaginaire.",
        "ad_labels": ["ANNONCE", "MARCHÉ", "THÉÂTRE", "BOUTIQUE", "BILLET"],
    },
    "united-states": {
        "language": "en",
        "font_key": "ascii-pixel",
        "section_label": "BREAKING NEWS",
        "edition_line": "BELLE EPOQUE EDITION",
        "fallback_reports": [
            "The city desk gathers the day's dispatches.",
            "Markets and stations carry the news.",
            "Small notices record the public mood.",
            "A new hour moves through the streets.",
        ],
        "fallback_snippets": [
            "CITY DESK",
            "MARKETS AND STATIONS",
            "WEATHER NOTE",
        ],
        "fallback_headline": "THE CITY MARKS THE MOMENT",
        "fallback_deck": "A Belle Epoque memory returns in pixel color.",
        "fallback_caption": "Lead image from the Belle Epoque archive.",
        "ad_labels": ["NOTICE", "MARKET", "TICKETS", "SPECIAL", "OPEN"],
    },
    "japan": {
        "language": "ja",
        "font_key": "japanese-gothic",
        "section_label": "号外",
        "edition_line": "ベル・エポック版",
        "fallback_reports": [
            "街角に号外が広がる。",
            "駅前の灯りがニュースを照らす。",
            "商店街は朝の声で満ちる。",
            "小さな記事が時代の気配を残す。",
        ],
        "fallback_snippets": [
            "街の短信",
            "市場と駅",
            "天気欄",
        ],
        "fallback_headline": "街はその日を記憶する",
        "fallback_deck": "ベル・エポックの記憶を画面に刻む。",
        "fallback_caption": "時代の情景を写した主図。",
        "ad_labels": ["広告", "劇場", "商店", "切符", "新発売"],
    },
    "china": {
        "language": "zh-Hans",
        "font_key": "chinese-heiti",
        "section_label": "要闻",
        "edition_line": "美好年代特刊",
        "fallback_reports": [
            "街头传来当天的消息。",
            "车站与商铺记录城市节奏。",
            "短讯栏保存此刻的回声。",
            "新式生活在纸面上展开。",
        ],
        "fallback_snippets": [
            "城中短讯",
            "市场与车站",
            "天气一栏",
        ],
        "fallback_headline": "城市记下这一刻",
        "fallback_deck": "美好年代的记忆在像素中重现。",
        "fallback_caption": "主图记录时代现场。",
        "ad_labels": ["广告", "市场", "戏院", "商号", "启事"],
    },
    "hong-kong": {
        "language": "zh-Hant",
        "font_key": "hong-kong-heiti",
        "section_label": "要聞",
        "edition_line": "美好年代特刊",
        "fallback_reports": [
            "街頭傳來當日消息。",
            "碼頭與電車站記下城市節奏。",
            "短訊欄保存此刻回聲。",
            "霓虹與報紙一同亮起。",
        ],
        "fallback_snippets": [
            "城中短訊",
            "市場與碼頭",
            "天氣一欄",
        ],
        "fallback_headline": "城市記下這一刻",
        "fallback_deck": "美好年代的記憶在像素中重現。",
        "fallback_caption": "主圖記錄時代現場。",
        "ad_labels": ["廣告", "市場", "戲院", "商號", "啟事"],
    },
    "korea": {
        "language": "ko",
        "font_key": "korean-gothic",
        "section_label": "속보",
        "edition_line": "벨 에포크 특집",
        "fallback_reports": [
            "거리마다 오늘의 소식이 퍼진다.",
            "역과 상점은 도시의 박자를 남긴다.",
            "짧은 기사들이 시대의 표정을 기록한다.",
            "새로운 생활의 불빛이 지면에 비친다.",
        ],
        "fallback_snippets": [
            "도시 단신",
            "시장과 역",
            "오늘의 날씨",
        ],
        "fallback_headline": "도시는 그날을 기억한다",
        "fallback_deck": "벨 에포크의 기억을 픽셀로 전한다.",
        "fallback_caption": "시대의 장면을 담은 주 이미지.",
        "ad_labels": ["광고", "시장", "극장", "상점", "특보"],
    },
}


def load_font() -> dict[str, list[str]]:
    return json.loads(FONT_PATH.read_text(encoding="utf-8"))


FONT = load_font()


def locale_for(style_key: str, manifest: dict[str, Any], template: dict[str, Any]) -> dict[str, Any]:
    locale = dict(LOCALE_TEXT.get(style_key, LOCALE_TEXT["united-states"]))
    if template.get("font_key"):
        locale["font_key"] = template["font_key"]
    if manifest.get("font_key"):
        locale["font_key"] = manifest["font_key"]
    if manifest.get("language"):
        locale["language"] = manifest["language"]
    if manifest.get("section_label"):
        locale["section_label"] = manifest["section_label"]
    if manifest.get("edition_line"):
        locale["edition_line"] = manifest["edition_line"]
    return locale


def set_active_font(font_key: str) -> None:
    global ACTIVE_FONT_KEY
    ACTIVE_FONT_KEY = font_key


def is_ascii_pixel_text(text: str | list[str]) -> bool:
    lines = text if isinstance(text, list) else [text]
    for line in lines:
        for ch in str(line):
            if ch.upper() not in FONT:
                return False
    return all(ord(ch) < 128 for line in lines for ch in str(line))


def use_bitmap_text(text: str | list[str]) -> bool:
    return ACTIVE_FONT_KEY == "ascii-pixel" and is_ascii_pixel_text(text)


def font_path_for(font_key: str) -> str | None:
    for candidate in FONT_STACKS.get(font_key, []) + FONT_STACKS["unicode-fallback"]:
        if Path(candidate).exists():
            return candidate
    return None


def pil_font(scale: int, weight: str = "regular", font_key: str | None = None) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    key = font_key or ACTIVE_FONT_KEY
    path = font_path_for(key)
    if not path:
        return ImageFont.load_default()
    size_multiplier = {"thin": 8, "regular": 10, "bold": 12}.get(weight, 10)
    size = max(7, scale * size_multiplier)
    try:
        return ImageFont.truetype(path, size=size, index=0)
    except OSError:
        return ImageFont.load_default()


def line_step(scale: int, weight: str = "regular", font_key: str | None = None) -> int:
    key = font_key or ACTIVE_FONT_KEY
    if key != "ascii-pixel":
        multiplier = {"thin": 9, "regular": 10, "bold": 12}.get(weight, 10)
        return max(10, scale * multiplier + max(3, scale * 3))
    return 9 * scale


def resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def resolve_asset(base: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    local = (base / path).resolve()
    if local.exists():
        return local
    return (SKILL_ROOT / path).resolve()


def load_rgba(path: Path) -> Image.Image:
    image = Image.open(path)
    image.load()
    return ImageOps.exif_transpose(image).convert("RGBA")


def recolor_asset(image: Image.Image, ink: str, paper: str | None = None, threshold: int = 214) -> Image.Image:
    """Map a scan-like asset onto the current newspaper ink/paper colors."""
    image = image.convert("RGBA")
    ink_rgba = color(ink)
    paper_rgba = color(paper) if paper else None
    alpha_values = [a for _, _, _, a in image.getdata() if a]
    is_alpha_mask = False
    if alpha_values:
        sample_colors: set[tuple[int, int, int]] = set()
        for r, g, b, a in image.getdata():
            if a:
                sample_colors.add((r, g, b))
                if len(sample_colors) > 8:
                    break
        is_alpha_mask = len(sample_colors) <= 3 and max(max(rgb) for rgb in sample_colors) < 40
    output = Image.new("RGBA", image.size, (0, 0, 0, 0))
    out = output.load()
    src = image.load()
    mask_alpha_threshold = 0
    if is_alpha_mask:
        sorted_alpha = sorted(alpha_values)
        mask_alpha_threshold = max(118, sorted_alpha[int(len(sorted_alpha) * 0.78)])
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = src[x, y]
            if a == 0:
                continue
            if is_alpha_mask:
                if a < mask_alpha_threshold:
                    continue
                alpha = min(255, max(80, a + 38))
                out[x, y] = (ink_rgba[0], ink_rgba[1], ink_rgba[2], alpha)
                continue
            luminance = (r * 299 + g * 587 + b * 114) // 1000
            if luminance >= threshold:
                if paper_rgba:
                    out[x, y] = (paper_rgba[0], paper_rgba[1], paper_rgba[2], a)
                continue
            if 95 <= luminance < threshold:
                alpha = max(24, min(a, 170 - luminance // 2))
            else:
                alpha = max(38, min(a, 255 - luminance))
            out[x, y] = (ink_rgba[0], ink_rgba[1], ink_rgba[2], alpha)
    bbox = output.getbbox()
    return output.crop(bbox) if bbox else output


def color(value: str) -> tuple[int, int, int, int]:
    return ImageColor.getcolor(value, "RGBA")


def solid_text_layer(layer: Image.Image, fill: tuple[int, int, int, int], weight: str) -> Image.Image:
    threshold = 64 if weight == "bold" else 98 if weight == "regular" else 118
    alpha = layer.getchannel("A").point(lambda value: 255 if value >= threshold else 0)
    target_alpha = fill[3]
    if weight == "thin":
        target_alpha = max(226, min(255, target_alpha))
    if target_alpha < 255:
        alpha = alpha.point(lambda value: target_alpha if value else 0)
    output = Image.new("RGBA", layer.size, fill)
    output.putalpha(alpha)
    return output


def blend_hex(a: str, b: str, ratio: float) -> str:
    ar, ag, ab, _ = color(a)
    br, bg, bb, _ = color(b)
    ratio = max(0.0, min(1.0, ratio))
    return hex_color(
        (
            round(ar * (1 - ratio) + br * ratio),
            round(ag * (1 - ratio) + bg * ratio),
            round(ab * (1 - ratio) + bb * ratio),
        )
    )


def hex_color(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def page_margin(
    page_width: int,
    manifest: dict[str, Any],
    template: dict[str, Any],
    default_ratio: float,
    min_default: int,
    max_ratio: float,
) -> int:
    default = int(template.get("margin") or max(min_default, round(page_width * float(template.get("margin_ratio", default_ratio)))))
    requested = manifest.get("margin")
    if requested is None:
        return default
    requested_margin = int(requested)
    if manifest.get("preserve_margin"):
        return requested_margin
    cap = max(default, round(page_width * float(template.get("max_margin_ratio", max_ratio))))
    return min(requested_margin, cap)


def sample_box_color(image: Image.Image, box: tuple[int, int, int, int], fallback: str) -> str:
    """Sample the already-rendered paper under a slot, like an eyedropper."""
    x, y, w, h = box
    if w <= 0 or h <= 0:
        return fallback
    points = [
        (x + w // 2, y + h // 2),
        (x + max(1, w // 5), y + max(1, h // 5)),
        (x + max(1, (w * 4) // 5), y + max(1, h // 5)),
        (x + max(1, w // 5), y + max(1, (h * 4) // 5)),
        (x + max(1, (w * 4) // 5), y + max(1, (h * 4) // 5)),
    ]
    pixels: list[tuple[int, int, int]] = []
    for px, py in points:
        px = max(0, min(image.width - 1, px))
        py = max(0, min(image.height - 1, py))
        r, g, b, _ = image.getpixel((px, py))
        pixels.append((r, g, b))
    channels = [sorted(pixel[i] for pixel in pixels)[len(pixels) // 2] for i in range(3)]
    return hex_color((channels[0], channels[1], channels[2]))


def trim_transparent(image: Image.Image) -> Image.Image:
    bbox = image.getbbox()
    return image.crop(bbox) if bbox else image


def normalize_text(text: str) -> str:
    return "".join(ch if ch.upper() in FONT else " " for ch in text).upper()


def glyph_width(ch: str) -> int:
    glyph = FONT.get(ch, FONT[" "])
    return len(glyph[0])


def measure_text(lines: list[str], scale: int) -> tuple[int, int]:
    if not use_bitmap_text(lines):
        font = pil_font(scale)
        draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        widths: list[int] = []
        heights: list[int] = []
        for line in lines:
            bbox = draw.textbbox((0, 0), str(line), font=font)
            widths.append(max(0, bbox[2] - bbox[0]))
            heights.append(max(1, bbox[3] - bbox[1]))
        return max(widths or [0]), sum(heights) + max(0, len(lines) - 1) * max(2, scale * 2)
    if not lines:
        return 0, 0
    widths = []
    for line in lines:
        width = sum(glyph_width(ch) + 1 for ch in line.rstrip())
        widths.append(max(0, width - 1))
    return max(widths) * scale, (len(lines) * 7 + max(0, len(lines) - 1) * 2) * scale


def text_height(line_count: int, scale: int) -> int:
    if line_count <= 0:
        return 0
    if ACTIVE_FONT_KEY != "ascii-pixel":
        return line_count * line_step(scale) + max(0, line_count - 1) * max(1, scale)
    return (line_count * 7 + max(0, line_count - 1) * 2) * scale


def wrap_text(text: str, max_width: int, scale: int, max_lines: int | None = None) -> list[str]:
    if not use_bitmap_text(text):
        source = str(text).strip()
        if not source:
            return [""]
        lines: list[str] = []
        current = ""
        has_spaces = any(ch.isspace() for ch in source)
        units = source.split() if has_spaces else list(source)
        separator = " " if has_spaces else ""
        for unit in units:
            candidate = unit if not current else f"{current}{separator}{unit}"
            if measure_text([candidate], scale)[0] <= max_width or not current:
                current = candidate
            else:
                lines.append(current)
                current = unit
                if max_lines and len(lines) >= max_lines:
                    return lines
        if current and (not max_lines or len(lines) < max_lines):
            lines.append(current)
        return lines or [source]
    words = normalize_text(text).split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if measure_text([candidate], scale)[0] <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
            if max_lines and len(lines) >= max_lines:
                return lines
    if current and (not max_lines or len(lines) < max_lines):
        lines.append(current)
    return lines or [normalize_text(text)]


def draw_pixel_text(
    image: Image.Image,
    xy: tuple[int, int],
    text: str | list[str],
    scale: int,
    fill: str,
    max_width: int | None = None,
    max_lines: int | None = None,
    weight: str = "regular",
) -> tuple[int, int]:
    lines = text if isinstance(text, list) else wrap_text(text, max_width or 10_000, scale, max_lines)
    if not use_bitmap_text(lines):
        font = pil_font(scale, weight)
        rgba = color(fill)
        if weight == "thin":
            rgba = (rgba[0], rgba[1], rgba[2], max(170, min(255, rgba[3])))
        x, y = xy
        max_line_width = 0
        step = line_step(scale, weight)
        layer_w = max(1, min(image.width - max(0, x), max_width or image.width))
        layer_h = max(1, step * max(1, len(lines)) + max(4, scale * 3))
        text_layer = Image.new("RGBA", (layer_w + 4, layer_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)
        local_y = 0
        for line in lines:
            draw.text((0, local_y), str(line), font=font, fill=rgba)
            if weight == "bold":
                draw.text((max(1, scale // 2), local_y), str(line), font=font, fill=rgba)
            bbox = draw.textbbox((0, local_y), str(line), font=font)
            max_line_width = max(max_line_width, bbox[2] - bbox[0])
            local_y += step
        bbox = text_layer.getbbox()
        if bbox:
            text_layer = text_layer.crop(bbox)
            if text_layer.width > 0 and text_layer.height > 0:
                pixelated = solid_text_layer(text_layer, rgba, weight)
                image.alpha_composite(pixelated, xy)
        return measure_text([str(line) for line in lines], scale)
    ink = color(fill)
    draw = ImageDraw.Draw(image)
    x0, y = xy
    offsets = [(0, 0)]
    if weight == "bold":
        offsets = [(0, 0), (scale, 0)]
    elif weight == "thin":
        ink = (ink[0], ink[1], ink[2], max(180, min(ink[3], 235)))
    for line in lines:
        x = x0
        for ch in line:
            glyph = FONT.get(ch, FONT[" "])
            for row, pattern in enumerate(glyph):
                for col, enabled in enumerate(pattern):
                    if enabled == "1":
                        for ox, oy in offsets:
                            draw.rectangle(
                                (
                                    x + col * scale + ox,
                                    y + row * scale + oy,
                                    x + (col + 1) * scale - 1 + ox,
                                    y + (row + 1) * scale - 1 + oy,
                                ),
                                fill=ink,
                            )
            x += (len(glyph[0]) + 1) * scale
        y += line_step(scale)
    return measure_text(lines, scale)


def draw_rule(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str) -> None:
    draw.rectangle(box, fill=color(fill))


def date_display_text(manifest: dict[str, Any]) -> str:
    for key in ("display_date", "date_label", "date"):
        value = str(manifest.get(key) or "").strip()
        if value:
            return value
    return "Belle Epoque"


def draw_prominent_date_badge(
    page: Image.Image,
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    manifest: dict[str, Any],
    ink: str,
    accent: str,
    paper: str,
    scale: int,
) -> tuple[int, int, int, int]:
    label = date_display_text(manifest)
    scale = max(1, scale)
    max_badge_w = max(1, box[2])
    lines = wrap_text(label, max(1, max_badge_w - max(36, scale * 18)), scale, 2)
    text_w, text_h = measure_text(lines, scale)
    required_w = text_w + max(44, scale * 22)
    if required_w > max_badge_w and scale > 1:
        scale -= 1
        lines = wrap_text(label, max(1, max_badge_w - max(34, scale * 18)), scale, 2)
        text_w, text_h = measure_text(lines, scale)
        required_w = text_w + max(42, scale * 22)
    w = min(max_badge_w, max(144, required_w))
    h = min(box[3], max(32, text_h + max(14, scale * 7)))
    x = box[0] + box[2] - w
    y = box[1]
    draw.rectangle((x, y, x + w, y + h), fill=color(blend_hex(paper, accent, 0.08)), outline=color(ink), width=1)
    draw.rectangle((x + 3, y + 3, x + w - 3, y + 6), fill=color(accent))
    draw_pixel_text(page, (x + max(9, scale * 5), y + max(9, scale * 5)), lines, scale, ink, w - max(18, scale * 10), 2, "bold")
    return (x, y, w, h)


def draw_belle_epoque_watermark(
    page: Image.Image,
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    max_width: int,
    accent: str,
    muted: str,
    ink: str,
    paper: str,
    scale: int,
) -> tuple[int, int, int, int]:
    text = "La Belle Epoque"
    scale = max(1, scale)
    lines = wrap_text(text, max_width, scale, 1)
    text_w, text_h = measure_text(lines, scale)
    x, y = xy
    pad_x = max(8, scale * 4)
    pad_y = max(5, scale * 3)
    box = (x, y, min(max_width, text_w + pad_x * 2), text_h + pad_y * 2)
    bx, by, bw, bh = box
    draw.rectangle((bx, by, bx + bw, by + bh), fill=color(blend_hex(paper, accent, 0.12)))
    draw.rectangle((bx, by, bx + bw, by + bh), outline=color(blend_hex(ink, accent, 0.35)), width=1)
    draw.rectangle((bx, by + bh - 4, bx + bw, by + bh - 2), fill=color(muted))
    colors = [accent, "#2f766f", "#c79a3c", ink]
    cursor_x = bx + pad_x
    for index, word in enumerate(["La", "Belle", "Epoque"]):
        word_color = colors[index % len(colors)]
        draw_pixel_text(page, (cursor_x, by + pad_y), word, scale, word_color, max_width, 1, "bold")
        word_w, _ = measure_text([word], scale)
        cursor_x += word_w + max(16, scale * 10)
    return box


def load_templates() -> dict[str, Any]:
    if not TEMPLATE_PATH.exists():
        return {}
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


def style_key_from_manifest(manifest: dict[str, Any]) -> str:
    raw = manifest.get("style_key") or manifest.get("country") or manifest.get("place") or "france"
    key = str(raw).strip().lower().replace("_", "-")
    return STYLE_ALIASES.get(key, key)


def select_template(manifest: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    templates = load_templates()
    key = style_key_from_manifest(manifest)
    if key not in templates:
        key = "france" if "france" in templates else next(iter(templates), "")
    return key, templates.get(key, {})


def pick_masthead(manifest: dict[str, Any], template: dict[str, Any]) -> tuple[str | None, str | None]:
    explicit = manifest.get("masthead_asset")
    if explicit:
        names = [str(name).upper() for name in template.get("masthead_names") or []]
        assets = [str(path) for path in template.get("masthead_assets") or []]
        name = None
        if str(explicit) in assets:
            name = names[assets.index(str(explicit)) % len(names)] if names else None
        return str(explicit), name
    real_assets = [
        str(path)
        for path in template.get("real_masthead_assets") or []
        if resolve_asset(SKILL_ROOT, str(path)).exists()
    ]
    historical_assets = [
        str(path)
        for path in template.get("historical_masthead_assets") or []
        if resolve_asset(SKILL_ROOT, str(path)).exists()
    ]
    fallback_assets = [str(path) for path in template.get("masthead_assets") or []]
    preferred_assets = real_assets or historical_assets
    assets = preferred_assets or fallback_assets
    if not assets:
        return None, None
    names = [str(name).upper() for name in template.get("masthead_names") or []]
    real_name = str(template.get("real_masthead_name") or "").upper() or None
    masthead = str(manifest.get("masthead") or "").upper()
    using_fallback_assets = not preferred_assets
    if using_fallback_assets and masthead and masthead in names:
        index = names.index(masthead)
        return assets[index % len(assets)], real_name or names[index]
    index = manifest.get("masthead_index")
    if index is not None:
        chosen = int(index) % len(assets)
    elif manifest.get("masthead_seed") is not None:
        chosen = random.Random(int(manifest["masthead_seed"])).randrange(len(assets))
    else:
        chosen = random.SystemRandom().randrange(len(assets))
    name = real_name or (names[chosen % len(names)] if using_fallback_assets and names else None)
    return assets[chosen], name


def paste_asset(
    canvas: Image.Image,
    base_dir: Path,
    asset_path: str | None,
    box: tuple[int, int, int, int],
    recolor: bool = False,
    ink: str = "#000000",
    paper: str | None = None,
) -> tuple[int, int, int, int] | None:
    if not asset_path:
        return None
    path = resolve_asset(base_dir, asset_path)
    if not path.exists():
        return None
    image = load_rgba(path)
    if recolor:
        image = recolor_asset(image, ink, paper)
    return paste_contained(canvas, image, box)


def draw_style_ornaments(
    page: Image.Image,
    style_key: str,
    ink: str,
    accent: str,
    muted: str,
    margin: int,
    header_h: int,
    lower_y: int,
) -> None:
    draw = ImageDraw.Draw(page)
    w, h = page.size
    if style_key == "france":
        for x in (margin + 8, w - margin - 42):
            draw.arc((x, margin + 10, x + 34, margin + 44), 90, 360, fill=color(accent), width=2)
            draw.arc((x, header_h - 34, x + 34, header_h), 180, 450, fill=color(muted), width=1)
    elif style_key == "united-states":
        chip_w = max(28, (w - margin * 2) // 14)
        for i, label in enumerate(["NEWS", "MONEY", "SPORT", "LIFE"]):
            x = margin + i * (chip_w + 8)
            draw.rectangle((x, margin + 4, x + chip_w, margin + 15), outline=color(ink), fill=color(accent if i == 0 else muted))
            draw_pixel_text(page, (x + 4, margin + 7), label, 1, ink if i else "#ffffff", chip_w - 6, 1, "bold")
    elif style_key == "japan":
        for i in range(7):
            x = w - margin - 16 - i * 12
            draw.line((x, lower_y, x, min(h - margin, lower_y + 92)), fill=color(muted), width=1)
            for y in range(lower_y + 4, min(h - margin - 6, lower_y + 86), 10):
                draw.rectangle((x - 2, y, x + 2, y + 5), fill=color(accent if (i + y) % 3 == 0 else ink))
    elif style_key == "china":
        draw.rectangle((margin, margin + 4, w - margin, margin + 13), fill=color(accent))
        for i in range(6):
            x = margin + i * ((w - margin * 2) // 6)
            draw.line((x, lower_y, x, h - margin), fill=color(muted), width=1)
    elif style_key == "hong-kong":
        draw.rectangle((margin, header_h - 16, w - margin, header_h - 5), outline=color(accent), width=2)
        for i in range(8):
            x = margin + 10 + i * 42
            if x < w - margin - 20:
                draw.rectangle((x, header_h - 13, x + 22, header_h - 8), fill=color(accent if i % 2 else muted))
    elif style_key == "korea":
        ring_colors = [accent, "#214aa5", "#38aeea", "#15945f", muted]
        for i, ring in enumerate(ring_colors):
            x = margin + 10 + i * 18
            draw.ellipse((x, margin + 5, x + 12, margin + 17), outline=color(ring), width=2)


def add_paper_texture(image: Image.Image, ink: str, seed: int, amount: int) -> None:
    rng = random.Random(seed)
    texture = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(texture)
    rgba = color(ink)
    for _ in range(amount):
        x = rng.randrange(image.width)
        y = rng.randrange(image.height)
        if rng.random() < 0.65:
            draw.point((x, y), fill=(rgba[0], rgba[1], rgba[2], 38))
    image.alpha_composite(texture)


def apply_aged_newspaper_filter(
    image: Image.Image,
    seed: int,
    paper: str,
    ink: str,
    strength: float = 1.0,
) -> Image.Image:
    if strength <= 0:
        return image
    rng = random.Random(seed + 7919)
    result = image.convert("RGBA")
    paper_rgba = color(paper)
    ink_rgba = color(ink)
    w, h = result.size

    wash = Image.new("RGBA", (w, h), (paper_rgba[0], max(0, paper_rgba[1] - 10), max(0, paper_rgba[2] - 28), int(24 * strength)))
    result.alpha_composite(wash)

    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = vignette.load()
    cx = (w - 1) / 2
    cy = (h - 1) / 2
    max_dist = max(1.0, (cx * cx + cy * cy) ** 0.5)
    for y in range(h):
        for x in range(w):
            dist = (((x - cx) ** 2 + (y - cy) ** 2) ** 0.5) / max_dist
            if dist > 0.60:
                alpha = int((dist - 0.60) / 0.40 * 34 * strength)
                px[x, y] = (92, 65, 28, min(48, max(0, alpha)))
    result.alpha_composite(vignette)

    stains = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(stains)
    for _ in range(max(8, (w * h) // 95_000)):
        rx = rng.randrange(w)
        ry = rng.randrange(h)
        rw = rng.randrange(max(8, w // 90), max(10, w // 28))
        rh = rng.randrange(max(6, h // 120), max(8, h // 45))
        alpha = rng.randrange(7, max(8, int(24 * strength)))
        draw.ellipse((rx - rw, ry - rh, rx + rw, ry + rh), fill=(116, 82, 38, alpha))
    for _ in range(max(450, w * h // 1100)):
        x = rng.randrange(w)
        y = rng.randrange(h)
        if rng.random() < 0.72:
            rgba = (ink_rgba[0], ink_rgba[1], ink_rgba[2], rng.randrange(10, max(12, int(36 * strength))))
        else:
            rgba = (255, 246, 214, rng.randrange(10, max(12, int(30 * strength))))
        draw.point((x, y), fill=rgba)
    result.alpha_composite(stains)
    return result


def apply_retro_print_filter(
    image: Image.Image,
    seed: int,
    paper: str,
    ink: str,
    accent: str,
    strength: float = 0.55,
    mode: str = "belle-epoque-print",
) -> Image.Image:
    mode = str(mode or "").strip().lower()
    if strength <= 0 or mode in {"", "off", "none", "false"}:
        return image
    rng = random.Random(seed + 15485863)
    strength = max(0.0, min(1.25, strength))
    result = image.convert("RGBA")
    w, h = result.size
    paper_rgba = color(paper)
    ink_rgba = color(ink)
    accent_rgba = color(accent)

    split = result.split()
    shift = max(1, round(min(w, h) * 0.0012 * strength))
    if shift > 0:
        r = ImageChops.offset(split[0], shift, 0)
        g = split[1]
        b = ImageChops.offset(split[2], -shift, 0)
        shifted = Image.merge("RGBA", (r, g, b, split[3]))
        result = Image.blend(result, shifted, min(0.22, 0.18 * strength))

    tone = Image.new(
        "RGBA",
        (w, h),
        (
            min(255, paper_rgba[0] + 8),
            max(0, paper_rgba[1] - 5),
            max(0, paper_rgba[2] - 20),
            int(18 * strength),
        ),
    )
    result.alpha_composite(tone)

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(0, h, 4):
        alpha = int((5 + (y // 4) % 2 * 3) * strength)
        draw.line((0, y, w, y), fill=(ink_rgba[0], ink_rgba[1], ink_rgba[2], alpha), width=1)
    for x in range(0, w, 6):
        alpha = int(3 * strength)
        draw.line((x, 0, x, h), fill=(255, 250, 230, alpha), width=1)

    fold_count = 1 + (1 if strength > 0.75 else 0)
    fold_xs = [w // 2]
    if fold_count > 1:
        fold_xs.append(w * 7 // 10)
    for fx in fold_xs:
        draw.line((fx, 0, fx, h), fill=(255, 245, 212, int(22 * strength)), width=max(1, w // 520))
        draw.line((min(w - 1, fx + max(1, w // 360)), 0, min(w - 1, fx + max(1, w // 360)), h), fill=(92, 62, 34, int(13 * strength)), width=1)
    fy = h // 2 + rng.randrange(-max(1, h // 24), max(2, h // 24))
    draw.line((0, fy, w, fy), fill=(255, 245, 212, int(13 * strength)), width=1)
    draw.line((0, min(h - 1, fy + 1), w, min(h - 1, fy + 1)), fill=(92, 62, 34, int(7 * strength)), width=1)

    for _ in range(max(12, int((w * h) / 65_000 * strength))):
        sx = rng.randrange(w)
        sy = rng.randrange(h)
        length = rng.randrange(max(5, w // 110), max(7, w // 36))
        if rng.random() < 0.55:
            draw.line((sx, sy, min(w - 1, sx + length), sy + rng.choice([-1, 0, 1])), fill=(255, 246, 220, rng.randrange(18, max(19, int(44 * strength)))), width=1)
        else:
            draw.line((sx, sy, min(w - 1, sx + length), sy), fill=(ink_rgba[0], ink_rgba[1], ink_rgba[2], rng.randrange(8, max(9, int(24 * strength)))), width=1)

    edge = max(2, min(w, h) // 90)
    for i in range(edge):
        alpha = int((1 - i / max(1, edge)) * 24 * strength)
        draw.rectangle((i, i, w - 1 - i, h - 1 - i), outline=(92, 62, 34, alpha), width=1)
    for _ in range(max(24, int((w + h) / 18 * strength))):
        side = rng.randrange(4)
        if side == 0:
            x, y = rng.randrange(w), rng.randrange(max(1, edge * 2))
        elif side == 1:
            x, y = rng.randrange(w), h - 1 - rng.randrange(max(1, edge * 2))
        elif side == 2:
            x, y = rng.randrange(max(1, edge * 2)), rng.randrange(h)
        else:
            x, y = w - 1 - rng.randrange(max(1, edge * 2)), rng.randrange(h)
        radius = rng.randrange(1, max(2, min(w, h) // 180))
        draw.rectangle((x - radius, y - radius, x + radius, y + radius), fill=(paper_rgba[0], paper_rgba[1], paper_rgba[2], rng.randrange(22, max(23, int(58 * strength)))))

    if mode in {"belle-epoque-print", "chromolithograph"}:
        for _ in range(max(10, int((w * h) / 90_000 * strength))):
            rx = rng.randrange(w)
            ry = rng.randrange(h)
            rw = rng.randrange(max(5, w // 160), max(7, w // 55))
            rh = rng.randrange(max(3, h // 190), max(5, h // 70))
            tint = accent_rgba if rng.random() < 0.45 else ink_rgba
            draw.ellipse((rx - rw, ry - rh, rx + rw, ry + rh), fill=(tint[0], tint[1], tint[2], rng.randrange(4, max(5, int(14 * strength)))))

    result.alpha_composite(overlay)
    sharp = result.filter(ImageFilter.UnsharpMask(radius=0.6, percent=int(35 * strength), threshold=2))
    return Image.blend(result, sharp, min(0.45, 0.22 * strength))


def paste_contained(canvas: Image.Image, image: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x, y, w, h = box
    fitted = ImageOps.contain(image, (w, h), Image.Resampling.NEAREST)
    px = x + (w - fitted.width) // 2
    py = y + (h - fitted.height) // 2
    canvas.alpha_composite(fitted, (px, py))
    return (px, py, fitted.width, fitted.height)


def scale_box(box: tuple[int, int, int, int] | list[int], factor: int) -> list[int]:
    return [int(value) * factor for value in box]


def paste_ad_image(
    canvas: Image.Image,
    image: Image.Image,
    box: tuple[int, int, int, int],
    align: str = "left",
) -> tuple[int, int, int, int]:
    x, y, w, h = box
    image = trim_transparent(image)
    if image.width <= 0 or image.height <= 0:
        return box
    fitted = ImageOps.contain(image, (w, h), Image.Resampling.NEAREST)
    if align == "right":
        px = x + w - fitted.width
    elif align == "center":
        px = x + (w - fitted.width) // 2
    else:
        px = x
    py = y + (h - fitted.height) // 2
    canvas.alpha_composite(fitted, (px, py))
    return (px, py, fitted.width, fitted.height)


def ad_image_size(base_dir: Path, ad_value: Any) -> tuple[int, int] | None:
    if not ad_value:
        return None
    asset = ad_value.get("path") if isinstance(ad_value, dict) else ad_value
    path = resolve_asset(base_dir, str(asset))
    if not path.exists():
        return None
    with Image.open(path) as image:
        return image.size


def ad_aspect(base_dir: Path, ad_value: Any) -> str:
    explicit = ""
    if isinstance(ad_value, dict):
        explicit = str(ad_value.get("aspect") or ad_value.get("target_aspect") or "").lower()
    if explicit in {"wide", "tall", "square"}:
        return explicit
    size = ad_image_size(base_dir, ad_value)
    if not size:
        return "square"
    w, h = size
    ratio = w / max(1, h)
    if ratio >= 1.45:
        return "wide"
    if ratio <= 0.78:
        return "tall"
    return "square"


def box_aspect(box: tuple[int, int, int, int]) -> str:
    ratio = box[2] / max(1, box[3])
    if ratio >= 1.45:
        return "wide"
    if ratio <= 0.78:
        return "tall"
    return "square"


def ordered_ad_values(manifest: dict[str, Any], template: dict[str, Any]) -> list[Any]:
    ad_paths = list(manifest.get("ads", []))
    default_ads = list(template.get("default_ad_assets") or [])
    target_count = max(
        len(ad_paths),
        int(manifest.get("ad_count") or manifest.get("ad_placeholders") or template.get("ad_default", 4)),
        0,
    )
    use_static_ads = bool(manifest.get("use_static_ads", template.get("use_static_ads_default", False)))
    while use_static_ads and default_ads and len(ad_paths) < target_count:
        ad_paths.append(default_ads[len(ad_paths) % len(default_ads)])
    return ad_paths


def ad_slots_from_specs(
    specs: list[Any],
    page_width: int,
    page_height: int,
    margin: int,
) -> list[dict[str, Any]]:
    slots: list[dict[str, Any]] = []
    for spec in specs:
        if not isinstance(spec, dict):
            continue
        box = rect_from_layout(spec, page_width, page_height, margin)
        if box[2] < 70 or box[3] < 56:
            continue
        slots.append(
            {
                "aspect": str(spec.get("aspect") or box_aspect(box)),
                "box": box,
                "priority": int(spec.get("priority", len(slots))),
            }
        )
    return sorted(slots, key=lambda item: item.get("priority", 0))


def distributed_ad_slots(
    ad_slot: tuple[int, int, int, int] | None,
    positions: list[tuple[int, int, int, int]],
    manifest: dict[str, Any],
    template: dict[str, Any],
    page_width: int,
    page_height: int,
    margin: int,
) -> list[dict[str, Any]]:
    specs = manifest.get("floating_ad_slots") or template.get("floating_ad_slots") or []
    if isinstance(specs, list) and specs:
        slots = ad_slots_from_specs(specs, page_width, page_height, margin)
        if slots:
            return slots
    slots = [{"aspect": box_aspect(position), "box": position, "priority": index} for index, position in enumerate(positions)]
    if ad_slot and not slots:
        slots = [{"aspect": box_aspect(ad_slot), "box": ad_slot, "priority": 0}]
    return slots


def fit_source_box(
    source: Image.Image,
    max_box: tuple[int, int],
    target_scale: float,
) -> tuple[int, int]:
    max_w, max_h = max_box
    target_w = max(1, round(source.width * target_scale))
    target_h = max(1, round(source.height * target_scale))
    factor = min(max_w / target_w, max_h / target_h, 1.0)
    return max(1, round(target_w * factor)), max(1, round(target_h * factor))


def rect_from_layout(layout: dict[str, Any], page_width: int, page_height: int, margin: int) -> tuple[int, int, int, int]:
    x = margin + round(float(layout.get("x", 0)) * (page_width - margin * 2))
    y = margin + round(float(layout.get("y", 0)) * (page_height - margin * 2))
    w = round(float(layout.get("w", 1)) * (page_width - margin * 2))
    h = round(float(layout.get("h", 1)) * (page_height - margin * 2))
    return x, y, max(1, w), max(1, h)


def draw_column_rules(
    draw: ImageDraw.ImageDraw,
    content_box: tuple[int, int, int, int],
    columns: int,
    gap: int,
    ink: str,
    muted: str,
) -> None:
    x, y, w, h = content_box
    if columns <= 1:
        return
    col_w = (w - gap * (columns - 1)) // columns
    for i in range(1, columns):
        rx = x + i * col_w + (i - 1) * gap + gap // 2
        draw.line((rx, y, rx, y + h), fill=color(muted), width=1)
    draw.rectangle((x, y, x + w, y + h), outline=color(ink), width=1)


def draw_staggered_text_blocks(
    page: Image.Image,
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    lines: list[str],
    snippet_count: int,
    scale: int,
    ink: str,
    accent: str,
    muted: str,
    columns: int,
) -> None:
    x, y, w, h = box
    if not lines or w <= 0 or h <= 0:
        return
    columns = max(1, min(columns, len(lines), 4))
    gap = max(10, min(24, w // 26))
    col_w = max(40, (w - gap * (columns - 1)) // columns)
    step_y = max(30, text_height(2, scale) + 10)
    offsets = [0, max(6, 8 * scale), max(4, 4 * scale), max(10, 12 * scale)]
    max_items = max(columns, columns * max(1, h // step_y))
    for index, line in enumerate(lines[:max_items]):
        col = index % columns
        row = index // columns
        bx = x + col * (col_w + gap)
        by = y + offsets[col % len(offsets)] + row * step_y
        if by > y + h - 10:
            continue
        weight = "regular" if index < snippet_count else "thin"
        line_fill = ink if index < snippet_count else paper_safe(ink)
        rule_fill = accent if index < snippet_count else muted
        draw.line((bx, by, bx + min(col_w, max(28, col_w - 8)), by), fill=color(rule_fill), width=1)
        draw.line((bx, by, bx, min(y + h, by + step_y - 6)), fill=color(muted), width=1)
        draw_pixel_text(page, (bx + 6, by + 6), line, scale, line_fill, col_w - 8, 2, weight)


def draw_snippet_area(
    page: Image.Image,
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    snippets: list[str],
    reports: list[str],
    template: dict[str, Any],
    scale: int,
    ink: str,
    accent: str,
    muted: str,
) -> None:
    lines = [*snippets, *reports]
    if not lines:
        return
    style = str(template.get("snippet_style") or "stacked")
    if style == "staggered-columns":
        draw_staggered_text_blocks(
            page,
            draw,
            box,
            lines,
            len(snippets),
            scale,
            ink,
            accent,
            muted,
            int(template.get("snippet_columns") or 3),
        )
        return
    x, y, w, h = box
    yy = y
    for index, snippet in enumerate(lines[:8]):
        if yy > y + h - 12:
            break
        weight = "regular" if index < len(snippets) else "thin"
        draw_pixel_text(page, (x, yy), snippet, scale, ink, w, 1, weight)
        yy += 11 * scale
        draw_rule(draw, (x, yy, x + w, yy + 1), muted)
        yy += 5


def draw_side_note_area(
    page: Image.Image,
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    lines: list[str],
    scale: int,
    ink: str,
    accent: str,
    muted: str,
) -> None:
    x, y, w, h = box
    if not lines or w <= 0 or h <= 0:
        return
    draw.rectangle((x, y, x + w, y + h), outline=color(ink), width=1)
    yy = y + 8
    for index, line in enumerate(lines[:5]):
        if yy > y + h - 26:
            break
        inset = 8 + (index % 2) * max(0, min(16, w // 12))
        rule_w = max(28, w - inset - 10 - (index % 3) * max(0, min(22, w // 10)))
        draw.line((x + inset, yy, x + inset + rule_w, yy), fill=color(accent if index % 2 == 0 else muted), width=1)
        draw_pixel_text(page, (x + inset, yy + 7), line, scale, ink, w - inset - 10, 2, "regular")
        yy += max(34, text_height(2, scale) + 12)


def draw_text_block(
    page: Image.Image,
    xy: tuple[int, int],
    paragraphs: list[str],
    scale: int,
    fill: str,
    max_width: int,
    max_y: int,
    max_lines_per_paragraph: int = 3,
    weight: str = "thin",
    paragraph_gap: int = 6,
) -> int:
    x, y = xy
    for paragraph in paragraphs:
        if y >= max_y:
            break
        lines = wrap_text(paragraph, max_width, scale, max_lines_per_paragraph)
        block_h = text_height(len(lines), scale)
        if y + block_h > max_y:
            remaining = max(1, (max_y - y) // max(1, line_step(scale, weight)))
            lines = lines[:remaining]
            block_h = text_height(len(lines), scale)
        draw_pixel_text(page, (x, y), lines, scale, fill, max_width, weight=weight)
        y += block_h + paragraph_gap
    return y


def subtract_interval(
    segments: list[tuple[int, int]],
    start: int,
    end: int,
    min_width: int,
) -> list[tuple[int, int]]:
    output: list[tuple[int, int]] = []
    for x, w in segments:
        seg_start = x
        seg_end = x + w
        if end <= seg_start or start >= seg_end:
            output.append((x, w))
            continue
        if start - seg_start >= min_width:
            output.append((seg_start, start - seg_start))
        if seg_end - end >= min_width:
            output.append((end, seg_end - end))
    return output


def line_segments_avoiding_boxes(
    x: int,
    y: int,
    w: int,
    line_y: int,
    line_h: int,
    obstacles: list[tuple[int, int, int, int]],
    pad: int,
    min_width: int,
) -> list[tuple[int, int]]:
    segments = [(x, w)]
    for ox, oy, ow, oh in obstacles:
        if line_y + line_h < oy - pad or line_y > oy + oh + pad:
            continue
        segments = subtract_interval(segments, ox - pad, ox + ow + pad, min_width)
        if not segments:
            break
    return segments


def padded_box(box: tuple[int, int, int, int], pad: int) -> tuple[int, int, int, int]:
    x, y, w, h = box
    return (x - pad, y - pad, w + pad * 2, h + pad * 2)


def boxes_intersect(
    a: tuple[int, int, int, int],
    b: tuple[int, int, int, int],
    pad: int = 0,
) -> bool:
    ax, ay, aw, ah = padded_box(a, pad)
    bx, by, bw, bh = b
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def box_collides(
    candidate: tuple[int, int, int, int],
    boxes: list[tuple[int, int, int, int]],
    pad: int,
) -> bool:
    return any(boxes_intersect(candidate, box, pad) for box in boxes)


def text_line_box(text: str, x: int, y: int, scale: int, weight: str = "regular") -> tuple[int, int, int, int]:
    text_w, text_h = measure_text([text], scale)
    line_h = max(text_h, line_step(scale, weight))
    return (x, y, text_w, line_h)


def draw_vertical_rule_avoiding_boxes(
    draw: ImageDraw.ImageDraw,
    x: int,
    y0: int,
    y1: int,
    fill: str,
    obstacles: list[tuple[int, int, int, int]],
    pad: int,
) -> None:
    blocked: list[tuple[int, int]] = []
    for ox, oy, ow, oh in obstacles:
        if ox - pad <= x <= ox + ow + pad:
            blocked.append((max(y0, oy - pad), min(y1, oy + oh + pad)))
    if not blocked:
        draw.line((x, y0, x, y1), fill=color(fill), width=1)
        return
    blocked.sort()
    cursor = y0
    for start, end in blocked:
        if start > cursor + 3:
            draw.line((x, cursor, x, start), fill=color(fill), width=1)
        cursor = max(cursor, end)
    if cursor < y1 - 3:
        draw.line((x, cursor, x, y1), fill=color(fill), width=1)


def repeat_to_fill(lines: list[str], target: int) -> list[str]:
    usable = [line for line in lines if str(line).strip()]
    if not usable:
        return []
    filled = list(usable)
    cursor = 0
    while len(filled) < target:
        filled.append(usable[cursor % len(usable)])
        cursor += 1
    return filled


def short_text_fragments(lines: list[str], max_chars: int = 48) -> list[str]:
    fragments: list[str] = []
    for raw in lines:
        text = " ".join(str(raw).replace(" - ", " ").split())
        if not text:
            continue
        if len(text) <= max_chars:
            fragments.append(text)
            continue
        words = text.split()
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    fragments.append(current)
                current = word
        if current:
            fragments.append(current)
    return fragments


def paragraph_texts(lines: list[str], target: int = 10, min_chars: int = 155) -> list[str]:
    source: list[str] = []
    for line in lines:
        text = " ".join(str(line).replace(" - ", ", ").split())
        if not text:
            continue
        alpha = [ch for ch in text if ch.isalpha()]
        upperish = bool(alpha) and sum(1 for ch in alpha if ch.upper() == ch) / len(alpha) > 0.82
        if upperish and len(text) < 36:
            continue
        if text[-1] not in ".。！？!?":
            text = f"{text}."
        source.append(text)
    if not source:
        return []
    paragraphs: list[str] = []
    index = 0
    while len(paragraphs) < target:
        group: list[str] = []
        used = 0
        while used < min(5, max(1, len(source))) and (not group or sum(len(part) for part in group) < min_chars):
            group.append(source[(index + used) % len(source)])
            used += 1
        paragraph = " ".join(group)
        paragraph = "".join(ch for ch in paragraph.lstrip() if not ch.isdigit()).lstrip(" ,-:;")
        if paragraph:
            paragraphs.append(paragraph)
        index += max(1, used)
    return paragraphs


def newspaper_paragraphs(manifest: dict[str, Any], locale: dict[str, Any] | None = None) -> list[str]:
    values = (
        manifest.get("newspaper_paragraphs")
        or manifest.get("article_paragraphs")
        or manifest.get("story_paragraphs")
        or manifest.get("report_paragraphs")
        or manifest.get("paragraphs")
        or []
    )
    if isinstance(values, str):
        values = [values]
    paragraphs: list[str] = []
    for item in values:
        if isinstance(item, dict):
            value = item.get("paragraph") or item.get("body") or item.get("text") or item.get("note")
            if value:
                paragraphs.append(str(value))
        elif item:
            paragraphs.append(str(item))
    if paragraphs:
        average = sum(len(text.strip()) for text in paragraphs) / max(1, len(paragraphs))
        if average < 125:
            return paragraph_texts(paragraphs, max(6, min(10, len(paragraphs))), 170)
        return paragraphs
    expanded: list[str] = []
    for item in manifest.get("secondary_events") or []:
        if isinstance(item, dict):
            body = item.get("paragraph") or item.get("body") or item.get("expanded_note") or item.get("note")
            headline = item.get("headline") or item.get("title")
            year = item.get("date") or item.get("year")
            text = " ".join(str(part) for part in (year, headline, body) if part)
            if text:
                expanded.append(text)
    return paragraph_texts([*report_lines(manifest, locale), *expanded, str(manifest.get("event") or "")], 10)


def split_drop_cap(text: str) -> tuple[str, str]:
    stripped = str(text).strip()
    if not stripped:
        return "", ""
    return stripped[0], stripped[1:].lstrip()


def draw_drop_cap_paragraph(
    page: Image.Image,
    xy: tuple[int, int],
    paragraph: str,
    scale: int,
    fill: str,
    max_width: int,
    max_y: int,
    weight: str = "regular",
) -> int:
    x, y = xy
    drop, rest = split_drop_cap(paragraph)
    if not drop or y >= max_y:
        return y
    drop_scale = max(scale + 1, scale * 2)
    drop_w, drop_h = measure_text([drop], drop_scale)
    draw_pixel_text(page, (x, y), drop, drop_scale, fill, max_width, 1, "bold")
    first_width = max(1, max_width - drop_w - max(4, scale * 4))
    first_lines = wrap_text(rest, first_width, scale, 2)
    draw_pixel_text(page, (x + drop_w + max(4, scale * 4), y), first_lines, scale, fill, first_width, 2, weight)
    used_chars = len(" ".join(first_lines))
    remainder = rest[used_chars:].lstrip(" .,;:")
    cursor_y = y + max(drop_h, text_height(len(first_lines), scale)) + max(2, scale * 2)
    if remainder and cursor_y < max_y:
        rest_lines = wrap_text(remainder, max_width, scale, 4)
        remaining = max(1, (max_y - cursor_y) // max(1, line_step(scale, weight)))
        rest_lines = rest_lines[:remaining]
        draw_pixel_text(page, (x, cursor_y), rest_lines, scale, fill, max_width, weight=weight)
        cursor_y += text_height(len(rest_lines), scale)
    return cursor_y + max(4, scale * 4)


def take_wrapped_line(text: str, max_width: int, scale: int) -> tuple[str, str]:
    source = str(text).strip()
    if not source:
        return "", ""
    if not use_bitmap_text(source):
        has_spaces = any(ch.isspace() for ch in source)
        units = source.split() if has_spaces else list(source)
        separator = " " if has_spaces else ""
        current = ""
        consumed_units = 0
        for unit in units:
            candidate = unit if not current else f"{current}{separator}{unit}"
            if measure_text([candidate], scale)[0] <= max_width or not current:
                current = candidate
                consumed_units += 1
                continue
            break
        if not current:
            return source[:1], source[1:].lstrip()
        if has_spaces:
            return current, " ".join(units[consumed_units:]).lstrip()
        return current, "".join(units[consumed_units:]).lstrip()
    units = normalize_text(source).split()
    current = ""
    consumed_units = 0
    for unit in units:
        candidate = unit if not current else f"{current} {unit}"
        if measure_text([candidate], scale)[0] <= max_width or not current:
            current = candidate
            consumed_units += 1
            continue
        break
    return current, " ".join(units[consumed_units:]).lstrip()


def flow_prepared_paragraphs_around_boxes(
    page: Image.Image,
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    paragraphs: list[str],
    scale: int,
    fill: str,
    muted: str,
    obstacles: list[tuple[int, int, int, int]] | None = None,
    columns: int = 3,
    repeat_target: int = 8,
    drop_cap_every: int = 2,
    drop_cap_limit: int = 1,
) -> None:
    x, y, w, h = box
    if not paragraphs or w <= 0 or h <= 0:
        return
    paragraphs = [text for text in paragraphs if str(text).strip()]
    if len(paragraphs) < 3:
        paragraphs = repeat_to_fill(paragraphs, 3)
    if not paragraphs:
        return
    obstacles = obstacles or []
    columns = max(1, min(columns, 4))
    gap = max(10, min(18, w // 34))
    col_w = max(40, (w - gap * (columns - 1)) // columns)
    line_h = max(10, line_step(scale, "regular") + max(3, scale * 3))
    min_segment_width = max(96, min(138, round(col_w * 0.62)))
    paragraph_index = 0
    remaining = paragraphs[0]
    at_paragraph_start = True
    drop_caps_drawn = 0

    flow_bottom = y + h - max(10, line_h)
    min_remaining_after_line = max(12, line_h)
    obstacle_pad = max(10, scale * 8)
    collision_pad = max(1, scale)
    occupied_boxes = list(obstacles)
    for col in range(columns):
        cx = x + col * (col_w + gap)
        yy = y
        if col > 0:
            rule_x = cx - gap // 2
            draw_vertical_rule_avoiding_boxes(draw, rule_x, y, y + h, muted, obstacles, obstacle_pad)
        skipped_rows = 0
        while yy + line_h + min_remaining_after_line <= flow_bottom and paragraph_index < len(paragraphs):
            segments = line_segments_avoiding_boxes(
                cx,
                y,
                col_w,
                yy,
                line_h,
                obstacles,
                obstacle_pad,
                min_segment_width,
            )
            if not segments:
                yy += line_h
                skipped_rows += 1
                if skipped_rows > 8:
                    break
                continue
            while not remaining.strip() and paragraph_index < len(paragraphs):
                paragraph_index += 1
                if paragraph_index < len(paragraphs):
                    remaining = paragraphs[paragraph_index]
                    at_paragraph_start = True
                    yy += max(3, scale * 3)
            if paragraph_index >= len(paragraphs):
                break
            usable_segments = [(sx, sw) for sx, sw in segments if sw >= min_segment_width]
            if not usable_segments:
                yy += line_h
                skipped_rows += 1
                if skipped_rows > 8:
                    break
                continue
            usable_segments = sorted(usable_segments, key=lambda item: item[1], reverse=True)
            wrote = False
            sx, sw = usable_segments[0]
            can_drop = (
                at_paragraph_start
                and paragraph_index % max(1, drop_cap_every) == 0
                and drop_caps_drawn < max(0, drop_cap_limit)
                and sw >= max(118, min_segment_width + 36)
                and yy + line_h * 2 <= flow_bottom
            )
            if can_drop:
                drop, rest = split_drop_cap(remaining)
                if drop:
                    drop_scale = max(scale + 1, scale * 2)
                    drop_w, drop_h = measure_text([drop], drop_scale)
                    rest_x = sx + drop_w + max(6, scale * 6)
                    rest_w = max(1, sw - drop_w - max(6, scale * 6))
                    line, rest_remaining = take_wrapped_line(rest, rest_w, scale)
                    line_w, line_text_h = measure_text([line], scale) if line else (0, 0)
                    candidate_h = max(drop_h, line_h * 2, line_text_h)
                    candidate_w = min(sw, max(drop_w, drop_w + max(6, scale * 6) + line_w))
                    candidate_box = (sx, yy, candidate_w, candidate_h)
                    if yy + candidate_h <= flow_bottom and not box_collides(candidate_box, occupied_boxes, collision_pad):
                        draw_pixel_text(page, (sx, yy), drop, drop_scale, fill, sw, 1, "bold")
                        if line:
                            draw_pixel_text(page, (rest_x, yy), line, scale, fill, rest_w, 1, "regular")
                        occupied_boxes.append(candidate_box)
                        remaining = rest_remaining
                        at_paragraph_start = False
                        drop_caps_drawn += 1
                        yy += candidate_h + max(6, scale * 6)
                        wrote = True
                        skipped_rows = 0
            if not wrote:
                for sx, sw in usable_segments:
                    line, rest_remaining = take_wrapped_line(remaining, sw, scale)
                    if not line:
                        continue
                    candidate_box = text_line_box(line, sx, yy, scale, "regular")
                    candidate_box = (candidate_box[0], candidate_box[1], min(sw, candidate_box[2]), max(line_h, candidate_box[3]))
                    if yy + candidate_box[3] > flow_bottom or box_collides(candidate_box, occupied_boxes, collision_pad):
                        continue
                    draw_pixel_text(page, (sx, yy), line, scale, fill, sw, 1, "regular")
                    occupied_boxes.append(candidate_box)
                    remaining = rest_remaining
                    at_paragraph_start = False
                    wrote = True
                    skipped_rows = 0
                    break
            if not wrote:
                yy += line_h
                skipped_rows += 1
                if skipped_rows > 8:
                    break
                continue
            if not remaining.strip():
                paragraph_index += 1
                if paragraph_index < len(paragraphs):
                    remaining = paragraphs[paragraph_index]
                    at_paragraph_start = True
                    if paragraph_index % 2 == 0 and yy + 3 < y + h:
                        rule_box = (cx, yy, col_w, 2)
                        if not box_collides(rule_box, occupied_boxes, collision_pad):
                            draw.line((cx, yy, cx + col_w, yy), fill=color(muted), width=1)
                            occupied_boxes.append(rule_box)
                            yy += max(3, scale * 3)
                else:
                    break
            else:
                yy += line_h + max(1, scale)


def flow_paragraphs_around_boxes(
    page: Image.Image,
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    lines: list[str],
    scale: int,
    fill: str,
    muted: str,
    obstacles: list[tuple[int, int, int, int]] | None = None,
    columns: int = 3,
    repeat_target: int = 18,
    preformatted: bool = False,
    drop_cap_every: int = 2,
) -> None:
    x, y, w, h = box
    if preformatted:
        paragraphs = []
        for line in lines:
            text = " ".join(str(line).split())
            if text:
                paragraphs.append(text)
        if len(paragraphs) < max(3, min(repeat_target, 8)):
            paragraphs = repeat_to_fill(paragraphs, max(3, min(repeat_target, 8)))
        flow_prepared_paragraphs_around_boxes(
            page,
            draw,
            box,
            paragraphs,
            scale,
            fill,
            muted,
            obstacles,
            columns,
            repeat_target,
            drop_cap_every,
            1,
        )
        return
    else:
        paragraphs = paragraph_texts(lines, repeat_target)
    if not paragraphs or w <= 0 or h <= 0:
        return
    obstacles = obstacles or []
    columns = max(1, min(columns, 4))
    gap = max(10, min(18, w // 34))
    col_w = max(40, (w - gap * (columns - 1)) // columns)
    cursor = 0
    line_h = max(8, line_step(scale, "regular"))
    for col in range(columns):
        cx = x + col * (col_w + gap)
        yy = y
        if col > 0:
            rule_x = cx - gap // 2
            draw.line((rule_x, y, rule_x, y + h), fill=color(muted), width=1)
        while yy + line_h <= y + h and cursor < len(paragraphs):
            segments = line_segments_avoiding_boxes(cx, y, col_w, yy, line_h * 6, obstacles, max(8, scale * 8), max(58, col_w // 2))
            if not segments:
                yy += line_h
                continue
            sx, sw = max(segments, key=lambda item: item[1])
            if sw < max(58, col_w // 2):
                yy += line_h
                continue
            if cursor % max(1, drop_cap_every) == 0:
                yy = draw_drop_cap_paragraph(page, (sx, yy), paragraphs[cursor], scale, fill, sw, y + h, "regular")
            else:
                yy = draw_text_block(
                    page,
                    (sx, yy),
                    [paragraphs[cursor]],
                    scale,
                    fill,
                    sw,
                    y + h,
                    6,
                    "regular",
                    max(4, scale * 4),
                )
            cursor += 1
            if cursor % 2 == 0 and yy + 3 < y + h:
                draw.line((sx, yy, sx + sw, yy), fill=color(muted), width=1)
                yy += max(3, scale * 2)


def flow_text_around_boxes(
    page: Image.Image,
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    lines: list[str],
    scale: int,
    fill: str,
    muted: str,
    obstacles: list[tuple[int, int, int, int]] | None = None,
    columns: int = 3,
    weight: str = "thin",
    min_segment_width: int = 56,
    repeat_target: int = 80,
) -> None:
    x, y, w, h = box
    if w <= 0 or h <= 0:
        return
    flow_lines = repeat_to_fill(short_text_fragments(lines, max(24, min(56, box[2] // max(1, columns) // 5))), repeat_target)
    if not flow_lines:
        return
    obstacles = obstacles or []
    columns = max(1, min(columns, 6))
    gap = max(8, min(18, w // 38))
    col_w = max(24, (w - gap * (columns - 1)) // columns)
    line_h = max(8, line_step(scale, weight))
    cursor = 0
    for col in range(columns):
        cx = x + col * (col_w + gap)
        if col > 0:
            rule_x = cx - gap // 2
            draw.line((rule_x, y, rule_x, y + h), fill=color(muted), width=1)
        yy = y
        row = 0
        while yy + line_h <= y + h and cursor < len(flow_lines) * 3:
            segments = line_segments_avoiding_boxes(cx, y, col_w, yy, line_h, obstacles, max(8, scale * 8), min_segment_width)
            if not segments:
                yy += line_h
                row += 1
                continue
            for sx, sw in segments:
                if sw < min_segment_width:
                    continue
                text = flow_lines[cursor % len(flow_lines)]
                draw_pixel_text(page, (sx, yy), text, scale, fill, sw, 1, weight)
                cursor += 1
                if row % 7 == 6 and sw > 70:
                    draw.line((sx, yy + line_h - 1, sx + sw, yy + line_h - 1), fill=color(muted), width=1)
            yy += line_h
            row += 1


def draw_micro_columns(
    page: Image.Image,
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    lines: list[str],
    scale: int,
    ink: str,
    accent: str,
    muted: str,
    columns: int,
    max_lines_per_item: int = 3,
) -> None:
    x, y, w, h = box
    if not lines or w <= 0 or h <= 0:
        return
    columns = max(1, min(columns, len(lines), 4))
    gap = max(8, min(18, w // 28))
    col_w = max(36, (w - gap * (columns - 1)) // columns)
    for col in range(columns):
        cx = x + col * (col_w + gap)
        cy = y + (col % 2) * max(0, 4 * scale)
        if col > 0:
            rule_x = cx - gap // 2
            draw.line((rule_x, y, rule_x, y + h), fill=color(muted), width=1)
        for index, line in enumerate(lines[col::columns]):
            if cy > y + h - max(16, line_step(scale)):
                break
            draw.line((cx, cy, cx + col_w, cy), fill=color(accent if index == 0 else muted), width=1)
            cy = draw_text_block(
                page,
                (cx, cy + 6),
                [line],
                scale,
                ink,
                col_w,
                y + h,
                max_lines_per_item,
                "thin",
                6,
            )


def draw_society_ad(
    page: Image.Image,
    draw: ImageDraw.ImageDraw,
    base_dir: Path,
    ad_value: Any,
    box: tuple[int, int, int, int],
    index: int,
    manifest: dict[str, Any],
    ink: str,
    accent: str,
    muted: str,
) -> tuple[int, int, int, int]:
    x, y, w, h = box
    ad_text = ad_text_for(index, ad_value, manifest)
    if ad_value:
        asset = ad_value.get("path") if isinstance(ad_value, dict) else ad_value
        path = resolve_asset(base_dir, str(asset))
        if path.exists():
            ad_img = load_rgba(path)
            pad = max(0, min(4, min(w, h) // 28))
            return paste_ad_image(page, ad_img, (x + pad, y + pad, max(1, w - pad * 2), max(1, h - pad * 2)), "left")

    draw_ad_frame(draw, box, ink, accent, muted, index)
    pad = max(6, min(12, w // 24))
    label = ad_text["label"]
    body = ad_text["body"]
    draw_pixel_text(page, (x + pad, y + pad), label, 1 if w < 220 else 2, ink, w - pad * 2, 1, "bold")
    yy = y + (18 if w < 220 else 28)
    if body:
        draw_pixel_text(page, (x + pad, yy), body, 1, accent, w - pad * 2, 3, "regular")
    icon_x = x + w // 2
    icon_y = y + h - max(18, h // 4)
    draw.rectangle((icon_x - 16, icon_y - 12, icon_x + 16, icon_y + 8), outline=color(ink), width=1)
    draw.line((icon_x - 12, icon_y + 10, icon_x + 12, icon_y + 10), fill=color(accent), width=1)
    return box


def choose_ad_for_slot(
    remaining: list[tuple[int, Any, str]],
    slot_aspect: str,
) -> tuple[int, Any, str] | None:
    if not remaining:
        return None
    for item in remaining:
        if item[2] == slot_aspect:
            remaining.remove(item)
            return item
    if slot_aspect == "wide":
        for item in remaining:
            if item[2] == "square":
                remaining.remove(item)
                return item
    if slot_aspect == "tall":
        for item in remaining:
            if item[2] == "square":
                remaining.remove(item)
                return item
    return remaining.pop(0)


def society_ad_slots(
    content_x: int,
    content_w: int,
    page_height: int,
    margin: int,
    article_y: int,
    article_h: int,
    story_w: int,
    gutter: int,
    image_x: int,
    image_y: int,
    image_w: int,
    image_h: int,
    lower_y: int,
    lower_h: int,
) -> list[dict[str, Any]]:
    bottom_h = max(78, min(round(page_height * 0.095), round(content_w * 0.135)))
    bottom_y = page_height - margin - bottom_h - round(page_height * 0.018)
    right_x = image_x + image_w + gutter // 2
    right_w = content_x + content_w - right_x
    slots: list[dict[str, Any]] = []
    if right_w >= max(110, content_w * 0.13):
        slots.append(
            {
                "aspect": "tall",
                "box": (
                    right_x,
                    article_y,
                    right_w,
                    min(article_h, max(92, bottom_y - article_y - 16)),
                ),
            }
        )
    compact = page_height <= 950
    if compact:
        mid_h = max(62, min(round(page_height * 0.078), round(content_w * 0.105)))
        mid_y = max(lower_y + 6, min(bottom_y - mid_h - 10, lower_y + max(8, round(lower_h * 0.18))))
        slots.extend(
            [
                {
                    "aspect": "wide",
                    "box": (
                        content_x,
                        mid_y,
                        round(content_w * 0.28),
                        mid_h,
                    ),
                },
                {
                    "aspect": "square",
                    "box": (
                        content_x + round(content_w * 0.33),
                        mid_y + round(mid_h * 0.12),
                        round(content_w * 0.21),
                        max(58, round(mid_h * 0.88)),
                    ),
                },
                {
                    "aspect": "wide",
                    "box": (
                        content_x + round(content_w * 0.64),
                        mid_y + round(mid_h * 0.05),
                        content_x + content_w - (content_x + round(content_w * 0.64)),
                        max(58, round(mid_h * 0.90)),
                    ),
                },
                {
                    "aspect": "square",
                    "box": (
                        content_x,
                        bottom_y + round(bottom_h * 0.02),
                        round(content_w * 0.26),
                        round(bottom_h * 0.95),
                    ),
                },
                {
                    "aspect": "wide",
                    "box": (
                        content_x + round(content_w * 0.30),
                        bottom_y + round(bottom_h * 0.09),
                        round(content_w * 0.31),
                        round(bottom_h * 0.86),
                    ),
                },
                {
                    "aspect": "wide",
                    "box": (
                        content_x + round(content_w * 0.64),
                        bottom_y + round(bottom_h * 0.14),
                        content_x + content_w - (content_x + round(content_w * 0.64)),
                        round(bottom_h * 0.80),
                    ),
                },
            ]
        )
    else:
        slots.extend(
            [
                {
                    "aspect": "square",
                    "box": (
                        content_x,
                        max(article_y + article_h + 12, lower_y),
                        min(story_w, round(content_w * 0.30)),
                        max(68, min(round(page_height * 0.12), lower_h)),
                    ),
                },
                {
                    "aspect": "wide",
                    "box": (
                        content_x + round(content_w * 0.32),
                        bottom_y - round(bottom_h * 0.22),
                        round(content_w * 0.31),
                        round(bottom_h * 1.10),
                    ),
                },
                {
                    "aspect": "wide",
                    "box": (
                        content_x + round(content_w * 0.67),
                        bottom_y + round(bottom_h * 0.08),
                        content_x + content_w - (content_x + round(content_w * 0.67)),
                        round(bottom_h * 0.92),
                    ),
                },
                {
                    "aspect": "square",
                    "box": (
                        content_x,
                        bottom_y + round(bottom_h * 0.04),
                        round(content_w * 0.28),
                        round(bottom_h * 0.96),
                    ),
                },
            ]
        )
    filtered: list[dict[str, Any]] = []
    for priority, slot in enumerate(slots):
        x, y, w, h = slot["box"]
        if w < 70 or h < 54:
            continue
        slot.setdefault("priority", priority)
        filtered.append(slot)
    return filtered


def render_society_broadsheet(
    base_dir: Path,
    manifest: dict[str, Any],
    text: dict[str, str],
    style_key: str,
    template: dict[str, Any],
    source_path: Path,
    source: Image.Image,
    seed: int,
    paper: str,
    ink: str,
    accent: str,
    muted: str,
    out_path: Path,
    preview_scale: int | None,
) -> dict[str, Any]:
    keep_page_size = bool(manifest.get("keep_page_size") or manifest.get("society_keep_page_size"))
    if keep_page_size and manifest.get("page_width"):
        page_width = int(manifest["page_width"])
    else:
        page_width = int(template.get("page_width") or round(source.width * float(template.get("page_width_ratio", 0.68))))
    if keep_page_size and manifest.get("page_height"):
        page_height = int(manifest["page_height"])
    else:
        page_height = int(template.get("page_height") or round(page_width * float(template.get("page_aspect_ratio", 1.30))))
    margin = page_margin(page_width, manifest, template, 0.036, 24, 0.040)
    page = Image.new("RGBA", (page_width, page_height), color(paper))
    draw = ImageDraw.Draw(page)
    add_paper_texture(page, ink, seed, max(200, page_width * page_height // 950))

    content_x = margin
    content_w = page_width - margin * 2
    small_scale = int(manifest.get("small_scale") or template.get("small_scale") or max(1, min(2, page_width // 760)))
    body_scale = int(manifest.get("body_scale") or template.get("body_scale") or max(1, min(2, page_width // 860)))
    section_scale = max(3, min(7, page_width // 245))
    title_scale = max(2, min(4, page_width // 520))

    masthead_asset, masthead_name = pick_masthead(manifest, template)
    if masthead_name:
        text["masthead"] = masthead_name
    locale = locale_for(style_key, manifest, template)
    set_active_font(str(locale.get("font_key") or "ascii-pixel"))

    draw_rule(draw, (content_x, margin, content_x + content_w, margin + 3), ink)
    masthead_box = (
        content_x,
        margin + round(page_height * 0.012),
        content_w,
        round(page_height * float(template.get("society_masthead_ratio", 0.115))),
    )
    masthead_paper = sample_box_color(page, masthead_box, paper)
    mx, my, mw, mh = masthead_box
    draw.rectangle((mx - 2, my - 2, mx + mw + 2, my + mh + 2), fill=color(masthead_paper))
    masthead_placed = paste_asset(page, base_dir, masthead_asset, masthead_box, True, ink, masthead_paper)
    if not masthead_placed:
        mast_lines = wrap_text(text["masthead"], content_w, max(3, min(8, page_width // 250)), 2)
        mast_w, _ = measure_text(mast_lines, max(3, min(8, page_width // 250)))
        draw_pixel_text(page, ((page_width - mast_w) // 2, my + 8), mast_lines, max(3, min(8, page_width // 250)), ink, weight="bold")
    mast_bottom = my + mh

    issue_y = mast_bottom + round(page_height * 0.012)
    draw_rule(draw, (content_x, issue_y - 8, content_x + content_w, issue_y - 6), ink)
    draw_rule(draw, (content_x, issue_y + text_height(1, small_scale) + 8, content_x + content_w, issue_y + text_height(1, small_scale) + 10), muted)
    left_issue = text["issue_line"]
    center_issue = str(manifest.get("edition_line") or locale.get("edition_line") or "BELLE EPOQUE EDITION")
    right_issue = str(manifest.get("date") or "")
    draw_pixel_text(page, (content_x, issue_y), left_issue, small_scale, ink, content_w // 3, 1, "thin")
    center_w, _ = measure_text(wrap_text(center_issue, content_w // 3, small_scale, 1), small_scale)
    draw_pixel_text(page, (content_x + (content_w - center_w) // 2, issue_y), center_issue, small_scale, ink, content_w // 3, 1, "thin")
    right_w, _ = measure_text(wrap_text(right_issue, content_w // 3, small_scale, 1), small_scale)
    draw_pixel_text(page, (content_x + content_w - right_w, issue_y), right_issue, small_scale, ink, content_w // 3, 1, "thin")

    section_label = str(manifest.get("section_label") or template.get("section_label") or locale.get("section_label") or "BREAKING NEWS")
    section_y = issue_y + text_height(1, small_scale) + round(page_height * 0.018)
    date_badge_scale = max(1, min(2, small_scale + 1))
    draw_prominent_date_badge(
        page,
        draw,
        (content_x + round(content_w * 0.56), issue_y + text_height(1, small_scale) + 14, round(content_w * 0.44), max(32, round(page_height * 0.050))),
        manifest,
        ink,
        accent,
        paper,
        date_badge_scale,
    )
    section_lines = wrap_text(section_label, content_w, section_scale, 1)
    section_w, section_h = measure_text(section_lines, section_scale)
    draw_pixel_text(page, (content_x + (content_w - section_w) // 2, section_y), section_lines, section_scale, ink, weight="regular")
    draw_rule(draw, (content_x, section_y - 12, content_x + content_w, section_y - 9), ink)
    draw_rule(draw, (content_x, section_y + section_h + 12, content_x + content_w, section_y + section_h + 14), ink)

    article_y = section_y + section_h + round(page_height * 0.032)
    article_h = round(page_height * float(template.get("society_article_ratio", 0.255)))
    story_w = round(content_w * float(template.get("society_story_ratio", 0.43)))
    gutter = max(18, round(content_w * 0.025))
    image_x = content_x + story_w + gutter
    reserve_ad_rail = bool(template.get("society_ad_rail", True))
    rail_w = round(content_w * float(template.get("society_ad_rail_ratio", 0.18))) if reserve_ad_rail else 0
    image_w = content_w - story_w - gutter - rail_w
    target_image_w = round(content_w * float(manifest.get("society_lead_width_ratio") or template.get("society_lead_width_ratio", 0)))
    if target_image_w > image_w:
        image_w = min(target_image_w, content_x + content_w - image_x - max(0, rail_w // 3))
    image_boost = float(manifest.get("lead_image_boost") or template.get("lead_image_boost", 1.0))
    image_h = min(round(article_h * 0.88 * image_boost), round(image_w * source.height / source.width))
    image_y = article_y + round(article_h * 0.04)

    draw_rule(draw, (content_x, article_y - 12, content_x + story_w, article_y - 10), accent)
    headline_lines = wrap_text(text["headline"], story_w, title_scale, 3)
    draw_pixel_text(page, (content_x, article_y), headline_lines, title_scale, ink, story_w, weight="bold")
    story_y = article_y + text_height(len(headline_lines), title_scale) + 12
    deck_lines = wrap_text(text["deck"], story_w, body_scale, 3)
    draw_pixel_text(page, (content_x, story_y), deck_lines, body_scale, accent, story_w, weight="regular")
    story_y += text_height(len(deck_lines), body_scale) + 12

    snippets = snippet_lines(manifest, locale)
    reports = report_lines(manifest, locale)
    prepared_paragraphs = newspaper_paragraphs(manifest, locale)
    paragraphs = prepared_paragraphs[:3] if prepared_paragraphs else [*reports, *snippets]
    story_end_y = draw_text_block(
        page,
        (content_x, story_y),
        paragraphs,
        body_scale,
        ink,
        story_w,
        article_y + article_h,
        5 if prepared_paragraphs else 3,
        "regular",
        8,
    )

    image_box = (image_x, image_y, image_w, image_h)
    draw.rectangle((image_x - 3, image_y - 3, image_x + image_w + 3, image_y + image_h + 3), outline=color(ink), width=2)
    placed_image = paste_contained(page, source, image_box)
    caption_y = image_y + image_h + 10
    caption_text = text["caption"]
    draw_pixel_text(page, (image_x, caption_y), caption_text, small_scale, ink, image_w, 2, "thin")
    watermark_y = max(section_y + section_h + 10, article_y - max(18, page_height // 42))
    draw_belle_epoque_watermark(
        page,
        draw,
        (image_x, watermark_y),
        max(140, image_w),
        accent,
        muted,
        ink,
        paper,
        max(1, min(2, small_scale + 1)),
    )

    lower_y = max(story_end_y + 12, caption_y + text_height(2, small_scale) + 10)
    lower_h = max(86, page_height - margin - lower_y - round(page_height * 0.018))
    lower_lines = newspaper_paragraphs(manifest, locale)
    use_prepared_paragraphs = bool(lower_lines)
    if not lower_lines:
        lower_lines = [*snippets, *reports, str(manifest.get("event") or "")]

    ad_paths = ordered_ad_values(manifest, template)
    default_ads = list(template.get("default_ad_assets") or [])
    ad_boxes: list[list[int]] = []
    remaining_ads = [(i, value, ad_aspect(base_dir, value)) for i, value in enumerate(ad_paths)]
    ad_slots = society_ad_slots(
        content_x,
        content_w,
        page_height,
        margin,
        article_y,
        article_h,
        story_w,
        gutter,
        image_x,
        image_y,
        image_w,
        image_h,
        lower_y,
        lower_h,
    )
    used_indices: set[int] = set()
    placed_ad_boxes: list[tuple[int, int, int, int]] = []
    for fallback_index, slot in enumerate(ad_slots):
        item = choose_ad_for_slot(remaining_ads, str(slot["aspect"]))
        original_index = item[0] if item else fallback_index
        ad_value = item[1] if item else None
        box = slot["box"]
        if box[1] + box[3] > page_height - margin:
            continue
        used_indices.add(original_index)
        placed_box = draw_society_ad(page, draw, base_dir, ad_value, box, original_index, manifest, ink, accent, muted)
        placed_ad_boxes.append(tuple(placed_box))
        ad_boxes.append([placed_box[0], placed_box[1], placed_box[2], placed_box[3]])

    flow_box = (
        content_x,
        max(lower_y - 6, margin),
        content_w,
        max(1, page_height - margin - max(lower_y - 6, margin) - max(24, round(page_height * 0.055))),
    )
    draw_rule(draw, (flow_box[0], flow_box[1] - 3, flow_box[0] + flow_box[2], flow_box[1] - 1), muted)
    flow_paragraphs_around_boxes(
        page,
        draw,
        flow_box,
        lower_lines,
        small_scale,
        ink,
        muted,
        placed_ad_boxes,
        columns=int(template.get("society_flow_columns") or 3),
        repeat_target=6 if use_prepared_paragraphs else 18,
        preformatted=use_prepared_paragraphs,
        drop_cap_every=int(manifest.get("drop_cap_every") or template.get("drop_cap_every") or 2),
    )

    draw_rule(draw, (content_x, page_height - margin, content_x + content_w, page_height - margin + 2), ink)
    output_scale = int(manifest.get("output_scale") or template.get("output_scale", 1))
    age_strength = float(manifest.get("age_filter_strength", template.get("age_filter_strength", 0.72)))
    save_page = apply_aged_newspaper_filter(page, seed, paper, ink, age_strength)
    retro_filter = str(manifest.get("retro_filter", template.get("retro_filter", "belle-epoque-print")))
    retro_strength = float(manifest.get("retro_filter_strength", template.get("retro_filter_strength", 0.50)))
    save_page = apply_retro_print_filter(save_page, seed, paper, ink, accent, retro_strength, retro_filter)
    save_size = [page_width, page_height]
    save_lead_box = list(placed_image)
    save_ad_boxes = ad_boxes
    if output_scale > 1:
        save_page = save_page.resize((page_width * output_scale, page_height * output_scale), Image.Resampling.NEAREST)
        save_size = [page_width * output_scale, page_height * output_scale]
        save_lead_box = scale_box(placed_image, output_scale)
        save_ad_boxes = [scale_box(box, output_scale) for box in ad_boxes]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    save_page.save(out_path)

    summary = {
        "output": str(out_path),
        "source_image": str(source_path),
        "size": save_size,
        "layout_size": [page_width, page_height],
        "output_scale": output_scale,
        "lead_image_box": save_lead_box,
        "ad_boxes": save_ad_boxes,
        "masthead": text["masthead"],
        "style_key": style_key,
        "layout_mode": "society_broadsheet",
        "filters": {
            "age_filter_strength": age_strength,
            "retro_filter": retro_filter,
            "retro_filter_strength": retro_strength,
        },
        "masthead_asset": masthead_asset,
        "static_assets": {
            "layout_template": str(TEMPLATE_PATH),
            "divider_asset": template.get("divider_asset"),
            "badge_asset": template.get("badge_asset"),
            "default_ad_assets": default_ads,
            "layout_family": template.get("layout_family"),
        },
    }
    summary_path = out_path.with_name("newspaper-render.json")
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    scale = preview_scale if preview_scale is not None else int(manifest.get("preview_scale", template.get("preview_scale", 1)))
    if scale > 1:
        preview = save_page.resize((page_width * scale, page_height * scale), Image.Resampling.NEAREST)
        preview_path = out_path.with_name("newspaper-preview.png")
        preview.save(preview_path)
        summary["preview"] = str(preview_path)
        summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    return summary


def ad_positions_from_pattern(
    ad_slot: tuple[int, int, int, int],
    pattern: list[Any],
    ad_count: int,
) -> list[tuple[int, int, int, int]]:
    x, y, w, h = ad_slot
    positions: list[tuple[int, int, int, int]] = []
    for spec in pattern[:ad_count]:
        if not isinstance(spec, dict):
            continue
        px = x + round(float(spec.get("x", 0)) * w)
        py = y + round(float(spec.get("y", 0)) * h)
        pw = round(float(spec.get("w", 1)) * w)
        ph = round(float(spec.get("h", 1)) * h)
        positions.append((px, py, max(24, pw), max(22, ph)))
    return positions


def build_ad_positions(
    ad_slot: tuple[int, int, int, int],
    ad_count: int,
    manifest: dict[str, Any],
    template: dict[str, Any],
    page_width: int,
) -> list[tuple[int, int, int, int]]:
    pattern = manifest.get("ad_box_pattern") or template.get("ad_box_pattern") or []
    if isinstance(pattern, list) and pattern:
        positions = ad_positions_from_pattern(ad_slot, pattern, ad_count)
        if len(positions) >= min(ad_count, len(pattern)):
            return positions

    x, y, w, h = ad_slot
    gap = int(manifest.get("ad_gap") or template.get("ad_gap") or max(8, page_width // 220))
    preferred_cols = int(manifest.get("ad_columns") or template.get("ad_columns", 2))
    min_w = int(template.get("ad_min_width") or max(120, page_width // 12))
    min_h = int(template.get("ad_min_height") or max(80, page_width // 18))
    cols = max(1, min(preferred_cols, ad_count))
    while cols > 1 and (w - gap * (cols - 1)) // cols < min_w:
        cols -= 1
    rows = max(1, (ad_count + cols - 1) // cols)
    while cols > 1 and (h - gap * (rows - 1)) // rows < min_h:
        cols -= 1
        rows = max(1, (ad_count + cols - 1) // cols)
    cell_w = max(24, (w - gap * max(0, cols - 1)) // cols)
    cell_h = max(22, (h - gap * max(0, rows - 1)) // rows)
    positions = []
    for i in range(ad_count):
        col = i % cols
        row = i // cols
        stagger_x = (gap // 2) if row % 2 and cols > 1 else 0
        shrink = 0 if i % 3 else max(0, gap // 2)
        px = x + col * (cell_w + gap) + min(stagger_x, max(0, w - cell_w))
        py = y + row * (cell_h + gap)
        positions.append((px, py, max(24, cell_w - shrink), cell_h))
    return positions


def draw_ad_frame(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    ink: str,
    accent: str,
    muted: str,
    index: int,
) -> None:
    x, y, w, h = box
    draw.rectangle((x, y, x + w, y + h), outline=color(ink), width=1)
    if w >= 120 and h >= 70:
        inset = 5 if index % 2 else 7
        draw.rectangle((x + inset, y + inset, x + w - inset, y + h - inset), outline=color(muted), width=1)
        if index % 3 == 0:
            draw.line((x + 8, y + 18, x + w - 8, y + 18), fill=color(accent), width=1)


def draw_scan_layout_texture(
    page: Image.Image,
    style_key: str,
    template: dict[str, Any],
    ink: str,
    accent: str,
    muted: str,
    margin: int,
    lead_box: tuple[int, int, int, int],
    text_boxes: list[tuple[int, int, int, int]],
) -> None:
    draw = ImageDraw.Draw(page)
    page_w, page_h = page.size
    content = (margin, margin, page_w - margin * 2, page_h - margin * 2)
    columns = int(template.get("columns", 5))
    gutter = int(template.get("gutter", max(8, page_w * 0.012)))
    draw_column_rules(draw, content, columns, gutter, ink, muted)

    lx, ly, lw, lh = lead_box
    draw.rectangle((lx - 4, ly - 4, lx + lw + 4, ly + lh + 4), outline=color(ink), width=2)
    draw.rectangle((lx - 1, ly - 1, lx + lw + 1, ly + lh + 1), outline=color(paper_safe(muted)), width=1)

    for x, y, w, h in text_boxes:
        for yy in range(y, y + h, max(8, h // 8 or 8)):
            draw.line((x, yy, x + w, yy), fill=color(muted), width=1)

    if style_key == "france":
        for yy in (margin + 8, ly - 16):
            draw.rectangle((margin, yy, page_w - margin, yy + 2), fill=color(ink))
            draw.rectangle((margin, yy + 6, page_w - margin, yy + 7), fill=color(accent))
    elif style_key == "united-states":
        chip_labels = ["NEWS", "MONEY", "SPORT", "LIFE"]
        chip_w = max(54, (page_w - margin * 2) // 10)
        for i, label in enumerate(chip_labels):
            cx = margin + i * (chip_w + 8)
            cy = margin + 8
            draw.rectangle((cx, cy, cx + chip_w, cy + 18), fill=color([accent, muted, "#ffd13b", "#39d3ff"][i % 4]))
            draw_pixel_text(page, (cx + 6, cy + 6), label, 1, ink, chip_w - 8, 1, "bold")
    elif style_key == "japan":
        for i in range(10):
            x = page_w - margin - 14 - i * 13
            for y in range(ly + 4, ly + lh - 8, 12):
                draw.rectangle((x, y, x + 4, y + 7), fill=color(accent if (i + y) % 4 == 0 else muted))
    elif style_key == "china":
        draw.rectangle((margin, margin + 4, page_w - margin, margin + 16), fill=color(accent))
        for i in range(5):
            y = ly + lh + 24 + i * 18
            draw.rectangle((margin, y, page_w - margin, y + 1), fill=color(muted))
    elif style_key == "hong-kong":
        draw.rectangle((margin, margin + 5, page_w - margin, margin + 20), outline=color(accent), width=2)
        for i in range(8):
            x = margin + i * 42
            draw.rectangle((x, margin + 8, x + 26, margin + 17), fill=color(accent if i % 2 else muted))
    elif style_key == "korea":
        ring_colors = [accent, "#214aa5", "#38aeea", "#15945f", muted]
        for i, ring in enumerate(ring_colors):
            x = margin + 8 + i * 18
            draw.ellipse((x, margin + 8, x + 12, margin + 20), outline=color(ring), width=2)


def paper_safe(value: str) -> str:
    return value or "#000000"


def default_manifest_text(manifest: dict[str, Any], locale: dict[str, Any] | None = None) -> dict[str, str]:
    locale = locale or {}
    place = manifest.get("place") or manifest.get("country") or "The City"
    date = manifest.get("date") or "Special Edition"
    event = manifest.get("event") or locale.get("fallback_deck") or "A Belle Epoque memory returns in pixel color"
    return {
        "masthead": manifest.get("masthead") or "THE BELLE EPOQUE GAZETTE",
        "issue_line": manifest.get("issue_line") or f"{place} - {date}",
        "headline": manifest.get("headline") or locale.get("fallback_headline") or f"{place} Marks The Moment",
        "deck": manifest.get("deck") or event,
        "caption": manifest.get("caption") or locale.get("fallback_caption") or "Lead image from the Belle Epoque archive.",
        "event": str(event),
    }


def event_fill_lines(manifest: dict[str, Any]) -> list[str]:
    values = (
        manifest.get("secondary_events")
        or manifest.get("side_events")
        or manifest.get("related_events")
        or manifest.get("other_events")
        or []
    )
    if isinstance(values, str):
        values = [values]
    lines: list[str] = []
    for item in values:
        if isinstance(item, dict):
            date = str(item.get("date") or item.get("year") or "").strip()
            title = str(
                item.get("headline")
                or item.get("local_headline")
                or item.get("headline_local")
                or item.get("title")
                or item.get("event")
                or item.get("summary")
                or ""
            ).strip()
            note = str(item.get("note") or item.get("local_note") or item.get("note_local") or item.get("detail") or "").strip()
            text = " - ".join(part for part in (date, title or note) if part)
            if text:
                lines.append(text)
        elif item:
            lines.append(str(item))
    return lines


def report_lines(manifest: dict[str, Any], locale: dict[str, Any] | None = None) -> list[str]:
    reports = manifest.get("reports") or manifest.get("report_fill") or manifest.get("story_fill") or []
    if isinstance(reports, str):
        reports = [reports]
    if not reports:
        reports = (locale or {}).get("fallback_reports") or [
            "THE FRONT PAGE RECORDS THE DAY IN SHORT COLUMNS.",
            "STREETS AND WINDOWS CARRY THE NEWS.",
            "SMALL NOTICES TRACE THE CITY RHYTHM.",
            "THE LEAD IMAGE HOLDS THE MEMORY.",
            "PRINT SHOPS HUM BEFORE THE MORNING.",
        ]
    lines: list[str] = []
    for report in reports:
        if isinstance(report, dict):
            for key in ("headline", "body", "text", "note"):
                value = report.get(key)
                if value:
                    lines.append(str(value))
        else:
            lines.append(str(report))
    return [*lines, *event_fill_lines(manifest)]


def snippet_lines(manifest: dict[str, Any], locale: dict[str, Any] | None = None) -> list[str]:
    snippets = manifest.get("snippets") or manifest.get("briefs") or manifest.get("side_notes") or []
    if isinstance(snippets, str):
        snippets = [snippets]
    lines: list[str] = []
    for item in snippets:
        if isinstance(item, dict):
            value = item.get("headline") or item.get("title") or item.get("text") or item.get("note")
            if value:
                lines.append(str(value))
        elif item:
            lines.append(str(item))
    if not lines:
        lines = [str(line) for line in ((locale or {}).get("fallback_snippets") or [])]
    return lines


def ad_text_for(index: int, ad_value: Any, manifest: dict[str, Any]) -> dict[str, str]:
    style_key = style_key_from_manifest(manifest)
    labels = list(LOCALE_TEXT.get(style_key, LOCALE_TEXT["united-states"]).get("ad_labels", [])) or [
        "LIVE AD",
        "SPECIAL",
        "MARKET",
        "NOTICE",
        "TICKETS",
        "OPEN",
    ]
    copy = manifest.get("ad_copy") or manifest.get("ad_text") or []
    if isinstance(ad_value, dict):
        label = str(ad_value.get("label") or ad_value.get("headline") or labels[index % len(labels)])
        body = str(ad_value.get("copy") or ad_value.get("body") or ad_value.get("tagline") or "")
        return {"label": label, "body": body}
    if isinstance(copy, list) and index < len(copy):
        item = copy[index]
        if isinstance(item, dict):
            return {
                "label": str(item.get("label") or item.get("headline") or labels[index % len(labels)]),
                "body": str(item.get("copy") or item.get("body") or item.get("tagline") or ""),
            }
        return {"label": str(item), "body": ""}
    return {"label": labels[index % len(labels)], "body": ""}


def render(manifest_path: Path, out_path: Path, preview_scale: int | None) -> dict[str, Any]:
    base_dir = manifest_path.parent
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    seed = int(manifest.get("seed", 1900))
    style_key, template = select_template(manifest)
    locale = locale_for(style_key, manifest, template)
    set_active_font(str(locale.get("font_key") or "ascii-pixel"))
    text = default_manifest_text(manifest, locale)
    template_palette = template.get("palette") or DEFAULT_PALETTE
    manifest_palette = manifest.get("palette") or template_palette
    use_manifest_newspaper_palette = bool(
        manifest.get("newspaper_palette_override") or manifest.get("use_manifest_newspaper_palette")
    )
    palette = manifest_palette if use_manifest_newspaper_palette else template_palette
    paper = (
        manifest.get("paper_color")
        if use_manifest_newspaper_palette and manifest.get("paper_color")
        else template.get("paper_color") or palette[9 if len(palette) > 9 else -1]
    )
    ink = (
        manifest.get("ink_color")
        if use_manifest_newspaper_palette and manifest.get("ink_color")
        else template.get("ink_color") or palette[0]
    )
    accent = (
        manifest.get("accent_color")
        if use_manifest_newspaper_palette and manifest.get("accent_color")
        else template.get("accent_color") or palette[4 if len(palette) > 4 else 0]
    )
    muted = (
        manifest.get("muted_color")
        if use_manifest_newspaper_palette and manifest.get("muted_color")
        else template.get("muted_color") or palette[10 if len(palette) > 10 else -1]
    )

    source_path = resolve(base_dir, manifest["source_image"])
    source = load_rgba(source_path)
    if str(manifest.get("layout_mode") or template.get("layout_mode") or "").lower() == "society_broadsheet":
        return render_society_broadsheet(
            base_dir,
            manifest,
            text,
            style_key,
            template,
            source_path,
            source,
            seed,
            paper,
            ink,
            accent,
            muted,
            out_path,
            preview_scale,
        )
    page_width = int(manifest.get("page_width") or round(source.width * float(template.get("page_width_ratio", 1.08))))
    margin = page_margin(page_width, manifest, template, 0.030, 16, 0.035)
    header_ratio = float(template.get("header_ratio", 0.20))
    lower_ratio = float(template.get("lower_ratio", 0.22))
    lead_scale = float(manifest.get("lead_image_scale") or template.get("lead_image_scale", 1.0))
    if manifest.get("page_height"):
        page_height = int(manifest["page_height"])
    else:
        ratio_height = round(source.height * float(template.get("page_height_ratio", 1.38)))
        fit_height = round((source.height * lead_scale + margin * 1.5) / max(0.45, 1 - header_ratio - lower_ratio))
        page_height = max(ratio_height, fit_height)
    page = Image.new("RGBA", (page_width, page_height), color(paper))
    draw = ImageDraw.Draw(page)
    add_paper_texture(page, ink, seed, max(200, page_width * page_height // 900))

    content_x = margin
    content_w = page_width - margin * 2
    slots = template.get("layout_slots") or {}
    if slots.get("lead"):
        lead_slot = rect_from_layout(slots["lead"], page_width, page_height, margin)
        image_w, image_h = fit_source_box(source, (lead_slot[2], lead_slot[3]), lead_scale)
        image_x = lead_slot[0] + (lead_slot[2] - image_w) // 2
        image_y = lead_slot[1] + (lead_slot[3] - image_h) // 2
    else:
        header_h = int(manifest.get("header_height") or round(page_height * header_ratio))
        lower_h = int(manifest.get("lower_height") or round(page_height * lower_ratio))
        image_y = header_h + margin // 2
        max_image_h = min(
            page_height - image_y - lower_h - margin,
            round(page_height * float(template.get("lead_ratio", 0.58))),
        )
        max_image_w = page_width - margin * 2
        image_w, image_h = fit_source_box(source, (max_image_w, max_image_h), lead_scale)
        image_x = (page_width - image_w) // 2

    draw_rule(draw, (margin, margin, page_width - margin, margin + 2), ink)
    mast_scale = max(2, min(5, page_width // 360))
    masthead_asset, masthead_name = pick_masthead(manifest, template)
    if masthead_name:
        text["masthead"] = masthead_name
    if slots.get("masthead"):
        masthead_box = rect_from_layout(slots["masthead"], page_width, page_height, margin)
    else:
        header_h = int(round(page_height * header_ratio))
        masthead_box_h = max(54, min(round(header_h * float(template.get("masthead_box_ratio", 0.42))), 132))
        masthead_box = (content_x, margin + 6, content_w, masthead_box_h)
    masthead_placed = None
    mast_bottom = masthead_box[1] + masthead_box[3]

    snippet_box = rect_from_layout(slots["snippets"], page_width, page_height, margin) if slots.get("snippets") else None
    ad_slot = rect_from_layout(slots["ads"], page_width, page_height, margin) if slots.get("ads") else None
    text_placeholder_boxes = []
    if snippet_box:
        text_placeholder_boxes.append(snippet_box)
    if ad_slot:
        text_placeholder_boxes.append(ad_slot)
    draw_scan_layout_texture(
        page,
        style_key,
        template,
        ink,
        accent,
        muted,
        margin,
        (image_x, image_y, image_w, image_h),
        text_placeholder_boxes,
    )

    mx, my, mw, mh = masthead_box
    masthead_paper = sample_box_color(page, masthead_box, paper)
    draw.rectangle((mx - 3, my - 3, mx + mw + 3, my + mh + 3), fill=color(masthead_paper))
    masthead_placed = paste_asset(page, base_dir, masthead_asset, masthead_box, True, ink, masthead_paper)
    if masthead_placed:
        mast_bottom = masthead_placed[1] + masthead_placed[3]
    else:
        mast_lines = wrap_text(text["masthead"], content_w, mast_scale, 2)
        mast_w, mast_h = measure_text(mast_lines, mast_scale)
        draw_pixel_text(page, ((page_width - mast_w) // 2, masthead_box[1]), mast_lines, mast_scale, ink)
        mast_bottom = masthead_box[1] + mast_h

    divider_y = mast_bottom + 8
    divider_placed = paste_asset(page, base_dir, template.get("divider_asset"), (content_x, divider_y, content_w, 24), True, ink, paper)
    if not divider_placed:
        draw_rule(draw, (margin, divider_y + 6, page_width - margin, divider_y + 8), accent)

    small_scale = max(1, min(2, page_width // 720))
    issue_box = rect_from_layout(slots["issue"], page_width, page_height, margin) if slots.get("issue") else (margin, divider_y + 28, content_w, 24)
    draw_pixel_text(page, (issue_box[0], issue_box[1]), text["issue_line"], small_scale, ink, issue_box[2], 1, "thin")
    badge_w = min(240, content_w // 4)
    badge_box = rect_from_layout(slots["badge"], page_width, page_height, margin) if slots.get("badge") else (page_width - margin - badge_w, issue_box[1] - 6, badge_w, 48)
    badge_placed = paste_asset(page, base_dir, template.get("badge_asset"), badge_box)
    if not badge_placed:
        draw_pixel_text(
            page,
            (badge_box[0], badge_box[1]),
            "SPECIAL EDITION",
            small_scale,
            accent,
            badge_box[2],
            1,
            "bold",
        )

    headline_scale = int(manifest.get("headline_scale") or max(1, min(4, page_width // 420)))
    headline_box = rect_from_layout(slots["headline"], page_width, page_height, margin) if slots.get("headline") else (margin, issue_box[1] + text_height(1, small_scale) + 16, content_w, 70)
    headline_lines = wrap_text(text["headline"], headline_box[2], headline_scale, int(template.get("headline_lines", 2)))
    draw_pixel_text(page, (headline_box[0], headline_box[1]), headline_lines, headline_scale, ink, weight="bold")
    deck_box = rect_from_layout(slots["deck"], page_width, page_height, margin) if slots.get("deck") else (headline_box[0], headline_box[1] + text_height(len(headline_lines), headline_scale) + 10, headline_box[2], 24)
    draw_pixel_text(page, (deck_box[0], deck_box[1]), text["deck"], small_scale, accent, deck_box[2], int(template.get("deck_lines", 1)), "regular")

    image_box = (image_x, image_y, image_w, image_h)
    draw.rectangle((image_x - 3, image_y - 3, image_x + image_w + 3, image_y + image_h + 3), outline=color(ink), width=2)
    placed_image = paste_contained(page, source, image_box)
    caption_box = rect_from_layout(slots["caption"], page_width, page_height, margin) if slots.get("caption") else (margin, image_y + image_h + 8, content_w, 24)
    draw_pixel_text(page, (caption_box[0], caption_box[1]), text["caption"], small_scale, ink, caption_box[2], 1, "thin")

    snippets = snippet_lines(manifest, locale)
    reports = report_lines(manifest, locale)
    if template.get("side_note_style") and image_x + image_w + 28 < page_width - margin:
        side_x = image_x + image_w + 18
        side_y = image_y + 10
        side_w = page_width - margin - side_x
        side_h = max(90, min(image_h - 24, round(page_height * float(template.get("side_note_height_ratio", 0.30)))))
        side_lines = [text["event"] if "event" in text else manifest.get("event", ""), *snippets, *reports]
        draw_side_note_area(
            page,
            draw,
            (side_x, side_y, side_w, side_h),
            [str(line) for line in side_lines if line],
            small_scale,
            ink,
            accent,
            muted,
        )
    ad_boxes = []
    ad_paths = ordered_ad_values(manifest, template)
    default_ads = list(template.get("default_ad_assets") or [])
    target_ad_count = max(
        len(ad_paths),
        int(manifest.get("ad_count") or manifest.get("ad_placeholders") or template.get("ad_default", 4)),
        4,
    )
    ad_count = max(len(ad_paths), target_ad_count)

    if snippet_box:
        draw_snippet_area(page, draw, snippet_box, snippets, reports, template, small_scale, ink, accent, muted)

    compact_ads = page_width < 640 or bool(ad_slot and ad_slot[3] < 100)
    if ad_slot:
        positions = build_ad_positions(ad_slot, ad_count, manifest, template, page_width)
    elif compact_ads:
        lower_y = image_y + image_h + margin + 12
        cols = min(4, ad_count)
        ad_area_x = margin
        ad_area_w = content_w
        ad_h = max(18, page_height - lower_y - margin)
        ad_w = max(24, (ad_area_w - 8 * (cols - 1)) // cols)
        positions = [(ad_area_x + i * (ad_w + 8), lower_y, ad_w, ad_h) for i in range(cols)]
    else:
        lower_y = image_y + image_h + margin + 12
        ad_area_x = page_width - margin - max(160, content_w // 4)
        snippet_w = ad_area_x - margin - 12
        if not snippet_box:
            y = lower_y
            for index, snippet in enumerate([*snippets, *reports][:6]):
                if y > page_height - margin - 18:
                    break
                weight = "regular" if index < len(snippets) else "thin"
                draw_pixel_text(page, (margin, y), snippet, small_scale, ink, snippet_w, 1, weight)
                y += 11 * small_scale
                draw_rule(draw, (margin, y, margin + snippet_w, y + 1), muted)
                y += 5

        preferred_cols = int(manifest.get("ad_columns") or template.get("ad_columns", 2))
        cols = min(preferred_cols, 3) if ad_count >= 5 and (page_width - ad_area_x - margin) >= 420 else 2
        ad_w = max(58, (page_width - ad_area_x - margin - 8) // cols)
        rows = max(1, (ad_count + cols - 1) // cols)
        ad_h = max(24, (page_height - lower_y - margin - 8 * max(0, rows - 1)) // rows)
        positions = []
        for i in range(ad_count):
            col = i % cols
            row = i // cols
            positions.append((ad_area_x + col * (ad_w + 8), lower_y + row * (ad_h + 8), ad_w, ad_h))

    remaining_ads = [(i, value, ad_aspect(base_dir, value)) for i, value in enumerate(ad_paths)]
    ad_slots = distributed_ad_slots(ad_slot, positions, manifest, template, page_width, page_height, margin)
    for fallback_index, slot in enumerate(ad_slots):
        if fallback_index >= ad_count:
            break
        item = choose_ad_for_slot(remaining_ads, str(slot.get("aspect") or "square"))
        original_index = item[0] if item else fallback_index
        ad_value = item[1] if item else None
        x, yy, ad_w, ad_h = slot["box"]
        if yy + ad_h > page_height - margin:
            continue
        draw_society_ad(page, draw, base_dir, ad_value, (x, yy, ad_w, ad_h), original_index, manifest, ink, accent, muted)
        if not ad_value:
            draw_rule(draw, (x + 6, yy + ad_h - 9, x + ad_w - 6, yy + ad_h - 8), muted)
        ad_boxes.append([x, yy, ad_w, ad_h])

    if not snippet_box:
        filler_top = image_y + image_h + max(12, margin // 2)
        filler_bottom = min(page_height - margin, min((box[1] for box in [tuple(slot["box"]) for slot in ad_slots] if box[1] > filler_top), default=page_height - margin) - 10)
        if filler_bottom - filler_top >= 50:
            draw_micro_columns(
                page,
                draw,
                (margin, filler_top, max(80, content_w // 2), filler_bottom - filler_top),
                [*snippets, *reports],
                small_scale,
                ink,
                accent,
                muted,
                2,
                2,
            )

    age_strength = float(manifest.get("age_filter_strength", template.get("age_filter_strength", 0.62)))
    save_page = apply_aged_newspaper_filter(page, seed, paper, ink, age_strength)
    retro_filter = str(manifest.get("retro_filter", template.get("retro_filter", "belle-epoque-print")))
    retro_strength = float(manifest.get("retro_filter_strength", template.get("retro_filter_strength", 0.50)))
    save_page = apply_retro_print_filter(save_page, seed, paper, ink, accent, retro_strength, retro_filter)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    save_page.save(out_path)

    summary = {
        "output": str(out_path),
        "source_image": str(source_path),
        "size": [page_width, page_height],
        "lead_image_box": list(placed_image),
        "ad_boxes": ad_boxes,
        "masthead": text["masthead"],
        "style_key": style_key,
        "filters": {
            "age_filter_strength": age_strength,
            "retro_filter": retro_filter,
            "retro_filter_strength": retro_strength,
        },
        "masthead_asset": masthead_asset,
        "static_assets": {
            "layout_template": str(TEMPLATE_PATH),
            "divider_asset": template.get("divider_asset"),
            "badge_asset": template.get("badge_asset"),
            "default_ad_assets": default_ads,
            "layout_family": template.get("layout_family"),
        },
    }
    summary_path = out_path.with_name("newspaper-render.json")
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    scale = preview_scale if preview_scale is not None else int(manifest.get("preview_scale", 1))
    if scale > 1:
        preview = save_page.resize((page_width * scale, page_height * scale), Image.Resampling.NEAREST)
        preview_path = out_path.with_name("newspaper-preview.png")
        preview.save(preview_path)
        summary["preview"] = str(preview_path)
        summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--preview-scale", type=int, default=None)
    args = parser.parse_args()

    summary = render(args.manifest.resolve(), args.out.resolve(), args.preview_scale)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
