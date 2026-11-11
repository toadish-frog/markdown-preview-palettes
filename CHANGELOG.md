# Changelog

All notable changes to this extension. Versions follow Semantic Versioning (Major.Minor.Patch).

## 0.4.0 (2026-11-12)

- New preset `onyx`: white headings on near-black (white page in light themes), amber bold, orange inline code, soft blue links, and blue, green and amber callouts.
- New preset `graphite`, in a docs style: white or black headings, grey text, orange inline code without a box, dotted link underlines, tables with a line under each row only, and grey callouts (muted amber for warnings).
- New preset options: `linkUnderline: "dotted"`, `codePlain`, `codeLinks`, `tableRowLines`, and per-callout `code`, `codeBg`, `codeBgAlpha`, `icon` and `underline` colours. Existing presets look the same as before.

## 0.3.0 (2026-11-06)

- `ember` now follows the Claude Code docs, dark and light: near-black (`#09090b`) or off-white (`#fdfdf7`) background, grey text, white headings, links with an orange (dark) or black (light) bottom-border underline that thickens on hover, inline code and code-block boxes, and tables with striped rows and column lines.
- `ember`: GitHub alerts `> [!TIP]`, `> [!NOTE]` / `> [!INFO]` and `> [!WARNING]` become green, blue and yellow callouts, also when Markdown All in One renders them. Other presets show them as plain quotes, as before.
- `folio`: links within the document or to other files are underlined on hover only; web and mail links keep the underline. Tables match the Claude Platform docs: shaded header row with brighter, medium-weight text, rounded corners and soft lines, plus the striped rows and column lines. GitHub alerts become the docs' blue note, green tip and orange warning callouts, also when Markdown All in One renders them.
- Presets can set table colours and rounded corners (`tableBg`, `tableHead`, `tableBorder`, `tableHeadBorder`, `tableHeadBg`, their opacities, `tableRadius`, `tableHeadWeight`), `linkUnderline: "external"`, link borders and weight, inline-code shape, code-block boxes, callout colours and callout icon size (`alertIcon`, `alertIconGap`).

## 0.2.0 (2026-11-05)

- New presets: `phosphor` (terminal greens), `parchment` (gold on beige paper), `azure` (clean blue), `ember` (orange and warm greys on black or beige paper) and `folio` (document style, warm grey text).
- Presets can set the body text colour (optional `text` key), the inline-code box and border opacity (`codeTintAlpha`, `codeBorderAlpha`) and link underlines (`linkUnderline`).
- Tables use the GitHub style in every preset: full grid border (outer edge, rows and columns) and striped rows.

## 0.1.0 (2026-10-13)

- First version: presets `teal` (default), `plum`, `crimson`, `golden`, `mono` and `default` (built-in look).
- Colours for headings H1 to H6, bold text, inline code, inline code inside links, `>` and `>>` quotes, and links.
- Dark and light version of every preset; high-contrast themes keep the built-in look.
- Preset setting `markdownPreviewPalettes.preset`; open previews refresh when it changes.
