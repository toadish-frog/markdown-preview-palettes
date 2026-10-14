# Markdown Preview Palettes

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
| `default` | Built-in VS Code look (all colouring off) | | | | |

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
- **Links:** some presets set their own link colour; the others keep the VS Code link colour.
- **Code blocks:** never changed; they keep the VS Code syntax colours.

## Development

Requirements: Python 3.8+ and Git. Node.js (for the extension tests and Markdown lint) and Ruff (for Python formatting) are used by CI and are optional locally.

| Command | What it does |
| --- | --- |
| `make css` | Generate `media/preview.css` from `palettes/palettes.json` and run the contrast check |
| `make test` | Python and extension unit tests |
| `make lint` | Formatting and lint checks |
| `make package` | Build `dist/markdown-preview-palettes-<version>.vsix` |

- **Colours:** edit `palettes/palettes.json`, then run `make css`. Never edit `media/preview.css` by hand.
- **Try it:** open the folder in VS Code and press `F5`; `test/sample.md` opens in a development window.
- **How it works:** `extension.js` adds a hidden marker naming the chosen preset to each preview; `media/preview.css` applies that preset's colours.
- **Project tracking:** see `docs/project-tracker.md` and `docs/release-guide.md`.

## Licence

MIT. See `LICENSE`.
