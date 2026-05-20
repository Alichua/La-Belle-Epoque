#!/usr/bin/env python3
"""Generate static pixel newspaper assets for Pixel Belle Epoque."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageColor, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
FONT = json.loads((ROOT / "assets" / "pixel-font-5x7.json").read_text(encoding="utf-8"))
OUT = ROOT / "assets" / "newspaper"


STYLES: dict[str, dict[str, Any]] = {
    "france": {
        "real_masthead_name": "Le Petit Journal",
        "mastheads": ["LE BOULEVARD MODERNE", "LA GAZETTE ELECTRIQUE", "LE PETIT BELLE EPOQUE"],
        "ads": ["PERFUME", "BICYCLE", "CABARET", "METRO", "CHOCOLAT", "THEATRE"],
        "palette": ["#2a1d1b", "#4f3828", "#8f642f", "#c79a3c", "#d94d3f", "#1f4b4a", "#2f766f", "#f1d27a", "#fff0d0", "#f8f4e8", "#e7e0d2"],
        "paper_color": "#f8f0dc",
        "ink_color": "#2a1d1b",
        "accent_color": "#d94d3f",
        "muted_color": "#d8cdb8",
        "layout": {"layout_mode": "society_broadsheet", "font_key": "latin-serif", "page_width_ratio": 0.46, "page_aspect_ratio": 1.00, "output_scale": 2, "margin_ratio": 0.036, "max_margin_ratio": 0.040, "age_filter_strength": 0.72, "society_masthead_ratio": 0.155, "society_article_ratio": 0.38, "society_story_ratio": 0.33, "society_lead_width_ratio": 0.54, "lead_image_boost": 1.35, "society_ad_rail": True, "society_ad_rail_ratio": 0.08, "society_flow_columns": 3, "drop_cap_every": 2, "ad_treatment": "direct-float-wrap", "ad_align": "left", "ad_wrap_padding": 8, "small_scale": 1, "body_scale": 1, "section_label": "DERNIÈRE HEURE", "header_ratio": 0.20, "lower_ratio": 0.28, "lead_ratio": 0.42, "lead_image_scale": 1.0, "masthead_box_ratio": 0.16, "headline_lines": 3, "deck_lines": 2, "ad_default": 6, "ad_columns": 2, "ad_gap": 10, "ad_min_width": 150, "ad_min_height": 80, "snippet_style": "staggered-columns", "snippet_columns": 2, "side_note_style": "boxed-column", "side_note_height_ratio": 0.34, "columns": 4, "gutter": 10, "ad_box_pattern": [{"x": 0.00, "y": 0.02, "w": 0.39, "h": 0.45}, {"x": 0.43, "y": 0.00, "w": 0.26, "h": 0.38}, {"x": 0.72, "y": 0.07, "w": 0.28, "h": 0.42}, {"x": 0.08, "y": 0.54, "w": 0.29, "h": 0.41}, {"x": 0.41, "y": 0.48, "w": 0.38, "h": 0.48}, {"x": 0.82, "y": 0.56, "w": 0.18, "h": 0.36}], "floating_ad_slots": [{"x": 0.67, "y": 0.325, "w": 0.15, "h": 0.245, "aspect": "tall", "priority": 0}, {"x": 0.00, "y": 0.665, "w": 0.27, "h": 0.120, "aspect": "square", "priority": 1}, {"x": 0.31, "y": 0.825, "w": 0.33, "h": 0.105, "aspect": "wide", "priority": 2}, {"x": 0.67, "y": 0.815, "w": 0.33, "h": 0.115, "aspect": "wide", "priority": 3}, {"x": 0.00, "y": 0.830, "w": 0.26, "h": 0.115, "aspect": "square", "priority": 4}], "layout_slots": {"masthead": {"x": 0.08, "y": 0.003, "w": 0.84, "h": 0.118}, "issue": {"x": 0.00, "y": 0.135, "w": 1.00, "h": 0.028}, "headline": {"x": 0.00, "y": 0.180, "w": 1.00, "h": 0.080}, "deck": {"x": 0.48, "y": 0.245, "w": 0.52, "h": 0.050}, "lead": {"x": 0.42, "y": 0.300, "w": 0.58, "h": 0.330}, "caption": {"x": 0.42, "y": 0.640, "w": 0.58, "h": 0.040}, "snippets": {"x": 0.00, "y": 0.650, "w": 1.00, "h": 0.160}, "ads": {"x": 0.00, "y": 0.835, "w": 1.00, "h": 0.115}}},
        "layout_family": "illustrated-popular-half-format",
        "decor": "nouveau",
    },
    "united-states": {
        "real_masthead_name": "USA Today",
        "mastheads": ["THE AMERICAN SIGNAL", "MARKET STREET DAILY", "THE NEON CHRONICLE"],
        "ads": ["PC SALE", "MALL", "VHS", "SNEAKER", "DINER", "MARKET"],
        "palette": ["#050712", "#111a33", "#1f3b73", "#2952a3", "#39d3ff", "#ff2f92", "#ffd13b", "#f28b30", "#c8d0da", "#f6f7fb", "#222222"],
        "paper_color": "#f7f8f5",
        "ink_color": "#07111f",
        "accent_color": "#22aee6",
        "muted_color": "#c6ccd4",
        "layout": {"page_width_ratio": 1.10, "page_height_ratio": 1.44, "header_ratio": 0.18, "lower_ratio": 0.24, "lead_ratio": 0.43, "lead_image_scale": 1.0, "masthead_box_ratio": 0.14, "headline_lines": 2, "deck_lines": 1, "ad_default": 6, "ad_columns": 2, "ad_gap": 12, "ad_min_width": 190, "ad_min_height": 115, "snippet_style": "staggered-columns", "snippet_columns": 1, "columns": 6, "gutter": 12, "ad_box_pattern": [{"x": 0.00, "y": 0.00, "w": 1.00, "h": 0.20}, {"x": 0.04, "y": 0.24, "w": 0.45, "h": 0.22}, {"x": 0.53, "y": 0.22, "w": 0.43, "h": 0.26}, {"x": 0.00, "y": 0.53, "w": 0.48, "h": 0.20}, {"x": 0.53, "y": 0.56, "w": 0.47, "h": 0.20}, {"x": 0.08, "y": 0.80, "w": 0.84, "h": 0.18}], "layout_slots": {"masthead": {"x": 0.04, "y": 0.005, "w": 0.36, "h": 0.085}, "issue": {"x": 0.43, "y": 0.020, "w": 0.24, "h": 0.026}, "badge": {"x": 0.74, "y": 0.012, "w": 0.24, "h": 0.055}, "headline": {"x": 0.00, "y": 0.165, "w": 0.68, "h": 0.085}, "deck": {"x": 0.00, "y": 0.248, "w": 0.68, "h": 0.030}, "lead": {"x": 0.00, "y": 0.300, "w": 0.68, "h": 0.420}, "caption": {"x": 0.00, "y": 0.735, "w": 0.68, "h": 0.030}, "snippets": {"x": 0.72, "y": 0.150, "w": 0.28, "h": 0.250}, "ads": {"x": 0.72, "y": 0.435, "w": 0.28, "h": 0.485}}},
        "layout_family": "modular-color-section-front",
        "decor": "section",
    },
    "japan": {
        "real_masthead_name": "The Asahi Shimbun",
        "mastheads": ["TOKYO EVENING PRESS", "GINZA CITY TIMES", "SHOWA SIGNAL"],
        "ads": ["CASSETTE", "RECORDS", "TAXI", "VENDOR", "CAMERA", "TRAIN"],
        "palette": ["#060817", "#101d3a", "#245f8f", "#2aa7c8", "#74e3d8", "#f4f2d6", "#ffd49a", "#ff5f6d", "#d92f8a", "#7e3fb3", "#2c2c35"],
        "paper_color": "#f4f0df",
        "ink_color": "#17141f",
        "accent_color": "#d92f8a",
        "muted_color": "#c8baa1",
        "layout": {"page_width_ratio": 1.08, "page_height_ratio": 1.50, "header_ratio": 0.17, "lower_ratio": 0.23, "lead_ratio": 0.47, "lead_image_scale": 1.0, "masthead_box_ratio": 0.13, "headline_lines": 2, "deck_lines": 1, "ad_default": 6, "ad_columns": 3, "ad_gap": 12, "ad_min_width": 190, "ad_min_height": 110, "snippet_style": "staggered-columns", "snippet_columns": 1, "columns": 9, "gutter": 9, "ad_box_pattern": [{"x": 0.00, "y": 0.02, "w": 0.23, "h": 0.82}, {"x": 0.26, "y": 0.00, "w": 0.22, "h": 0.70}, {"x": 0.51, "y": 0.08, "w": 0.22, "h": 0.78}, {"x": 0.76, "y": 0.03, "w": 0.24, "h": 0.68}, {"x": 0.27, "y": 0.76, "w": 0.31, "h": 0.22}, {"x": 0.62, "y": 0.76, "w": 0.36, "h": 0.22}], "layout_slots": {"masthead": {"x": 0.00, "y": 0.005, "w": 0.48, "h": 0.085}, "issue": {"x": 0.52, "y": 0.018, "w": 0.25, "h": 0.026}, "badge": {"x": 0.82, "y": 0.012, "w": 0.18, "h": 0.050}, "headline": {"x": 0.00, "y": 0.125, "w": 0.76, "h": 0.075}, "deck": {"x": 0.00, "y": 0.200, "w": 0.76, "h": 0.030}, "lead": {"x": 0.00, "y": 0.255, "w": 0.76, "h": 0.465}, "caption": {"x": 0.00, "y": 0.730, "w": 0.76, "h": 0.030}, "snippets": {"x": 0.80, "y": 0.125, "w": 0.20, "h": 0.595}, "ads": {"x": 0.00, "y": 0.805, "w": 1.00, "h": 0.160}}},
        "layout_family": "compact-evening-grid",
        "decor": "tabs",
    },
    "china": {
        "real_masthead_name": "People's Daily",
        "mastheads": ["OPEN CITY DAILY", "REFORM MORNING NEWS", "THE RIVERFRONT BUILDER"],
        "ads": ["APPLIANCE", "BICYCLE", "CRANE", "HOUSING", "PAGER", "BUS"],
        "palette": ["#071b24", "#123746", "#1d6070", "#2e9aa0", "#77d1c8", "#f2e3bf", "#f1c232", "#f08b32", "#d9482e", "#a42020", "#5b6970"],
        "paper_color": "#f5ead0",
        "ink_color": "#171411",
        "accent_color": "#b71e22",
        "muted_color": "#d2bd98",
        "layout": {"page_width_ratio": 1.08, "page_height_ratio": 1.52, "header_ratio": 0.19, "lower_ratio": 0.23, "lead_ratio": 0.42, "lead_image_scale": 1.0, "masthead_box_ratio": 0.13, "headline_lines": 2, "deck_lines": 1, "ad_default": 6, "ad_columns": 3, "columns": 6, "gutter": 12, "layout_slots": {"masthead": {"x": 0.08, "y": 0.005, "w": 0.44, "h": 0.105}, "issue": {"x": 0.58, "y": 0.020, "w": 0.22, "h": 0.026}, "badge": {"x": 0.82, "y": 0.012, "w": 0.18, "h": 0.050}, "headline": {"x": 0.00, "y": 0.150, "w": 1.00, "h": 0.075}, "deck": {"x": 0.00, "y": 0.225, "w": 1.00, "h": 0.030}, "lead": {"x": 0.00, "y": 0.285, "w": 0.65, "h": 0.405}, "caption": {"x": 0.00, "y": 0.700, "w": 0.65, "h": 0.030}, "snippets": {"x": 0.68, "y": 0.285, "w": 0.32, "h": 0.405}, "ads": {"x": 0.00, "y": 0.785, "w": 1.00, "h": 0.175}}},
        "layout_family": "civic-grid-announcement",
        "decor": "civic",
    },
    "hong-kong": {
        "real_masthead_name": "Apple Daily",
        "mastheads": ["HARBOUR EVENING", "NEON HARBOUR DAILY", "THE COUNTDOWN POST"],
        "ads": ["TAXI", "WATCH", "TEA", "FERRY", "CINEMA", "JEWEL"],
        "palette": ["#030914", "#071b33", "#0b3f5f", "#0c7f96", "#20d2d6", "#ffd33d", "#f39a24", "#ff4b38", "#ff2aa3", "#8526b8", "#1c1c22"],
        "paper_color": "#f6efe2",
        "ink_color": "#101018",
        "accent_color": "#d72843",
        "muted_color": "#c9bca9",
        "layout": {"page_width_ratio": 1.08, "page_height_ratio": 1.42, "header_ratio": 0.17, "lower_ratio": 0.24, "lead_ratio": 0.49, "lead_image_scale": 1.0, "masthead_box_ratio": 0.12, "headline_lines": 2, "deck_lines": 1, "ad_default": 6, "ad_columns": 3, "columns": 5, "gutter": 10, "layout_slots": {"masthead": {"x": 0.02, "y": 0.005, "w": 0.42, "h": 0.080}, "issue": {"x": 0.46, "y": 0.018, "w": 0.24, "h": 0.026}, "badge": {"x": 0.75, "y": 0.010, "w": 0.25, "h": 0.055}, "headline": {"x": 0.00, "y": 0.120, "w": 1.00, "h": 0.090}, "deck": {"x": 0.00, "y": 0.210, "w": 1.00, "h": 0.030}, "lead": {"x": 0.00, "y": 0.265, "w": 0.72, "h": 0.485}, "caption": {"x": 0.00, "y": 0.760, "w": 0.72, "h": 0.030}, "snippets": {"x": 0.75, "y": 0.265, "w": 0.25, "h": 0.190}, "ads": {"x": 0.75, "y": 0.495, "w": 0.25, "h": 0.410}}},
        "layout_family": "dense-commercial-color-tabloid",
        "decor": "neon",
    },
    "korea": {
        "real_masthead_name": "Chosun Ilbo",
        "mastheads": ["SEOUL OLYMPIC DAILY", "GANGNAM MORNING", "THE HAN RIVER STANDARD"],
        "ads": ["SEDAN", "OLYMPIC", "TV SET", "BANK", "STORE", "COFFEE"],
        "palette": ["#070912", "#11192b", "#273550", "#46546a", "#c6ccd0", "#ffffff", "#f3e4bd", "#f5c057", "#d7472f", "#214aa5", "#38aeea", "#15945f"],
        "paper_color": "#f7f4ea",
        "ink_color": "#0d1728",
        "accent_color": "#214aa5",
        "muted_color": "#c5ccd4",
        "layout": {"page_width_ratio": 1.08, "page_height_ratio": 1.48, "header_ratio": 0.18, "lower_ratio": 0.23, "lead_ratio": 0.46, "lead_image_scale": 1.0, "masthead_box_ratio": 0.13, "headline_lines": 2, "deck_lines": 1, "ad_default": 6, "ad_columns": 3, "columns": 6, "gutter": 12, "layout_slots": {"masthead": {"x": 0.00, "y": 0.005, "w": 0.52, "h": 0.090}, "issue": {"x": 0.54, "y": 0.018, "w": 0.24, "h": 0.026}, "badge": {"x": 0.80, "y": 0.012, "w": 0.20, "h": 0.052}, "headline": {"x": 0.00, "y": 0.135, "w": 0.70, "h": 0.080}, "deck": {"x": 0.00, "y": 0.215, "w": 0.70, "h": 0.030}, "lead": {"x": 0.00, "y": 0.270, "w": 0.72, "h": 0.455}, "caption": {"x": 0.00, "y": 0.735, "w": 0.72, "h": 0.030}, "snippets": {"x": 0.75, "y": 0.135, "w": 0.25, "h": 0.590}, "ads": {"x": 0.00, "y": 0.805, "w": 1.00, "h": 0.155}}},
        "layout_family": "clean-developmental-daily",
        "decor": "olympic",
    },
}


STYLE_LAYOUT_UPDATES: dict[str, dict[str, Any]] = {
    "france": {
        "retro_filter": "belle-epoque-print",
        "retro_filter_strength": 0.42,
    },
    "united-states": {
        "font_key": "ascii-pixel",
        "retro_filter": "belle-epoque-print",
        "retro_filter_strength": 0.40,
        "floating_ad_slots": [
            {"x": 0.72, "y": 0.415, "w": 0.28, "h": 0.155, "aspect": "square", "priority": 0},
            {"x": 0.72, "y": 0.595, "w": 0.28, "h": 0.145, "aspect": "square", "priority": 1},
            {"x": 0.00, "y": 0.800, "w": 0.44, "h": 0.120, "aspect": "wide", "priority": 2},
            {"x": 0.48, "y": 0.792, "w": 0.30, "h": 0.155, "aspect": "square", "priority": 3},
            {"x": 0.82, "y": 0.770, "w": 0.18, "h": 0.185, "aspect": "tall", "priority": 4},
            {"x": 0.00, "y": 0.930, "w": 0.70, "h": 0.055, "aspect": "wide", "priority": 5},
        ],
    },
    "japan": {
        "font_key": "japanese-gothic",
        "retro_filter": "belle-epoque-print",
        "retro_filter_strength": 0.40,
        "floating_ad_slots": [
            {"x": 0.80, "y": 0.390, "w": 0.20, "h": 0.165, "aspect": "tall", "priority": 0},
            {"x": 0.80, "y": 0.585, "w": 0.20, "h": 0.135, "aspect": "square", "priority": 1},
            {"x": 0.00, "y": 0.790, "w": 0.32, "h": 0.160, "aspect": "wide", "priority": 2},
            {"x": 0.36, "y": 0.770, "w": 0.26, "h": 0.185, "aspect": "square", "priority": 3},
            {"x": 0.66, "y": 0.785, "w": 0.34, "h": 0.135, "aspect": "wide", "priority": 4},
            {"x": 0.68, "y": 0.930, "w": 0.32, "h": 0.055, "aspect": "wide", "priority": 5},
        ],
    },
    "china": {
        "font_key": "chinese-heiti",
        "retro_filter": "belle-epoque-print",
        "retro_filter_strength": 0.42,
        "ad_columns": 3,
        "ad_gap": 12,
        "ad_min_width": 190,
        "ad_min_height": 110,
        "snippet_style": "staggered-columns",
        "snippet_columns": 2,
        "floating_ad_slots": [
            {"x": 0.69, "y": 0.305, "w": 0.31, "h": 0.150, "aspect": "wide", "priority": 0},
            {"x": 0.72, "y": 0.485, "w": 0.28, "h": 0.175, "aspect": "square", "priority": 1},
            {"x": 0.00, "y": 0.765, "w": 0.30, "h": 0.165, "aspect": "square", "priority": 2},
            {"x": 0.34, "y": 0.790, "w": 0.38, "h": 0.115, "aspect": "wide", "priority": 3},
            {"x": 0.76, "y": 0.745, "w": 0.24, "h": 0.220, "aspect": "tall", "priority": 4},
            {"x": 0.02, "y": 0.940, "w": 0.62, "h": 0.050, "aspect": "wide", "priority": 5},
        ],
        "ad_box_pattern": [
            {"x": 0.00, "y": 0.03, "w": 0.25, "h": 0.76},
            {"x": 0.28, "y": 0.00, "w": 0.20, "h": 0.66},
            {"x": 0.51, "y": 0.07, "w": 0.22, "h": 0.72},
            {"x": 0.76, "y": 0.02, "w": 0.24, "h": 0.66},
            {"x": 0.30, "y": 0.72, "w": 0.32, "h": 0.24},
            {"x": 0.66, "y": 0.75, "w": 0.30, "h": 0.22},
        ],
    },
    "hong-kong": {
        "font_key": "hong-kong-heiti",
        "retro_filter": "belle-epoque-print",
        "retro_filter_strength": 0.42,
        "ad_columns": 2,
        "ad_gap": 12,
        "ad_min_width": 180,
        "ad_min_height": 120,
        "snippet_style": "staggered-columns",
        "snippet_columns": 1,
        "floating_ad_slots": [
            {"x": 0.75, "y": 0.470, "w": 0.25, "h": 0.155, "aspect": "tall", "priority": 0},
            {"x": 0.75, "y": 0.655, "w": 0.25, "h": 0.130, "aspect": "square", "priority": 1},
            {"x": 0.00, "y": 0.805, "w": 0.38, "h": 0.140, "aspect": "wide", "priority": 2},
            {"x": 0.42, "y": 0.790, "w": 0.30, "h": 0.160, "aspect": "square", "priority": 3},
            {"x": 0.75, "y": 0.815, "w": 0.25, "h": 0.150, "aspect": "wide", "priority": 4},
            {"x": 0.02, "y": 0.955, "w": 0.68, "h": 0.040, "aspect": "wide", "priority": 5},
        ],
        "ad_box_pattern": [
            {"x": 0.00, "y": 0.00, "w": 1.00, "h": 0.22},
            {"x": 0.04, "y": 0.27, "w": 0.43, "h": 0.26},
            {"x": 0.53, "y": 0.24, "w": 0.43, "h": 0.30},
            {"x": 0.00, "y": 0.59, "w": 0.48, "h": 0.20},
            {"x": 0.54, "y": 0.62, "w": 0.46, "h": 0.20},
            {"x": 0.08, "y": 0.84, "w": 0.84, "h": 0.14},
        ],
    },
    "korea": {
        "font_key": "korean-gothic",
        "retro_filter": "belle-epoque-print",
        "retro_filter_strength": 0.40,
        "ad_columns": 3,
        "ad_gap": 12,
        "ad_min_width": 190,
        "ad_min_height": 105,
        "snippet_style": "staggered-columns",
        "snippet_columns": 1,
        "floating_ad_slots": [
            {"x": 0.75, "y": 0.420, "w": 0.25, "h": 0.145, "aspect": "square", "priority": 0},
            {"x": 0.75, "y": 0.590, "w": 0.25, "h": 0.135, "aspect": "tall", "priority": 1},
            {"x": 0.00, "y": 0.795, "w": 0.34, "h": 0.135, "aspect": "wide", "priority": 2},
            {"x": 0.38, "y": 0.775, "w": 0.28, "h": 0.170, "aspect": "square", "priority": 3},
            {"x": 0.70, "y": 0.785, "w": 0.30, "h": 0.150, "aspect": "wide", "priority": 4},
            {"x": 0.04, "y": 0.955, "w": 0.56, "h": 0.040, "aspect": "wide", "priority": 5},
        ],
        "ad_box_pattern": [
            {"x": 0.00, "y": 0.00, "w": 0.24, "h": 0.78},
            {"x": 0.27, "y": 0.04, "w": 0.21, "h": 0.66},
            {"x": 0.51, "y": 0.00, "w": 0.23, "h": 0.76},
            {"x": 0.77, "y": 0.08, "w": 0.23, "h": 0.68},
            {"x": 0.28, "y": 0.76, "w": 0.30, "h": 0.22},
            {"x": 0.62, "y": 0.78, "w": 0.34, "h": 0.20},
        ],
    },
}


def rgba(hex_color: str) -> tuple[int, int, int, int]:
    return ImageColor.getcolor(hex_color, "RGBA")


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


def centered_text(image: Image.Image, y: int, text: str, scale: int, fill: str) -> None:
    w, _ = measure(text, scale)
    draw_text(image, ((image.width - w) // 2, y), text, scale, fill)


def draw_decor(draw: ImageDraw.ImageDraw, decor: str, box: tuple[int, int, int, int], palette: list[str]) -> None:
    x0, y0, x1, y1 = box
    ink, accent, muted = palette[0], palette[min(4, len(palette) - 1)], palette[min(6, len(palette) - 1)]
    draw.rectangle((x0, y0, x1, y0 + 2), fill=rgba(ink))
    draw.rectangle((x0, y1 - 2, x1, y1), fill=rgba(ink))
    if decor == "nouveau":
        for side in [x0 + 10, x1 - 22]:
            draw.arc((side, y0 + 8, side + 18, y0 + 26), 90, 360, fill=rgba(accent), width=2)
            draw.arc((side, y1 - 28, side + 18, y1 - 10), 180, 450, fill=rgba(muted), width=2)
    elif decor == "section":
        for i, c in enumerate([palette[3], palette[4], palette[6], palette[7]]):
            draw.rectangle((x0 + 10 + i * 16, y0 + 8, x0 + 21 + i * 16, y0 + 19), fill=rgba(c))
    elif decor == "tabs":
        for i, c in enumerate([palette[3], palette[4], palette[7], palette[8]]):
            draw.rectangle((x0 + 10 + i * 20, y0 + 8, x0 + 26 + i * 20, y0 + 14), fill=rgba(c))
            draw.rectangle((x0 + 10 + i * 20, y1 - 15, x0 + 26 + i * 20, y1 - 9), fill=rgba(c))
    elif decor == "civic":
        draw.rectangle((x0 + 8, y0 + 7, x1 - 8, y0 + 14), fill=rgba(accent))
        for i in range(6):
            draw.line((x0 + 12 + i * 28, y0 + 18, x0 + 12 + i * 28, y1 - 8), fill=rgba(muted), width=1)
    elif decor == "neon":
        draw.rectangle((x0 + 6, y0 + 6, x1 - 6, y1 - 6), outline=rgba(accent), width=2)
        draw.rectangle((x0 + 10, y0 + 10, x1 - 10, y1 - 10), outline=rgba(palette[4]), width=1)
    elif decor == "olympic":
        for i, c in enumerate([palette[8], palette[9], palette[10], palette[11], palette[7]]):
            draw.ellipse((x0 + 10 + i * 16, y0 + 8, x0 + 20 + i * 16, y0 + 18), outline=rgba(c), width=2)


def make_masthead(style_key: str, index: int, name: str, style: dict[str, Any]) -> str:
    palette = style["palette"]
    image = Image.new("RGBA", (720, 120), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw_decor(draw, style["decor"], (8, 8, 712, 112), palette)
    scale = 4
    while measure(name, scale)[0] > 620 and scale > 1:
        scale -= 1
    centered_text(image, 44 if scale >= 4 else 48, name, scale, palette[0])
    centered_text(image, 86, "BELLE EPOQUE EDITION", 1, palette[min(4, len(palette) - 1)])
    path = OUT / style_key / f"masthead-{index:02d}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)
    return str(path.relative_to(ROOT))


def make_divider(style_key: str, style: dict[str, Any]) -> str:
    palette = style["palette"]
    image = Image.new("RGBA", (720, 22), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 4, 719, 6), fill=rgba(palette[0]))
    draw.rectangle((0, 12, 719, 13), fill=rgba(palette[min(4, len(palette) - 1)]))
    if style["decor"] in {"section", "tabs", "neon", "olympic"}:
        for i, c in enumerate(palette[3:8]):
            draw.rectangle((12 + i * 18, 0, 22 + i * 18, 17), fill=rgba(c))
    path = OUT / style_key / "divider.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)
    return str(path.relative_to(ROOT))


def make_badge(style_key: str, style: dict[str, Any]) -> str:
    palette = style["palette"]
    paper = style.get("paper_color", palette[9 if len(palette) > 9 else -1])
    ink = style.get("ink_color", palette[0])
    accent = style.get("accent_color", palette[min(4, len(palette) - 1)])
    image = Image.new("RGBA", (180, 46), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 179, 45), outline=rgba(ink), width=2)
    draw.rectangle((4, 4, 175, 14), fill=rgba(accent))
    centered_text(image, 22, "SPECIAL", 2, ink)
    path = OUT / style_key / "badge-special.png"
    image.save(path)
    return str(path.relative_to(ROOT))


def make_ad(style_key: str, index: int, label: str, style: dict[str, Any]) -> str:
    palette = style["palette"]
    paper = style.get("paper_color", palette[9 if len(palette) > 9 else -1])
    ink = style.get("ink_color", palette[0])
    accent = style.get("accent_color", palette[min(4, len(palette) - 1)])
    image = Image.new("RGBA", (180, 88), rgba(paper))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 179, 87), outline=rgba(ink), width=2)
    draw.rectangle((5, 5, 174, 18), fill=rgba(accent))
    draw_text(image, (10, 8), "AD", 1, paper)
    scale = 2 if measure(label, 2)[0] < 140 else 1
    centered_text(image, 28, label, scale, ink)
    # Simple product icon.
    cx, cy = 90, 66
    if label in {"BICYCLE", "TAXI", "SEDAN", "BUS"}:
        draw.ellipse((cx - 38, cy - 10, cx - 24, cy + 4), outline=rgba(ink), width=2)
        draw.ellipse((cx + 24, cy - 10, cx + 38, cy + 4), outline=rgba(ink), width=2)
        draw.line((cx - 31, cy - 3, cx, cy - 18, cx + 31, cy - 3), fill=rgba(ink), width=2)
    elif label in {"PERFUME", "CHOCOLAT", "TEA", "COFFEE"}:
        draw.rectangle((cx - 18, cy - 26, cx + 18, cy + 8), outline=rgba(ink), width=2)
        draw.rectangle((cx - 9, cy - 34, cx + 9, cy - 26), fill=rgba(ink))
    elif label in {"PC SALE", "TV SET", "VHS", "CAMERA"}:
        draw.rectangle((cx - 30, cy - 28, cx + 30, cy + 6), outline=rgba(ink), width=2)
        draw.rectangle((cx - 12, cy + 8, cx + 12, cy + 13), fill=rgba(ink))
    else:
        draw.polygon([(cx, cy - 30), (cx + 28, cy), (cx, cy + 20), (cx - 28, cy)], outline=rgba(ink))
        draw.rectangle((cx - 18, cy - 8, cx + 18, cy + 8), outline=rgba(accent), width=1)
    path = OUT / style_key / f"ad-{index:02d}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)
    return str(path.relative_to(ROOT))


def discover_mastheads(style_key: str) -> list[str]:
    real_dir = OUT / style_key / "real-mastheads"
    historical_dir = OUT / style_key / "historical-mastheads"
    choices = sorted(real_dir.glob("*-choice-*.png"))
    if len(choices) >= 5:
        return [str(path.relative_to(ROOT)) for path in choices[:5]]
    assets = [
        *choices,
        *sorted(real_dir.glob("*.png")),
        *sorted(historical_dir.glob("*.png")),
    ]
    seen: set[Path] = set()
    unique: list[str] = []
    for path in assets:
        if path in seen:
            continue
        seen.add(path)
        unique.append(str(path.relative_to(ROOT)))
        if len(unique) >= 5:
            break
    return unique


def main() -> None:
    layout: dict[str, Any] = {}
    for style_key, style in STYLES.items():
        mastheads = [make_masthead(style_key, i + 1, name, style) for i, name in enumerate(style["mastheads"])]
        ads = [make_ad(style_key, i + 1, label, style) for i, label in enumerate(style["ads"])]
        real_masthead_assets = discover_mastheads(style_key)
        layout_values = {**style["layout"], **STYLE_LAYOUT_UPDATES.get(style_key, {})}
        layout[style_key] = {
            "layout_family": style["layout_family"],
            "decor": style["decor"],
            "real_masthead_name": style["real_masthead_name"],
            "paper_color": style["paper_color"],
            "ink_color": style["ink_color"],
            "accent_color": style["accent_color"],
            "muted_color": style["muted_color"],
            "masthead_names": style["mastheads"],
            "real_masthead_assets": real_masthead_assets,
            "historical_masthead_assets": real_masthead_assets,
            "masthead_assets": mastheads,
            "divider_asset": make_divider(style_key, style),
            "badge_asset": make_badge(style_key, style),
            "advertising_labels": style["ads"],
            "default_ad_assets": ads,
            "use_static_ads_default": False,
            "palette": style["palette"],
            **layout_values,
        }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "layout-templates.json").write_text(json.dumps(layout, indent=2, ensure_ascii=False), encoding="utf-8")
    print(OUT / "layout-templates.json")


if __name__ == "__main__":
    main()
