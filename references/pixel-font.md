# Shared Pixel Font

Use `assets/pixel-font-5x7.json` for every deliberately readable text element in the final artwork:

- final watermark
- storefront signs
- posters
- station/platform labels
- newspaper headlines
- event banners
- tiny date markers

The font is a 5x7 uppercase bitmap alphabet with digits and basic punctuation. Each glyph is an array of seven strings, where `1` is an inked pixel and `0` is empty. Use integer scaling only: 1x, 2x, 3x, etc. Do not antialias, blur, rotate freely, or use proportional/vector fonts for readable text.

## Drawing Rules

- Convert readable text to uppercase before drawing.
- Keep phrases short. Prefer `JULY 1`, `PARIS`, `EXPO`, `METRO`, `OPEN`, `NO. 1`, or abstract initials over long sentences.
- Use this font for any readable Latin text. For non-Latin local signs, use abstract glyph blocks or very short romanized labels, unless the user explicitly asks for native script.
- Use palette colors only. Add a one-pixel dark shadow or backing plate when text sits over busy art.
- Let signs and posters carry atmosphere, but avoid real logos and long readable copyrighted text.
- Font weight must keep the same 5x7 glyph skeleton. Use `bold` by drawing the glyph again with a one-pixel horizontal offset, `regular` as the base glyph, and `thin` as the base glyph with lighter ink alpha or lower contrast.
- In newspapers, use `bold` for headline and ad labels, `regular` for decks/snippet headings, and `thin` for issue lines, captions, report fill, and ad copy.

## Worker Contract Addition

When a worker creates a sprite containing readable text, include this in the sprite metadata:

```json
{
  "text_font": "pixel-font-5x7",
  "text": "JULY 1",
  "text_scale": 2
}
```

If a sprite has decorative unreadable sign strokes only, mark:

```json
{
  "text_font": "abstract-glyphs",
  "text": null
}
```
