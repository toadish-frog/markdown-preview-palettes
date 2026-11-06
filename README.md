# Markdown Preview Palettes

[![VS Marketplace version](https://vsmarketplacebadges.dev/version-short/ToadishFrog67.markdown-preview-colours.svg)](https://marketplace.visualstudio.com/items?itemName=ToadishFrog67.markdown-preview-colours)
[![CI](https://github.com/toadish-frog/markdown-preview-palettes/actions/workflows/ci.yml/badge.svg)](https://github.com/toadish-frog/markdown-preview-palettes/actions/workflows/ci.yml)

Colour presets for the built-in VS Code Markdown preview. Headings, bold text, inline code, quotes and links each get their own colour, so long notes are easier to scan.

- **Preview only:** Markdown files are never changed.
- **Dark and light:** every preset has a version for each theme. High-contrast themes keep the built-in look.
- **Readable:** every colour meets the WCAG contrast minimum (4.5:1 for text, 3:1 for the two largest headings). The build fails otherwise.

## Presets

| Preset | Headings | Bold | Inline code | Links | Background (dark theme) |
| --- | --- | --- | --- | --- | --- |
| `teal` (default) | Green-teal family | Amber | Muted orange | VS Code blue | Theme default |
| `plum` | Plum and lavender | Yellow | Red | Light blue | Charcoal |
| `crimson` | Red | White | Steel grey | Cyan | Near-black |
| `golden` | Gold, amber, orange | White | Ivory | Teal | Near-black |
| `mono` | Greyscale | Brightest white | Light grey | VS Code blue | Theme default |
| `phosphor` | Terminal greens | Pale green | Lime | Cyan | Green-black |
| `parchment` | Gold and brown | Cream | Orange | Light blue | Warm charcoal (beige paper in light themes) |
| `azure` | Blue | White | Light blue | VS Code blue | Theme default |
| `ember` | White and light grey | Off-white | Light grey | Off-white, orange underline | Near-black (off-white paper in light themes) |
| `folio` | Near-white, one shade for every level | Near-white | Soft red | Light blue | Charcoal (off-white in light themes) |
| `default` | Built-in VS Code look (all colouring off) | | | | |

`parchment` uses colours from the Apache 2.0 [brand-guidelines skill](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines) (Light `#faf9f5`, Dark `#141413`, Mid Gray `#b0aea5`, Light Gray `#e8e6dc`, Orange `#d97757`, Blue `#6a9bcc`, Green `#788c5d`). In light themes, some are darkened slightly to meet the contrast minimum.

`ember` follows the colours of the [Claude Code docs](https://code.claude.com/docs) in their dark and light modes: text, headings, links with an orange (dark) or black (light) underline, inline code, code-block boxes, tables and the green tip, blue note and yellow warning callouts. Only colour values and box sizes are reused; no fonts, icons or site code.

## Switch Preset

1. Open Settings (`Ctrl+,` or `Cmd+,`) and search for **Markdown Preview Palettes**.
2. Pick a preset. Open previews refresh straight away.

Or in `settings.json`:

```json
"markdownPreviewPalettes.preset": "golden"
```

The setting can also be set per workspace.

## What Gets Coloured

- **Headings:** one shade per level, H1 to H6.
- **Bold text:** bold inside a heading or link keeps the heading or link colour.
- **Inline code:** coloured, in a tinted box. Inline code inside a link, `` [`text`](url) ``, takes the link colour.
- **Quotes:** `>` and nested `>>` each have their own colour.
- **Callouts:** in `ember` and `folio`, GitHub alerts `> [!TIP]` (green), `> [!NOTE]` or `> [!INFO]` (blue) and `> [!WARNING]` (yellow in `ember`, orange in `folio`) become coloured boxes; inline code and links inside take the callout colour. With [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one) installed, its alert boxes get the same colours, keep its icon and hide its title word. Other presets show them as plain quotes.
- **Links:** some presets set their own link colour; the others keep the VS Code link colour. `folio` underlines web and mail links; links within the document or to other files show the underline on hover only.
- **Tables:** GitHub style, with a full grid border and striped rows. `folio` follows the Claude Platform docs: a shaded header row, rounded corners and soft lines.
- **Code blocks:** syntax colours always stay the VS Code ones. `ember` also gives the box its own background, border and rounded corners.

## Development

Requirements: Python 3.8+ and Git. Node.js (for the extension tests and Markdown lint) and Ruff (for Python formatting) are used by CI and are optional locally.

| Command | What it does |
| --- | --- |
| `make css` | Generate `media/preview.css` from `palettes/palettes.json` and run the contrast check |
| `make test` | Python and extension unit tests |
| `make lint` | Formatting and lint checks |
| `make package` | Build `dist/markdown-preview-colours-<version>.vsix` for local testing (publish with `npx @vscode/vsce package`) |

- **Colours:** edit `palettes/palettes.json`, then run `make css`. Never edit `media/preview.css` by hand.
- **Try it:** open the folder in VS Code and press `F5`; `test/sample.md` opens in a development window.
- **How it works:** `extension.js` adds a hidden marker naming the chosen preset to each preview; `media/preview.css` applies that preset's colours.
- **Project tracking:** see `docs/project-tracker.md` and `docs/release-guide.md`.

## Licence

MIT. See `LICENSE`.
