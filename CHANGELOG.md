# Changelog

All notable changes to this extension. Versions follow Semantic Versioning (Major.Minor.Patch).

## Unreleased

- New presets: `phosphor` (terminal greens), `parchment` (gold on beige paper), `azure` (clean blue) and `ember` (orange and warm greys on black or beige paper) and `folio` (document style, warm grey text).
- Presets can set the body text colour (optional `text` key), the inline-code box and border opacity (`codeTintAlpha`, `codeBorderAlpha`) and link underlines (`linkUnderline`).
- Tables use the GitHub style in every preset: full grid border (outer edge, rows and columns) and striped rows.

## 0.1.0 (2026-10-13)

- First version: presets `teal` (default), `plum`, `crimson`, `golden`, `mono` and `default` (built-in look).
- Colours for headings H1 to H6, bold text, inline code, inline code inside links, `>` and `>>` quotes, and links.
- Dark and light version of every preset; high-contrast themes keep the built-in look.
- Preset setting `markdownPreviewPalettes.preset`; open previews refresh when it changes.
