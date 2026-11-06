#!/usr/bin/env python3
"""Build tool for Markdown Preview Palettes. Python 3.8+, standard library only.

Commands (run from anywhere):
  python3 scripts/build.py css      Generate media/preview.css from palettes/palettes.json, then run the contrast check
  python3 scripts/build.py check    Contrast check only
  python3 scripts/build.py package  css + check, then build dist/<name>-<version>.vsix (for local install and testing)
"""

import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
PALETTES = ROOT / "palettes" / "palettes.json"
CSS_OUT = ROOT / "media" / "preview.css"
DIST = ROOT / "dist"

THEMES = ("dark", "light")
# Preview background assumed when a preset keeps the theme's own (VS Code Dark Modern / Light Modern)
DEFAULT_BG = {"dark": "#1f1f1f", "light": "#ffffff"}
# Opacity of derived tints and borders
ALPHA = {
    "dark": {"code": 0.12, "quote": 0.08, "h1Border": 0.35, "h2Border": 0.30},
    "light": {"code": 0.08, "quote": 0.06, "h1Border": 0.30, "h2Border": 0.25},
}
REQUIRED = ("h1", "h2", "h3", "h4", "h5", "h6", "bold", "code", "quote", "quoteBar", "quote2", "quote2Bar")
OPTIONAL = (
    "background",
    "text",
    "link",
    "linkHover",
    "codeTint",
    "tableBg",
    "tableHead",
    "tableBorder",
    "tableHeadBorder",
    "linkBorder",
    "preBg",
    "preBorder",
)
# Non-colour options: opacities (0 to 1), sizes in whole pixels and on/off switches
NUMBERS = ("codeTintAlpha", "codeBorderAlpha", "tableBorderAlpha", "tableHeadBorderAlpha", "preBorderAlpha")
PIXELS = {
    "tableRadius": (1, 32),
    "codeRadius": (1, 32),
    "preRadius": (1, 32),
    "alertRadius": (1, 32),
    "linkWeight": (100, 900),
}
# Padding as CSS lengths in whole pixels, for example "2px 8px"
PADDINGS = ("codePadding", "prePadding", "alertPadding")
PADDING = re.compile(r"^\d{1,2}px( \d{1,2}px){0,3}$")
# Callout boxes for GitHub alerts (> [!NOTE], > [!TIP], > [!WARNING]); [!INFO] uses the note colours
ALERT_TYPES = ("note", "tip", "warning")
ALERT_KEYS = {"text": True, "bg": True, "border": True, "bgAlpha": False}
FLAGS = ("linkUnderline",)
PRESET_NAME = re.compile(r"^[a-z][a-z0-9-]{0,30}$")
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
# WCAG minimum contrast: 3.0 for large text (H1, H2), 4.5 for everything else
MIN_LARGE, MIN_TEXT = 3.0, 4.5

# Preset is active (marker present) and the theme is plain dark or light; high-contrast keeps VS Code defaults
SCOPE = "body:is(.vscode-dark, .vscode-light):not(.vscode-high-contrast):has(.mpp-preset)"
# Links that leave the document: web and mail addresses (data-href holds the link target as written)
EXTERNAL_LINK = '[data-href^="http:" i], [data-href^="https:" i], [data-href^="mailto:" i]'
# Table lines when a preset sets no table colours: the text colour mixed into the background
TABLE_BORDER = "color-mix(in srgb, currentColor 20%, transparent)"
TABLE_HEAD_BORDER = f"var(--mpp-table-head-border, var(--mpp-table-border, {TABLE_BORDER}))"


# ---------- Palette loading and validation ----------


def load_palettes(path=PALETTES):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    presets = {k: v for k, v in data.items() if not k.startswith("_")}
    errors = validate(presets)
    if errors:
        sys.exit("Palette errors:\n  " + "\n  ".join(errors))
    return presets


def validate(presets):
    """Return a list of problems; empty when every preset is complete and well-formed."""
    errors = []
    for name, preset in presets.items():
        if not PRESET_NAME.match(name) or name == "default":
            errors.append(f"{name}: invalid preset name")
        for theme in THEMES:
            colours = preset.get(theme)
            if not isinstance(colours, dict):
                errors.append(f"{name}.{theme}: missing")
                continue
            for key in REQUIRED:
                if key not in colours:
                    errors.append(f"{name}.{theme}.{key}: missing")
            for key, value in colours.items():
                if key in NUMBERS:
                    if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 < value <= 1:
                        errors.append(f"{name}.{theme}.{key}: '{value}' is not a number above 0, up to 1")
                elif key in PIXELS:
                    low, high = PIXELS[key]
                    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
                        errors.append(f"{name}.{theme}.{key}: '{value}' is not a whole number from {low} to {high}")
                elif key == "linkUnderline":
                    if value is not True and value != "external":
                        errors.append(f'{name}.{theme}.{key}: must be true, "external" (or left out)')
                elif key in FLAGS:
                    if value is not True:
                        errors.append(f"{name}.{theme}.{key}: must be true (or left out)")
                elif key in PADDINGS:
                    if not isinstance(value, str) or not PADDING.match(value):
                        errors.append(f"{name}.{theme}.{key}: '{value}' is not 1 to 4 lengths like \"2px 8px\"")
                elif key == "alerts":
                    errors += validate_alerts(f"{name}.{theme}.alerts", value)
                elif key not in REQUIRED + OPTIONAL:
                    errors.append(f"{name}.{theme}.{key}: unknown key")
                elif not isinstance(value, str) or not HEX.match(value):
                    errors.append(f"{name}.{theme}.{key}: '{value}' is not #rrggbb")
    return errors


def validate_alerts(where, alerts):
    """Each alert type needs text, bg and border colours; bgAlpha (0 to 1) is optional."""
    if not isinstance(alerts, dict):
        return [f"{where}: must be an object"]
    errors = [f"{where}.{kind}: unknown alert type" for kind in alerts if kind not in ALERT_TYPES]
    for kind in ALERT_TYPES:
        box = alerts.get(kind)
        if not isinstance(box, dict):
            errors.append(f"{where}.{kind}: missing")
            continue
        for key, required in ALERT_KEYS.items():
            if required and key not in box:
                errors.append(f"{where}.{kind}.{key}: missing")
        for key, value in box.items():
            if key == "bgAlpha":
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 < value <= 1:
                    errors.append(f"{where}.{kind}.{key}: '{value}' is not a number above 0, up to 1")
            elif key not in ALERT_KEYS:
                errors.append(f"{where}.{kind}.{key}: unknown key")
            elif not isinstance(value, str) or not HEX.match(value):
                errors.append(f"{where}.{kind}.{key}: '{value}' is not #rrggbb")
    return errors


# ---------- Colour maths ----------


def rgb(hex_colour):
    return tuple(int(hex_colour[i : i + 2], 16) for i in (1, 3, 5))


def rgba(hex_colour, alpha):
    r, g, b = rgb(hex_colour)
    return f"rgba({r}, {g}, {b}, {alpha:.2f})"


def blend(top_hex, alpha, base_rgb):
    return tuple(round(t * alpha + b * (1 - alpha)) for t, b in zip(rgb(top_hex), base_rgb))


def luminance(channels):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (lin(c) for c in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg_rgb, bg_rgb):
    hi, lo = sorted((luminance(fg_rgb), luminance(bg_rgb)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


# ---------- Contrast check ----------


def check(presets, quiet=False):
    """Print one line per preset and theme; exit non-zero when any colour is below its minimum."""
    failures = 0
    for name, preset in presets.items():
        for theme in THEMES:
            c = preset[theme]
            a = ALPHA[theme]
            base = rgb(c.get("background", DEFAULT_BG[theme]))
            quote_bg = blend(c["quoteBar"], a["quote"], base)
            pairs = [(f"h{i}", c[f"h{i}"], base, MIN_LARGE if i <= 2 else MIN_TEXT) for i in range(1, 7)]
            pairs += [
                ("bold", c["bold"], base, MIN_TEXT),
                ("code", c["code"], blend(c.get("codeTint", c["code"]), code_alpha(c, theme), base), MIN_TEXT),
                ("quote", c["quote"], quote_bg, MIN_TEXT),
                ("quote2", c["quote2"], blend(c["quote2Bar"], a["quote"], quote_bg), MIN_TEXT),
            ]
            if "text" in c:
                pairs.append(("text", c["text"], base, MIN_TEXT))
            if "link" in c:
                pairs.append(("link", c["link"], base, MIN_TEXT))
            # Table text sits on the table surface when the preset sets one
            table_bg = rgb(c["tableBg"]) if "tableBg" in c else base
            if "tableHead" in c:
                pairs.append(("tableHead", c["tableHead"], table_bg, MIN_TEXT))
            if "tableBg" in c and "text" in c:
                pairs.append(("table text", c["text"], table_bg, MIN_TEXT))
            for kind, box in c.get("alerts", {}).items():
                pairs.append((f"{kind} alert", box["text"], blend(box["bg"], box.get("bgAlpha", 1), base), MIN_TEXT))
            bad = [
                (k, round(contrast(rgb(fg), bg), 2), need) for k, fg, bg, need in pairs if contrast(rgb(fg), bg) < need
            ]
            status = "ok" if not bad else "FAIL " + ", ".join(f"{k} {r}:1 (needs {n})" for k, r, n in bad)
            if not quiet:
                print(f"  {name:8} {theme:5} {status}")
            failures += len(bad)
    if failures:
        sys.exit(f"Contrast check failed: {failures} colour(s) below the minimum.")
    if not quiet:
        print("Contrast check passed.")


# ---------- CSS generation ----------


def code_alpha(c, theme):
    return c.get("codeTintAlpha", ALPHA[theme]["code"])


def preset_block(name, theme, c):
    a = ALPHA[theme]
    scope = f'body.vscode-{theme}:not(.vscode-high-contrast):has(.mpp-preset[data-preset="{name}"])'
    tint = c.get("codeTint", c["code"])
    lines = [f"{scope} {{"]
    if "background" in c:
        lines.append(f"  background-color: {c['background']};")
    if "text" in c:
        lines.append(f"  color: {c['text']};")
    if "link" in c:
        lines.append(f"  --vscode-textLink-foreground: {c['link']};")
        lines.append(f"  --vscode-textLink-activeForeground: {c.get('linkHover', c['link'])};")
    for i in range(1, 7):
        lines.append(f"  --mpp-h{i}: {c[f'h{i}']};")
    lines += [
        f"  --mpp-h1-border: {rgba(c['h1'], a['h1Border'])};",
        f"  --mpp-h2-border: {rgba(c['h2'], a['h2Border'])};",
        f"  --mpp-bold: {c['bold']};",
        f"  --mpp-code: {c['code']};",
        f"  --mpp-code-bg: {rgba(tint, code_alpha(c, theme))};",
        f"  --mpp-quote: {c['quote']};",
        f"  --mpp-quote-bar: {c['quoteBar']};",
        f"  --mpp-quote-bg: {rgba(c['quoteBar'], a['quote'])};",
        f"  --mpp-quote2: {c['quote2']};",
        f"  --mpp-quote2-bar: {c['quote2Bar']};",
        f"  --mpp-quote2-bg: {rgba(c['quote2Bar'], a['quote'])};",
    ]
    if "codeBorderAlpha" in c:
        lines.append(f"  --mpp-code-border: 0.5px solid {rgba(tint, c['codeBorderAlpha'])};")
    if "tableBg" in c:
        lines.append(f"  --mpp-table-bg: {c['tableBg']};")
    if "tableHead" in c:
        lines.append(f"  --mpp-table-head: {c['tableHead']};")
    if "tableBorder" in c:
        lines.append(f"  --mpp-table-border: {rgba(c['tableBorder'], c.get('tableBorderAlpha', 1))};")
    if "tableHeadBorder" in c:
        lines.append(f"  --mpp-table-head-border: {rgba(c['tableHeadBorder'], c.get('tableHeadBorderAlpha', 1))};")
    lines.append("}")
    lines += extra_rules(scope, c)
    if "tableRadius" in c:
        # Rounded corners need separate borders: each cell draws its top and left line, the table draws the outer edge
        lines += [
            f"{scope} table {{",
            "  border-collapse: separate;",
            f"  border: 1px solid var(--mpp-table-border, {TABLE_BORDER});",
            f"  border-radius: {c['tableRadius']}px;",
            "  overflow: hidden;",
            "}",
            f"{scope} :is(th, td) {{ border-width: 1px 0 0 1px; }}",
            f"{scope} :is(th, td):first-child {{ border-left-width: 0; }}",
            f"{scope} thead :is(th, td) {{ border-top-width: 0; }}",
            f"{scope} tbody tr:first-child > td {{ border-top-color: {TABLE_HEAD_BORDER}; }}",
        ]
    underline = c.get("linkUnderline")
    if underline:
        # Underline at 40% of the link colour, full colour on hover.
        # "external": only web and mail links are underlined; links inside the document or to other files
        # show the underline on hover only (VS Code keeps each link's original target in data-href).
        links = f"{scope} a:is({EXTERNAL_LINK})" if underline == "external" else f"{scope} a"
        lines += [
            f"{links} {{",
            "  text-decoration: underline;",
            "  text-decoration-color: color-mix(in srgb, currentColor 40%, transparent);",
            "  text-underline-offset: 3px;",
            "}",
            f"{scope} a:hover {{",
            "  text-decoration: underline;",
            "  text-decoration-color: currentColor;",
            "  text-underline-offset: 3px;",
            "}",
        ]
    return "\n".join(lines)


def extra_rules(scope, c):
    """Optional per-preset rules: link border underline, inline-code shape, code-block box, alert callouts."""
    lines = []
    link = []
    if "linkWeight" in c:
        link.append(f"  font-weight: {c['linkWeight']};")
    if "linkBorder" in c:
        # Underline drawn as a bottom border, as on the Claude Code docs; thicker on hover
        link += ["  text-decoration: none;", f"  border-bottom: 1px solid {c['linkBorder']};"]
    if link:
        lines += [f"{scope} a {{", *link, "}"]
    if "linkBorder" in c:
        lines.append(f"{scope} a:hover {{ text-decoration: none; border-bottom-width: 2px; }}")
    code = []
    if "codeRadius" in c:
        code.append(f"  border-radius: {c['codeRadius']}px;")
    if "codePadding" in c:
        code.append(f"  padding: {c['codePadding']};")
    if code:
        lines += [f"{scope} :not(pre) > code {{", *code, "}"]
    if "preBg" in c:
        # The box only: syntax colours inside code blocks always stay the VS Code ones
        box = [f"  --vscode-textCodeBlock-background: {c['preBg']};", f"  background-color: {c['preBg']};"]
        if "preBorder" in c:
            box.append(f"  border: 1px solid {rgba(c['preBorder'], c.get('preBorderAlpha', 1))};")
        if "preRadius" in c:
            box.append(f"  border-radius: {c['preRadius']}px;")
        lines += [f"{scope} pre {{", *box, "}", f"{scope} pre.hljs {{ overflow: hidden; }}"]
        if "prePadding" in c:
            lines.append(f"{scope} :is(pre:not(.hljs), pre.hljs code > div) {{ padding: {c['prePadding']}; }}")
    if "alerts" in c:
        # extension.js marks > [!NOTE], > [!INFO], > [!TIP] and > [!WARNING] quotes; other presets show them as quotes
        box = ["  margin: 16px 0;", "  border: 1px solid;"]
        if "alertRadius" in c:
            box.append(f"  border-radius: {c['alertRadius']}px;")
        if "alertPadding" in c:
            box.append(f"  padding: {c['alertPadding']};")
        # Markdown All in One (markdown-it-github-alerts) turns the same quotes into
        # <div class="markdown-alert markdown-alert-tip"> with an icon title before extension.js sees them
        theirs = f".markdown-alert:is({', '.join(f'.markdown-alert-{kind}' for kind in ALERT_TYPES)})"
        alert = f":is(.mpp-alert, {theirs})"
        lines += [f"{scope} :is(blockquote.mpp-alert, {theirs}) {{", *box, "}"]
        for kind in ALERT_TYPES:
            a = c["alerts"][kind]
            lines.append(
                f"{scope} :is(blockquote.mpp-alert-{kind}, .markdown-alert.markdown-alert-{kind}) {{ color: {a['text']}; "
                f"background-color: {rgba(a['bg'], a.get('bgAlpha', 1))}; border-color: {a['border']}; }}"
            )
        lines += [
            f"{scope} {alert} :is(strong, code, a) {{ color: inherit; }}",
            f"{scope} {alert} a {{ border-bottom-color: currentColor; }}",
            f"{scope} :is(.mpp-alert-marker, .mpp-alert-marker + br, .mpp-alert-title-only) {{ display: none; }}",
            f"{scope} {alert} > :last-child {{ margin-bottom: 0; }}",
        ]
        lines += alert_icon_rules(scope, theirs, c.get("alertPadding"))
    return lines


ICON_SIZE, ICON_COLUMN, ICON_GAP = 18, 16, 12  # the docs site: 18px icon in a 16px column, 12px gap


def alert_icon_rules(scope, theirs, padding):
    """Keep the other extension's icon in a left column, like the docs site, and hide its title word."""
    title = f"{scope} {theirs} > .markdown-alert-title"
    if not padding:
        return [f"{title} {{ display: none; }}"]
    sides = [int(part[:-2]) for part in padding.split()]
    top, left = sides[0], sides[{1: 0, 2: 1, 3: 1, 4: 3}[len(sides)]]
    return [
        f"{scope} {theirs} {{ position: relative; padding-left: {left + ICON_COLUMN + ICON_GAP}px; }}",
        f"{title} {{ position: absolute; top: {top + 2}px; left: {left}px; margin: 0; font-size: 0; line-height: 0; color: inherit; }}",
        f"{title} svg {{ width: {ICON_SIZE}px; height: {ICON_SIZE}px; margin: 0; }}",
        f"{title} + * {{ margin-top: 0; }}",
    ]


def render_css(presets):
    S = SCOPE
    blocks = [preset_block(n, t, p[t]) for n, p in presets.items() for t in THEMES]
    rules = f"""
/* ---------- Rules (shared by every preset) ---------- */

{S} h1 {{ color: var(--mpp-h1); border-bottom-color: var(--mpp-h1-border); }}
{S} h2 {{ color: var(--mpp-h2); border-bottom-color: var(--mpp-h2-border); }}
{S} h3 {{ color: var(--mpp-h3); }}
{S} h4 {{ color: var(--mpp-h4); }}
{S} h5 {{ color: var(--mpp-h5); }}
{S} h6 {{ color: var(--mpp-h6); }}

{S} strong {{ color: var(--mpp-bold); }}

/* Inline code only; code blocks (pre > code) keep the VS Code default */
{S} :not(pre) > code {{
  color: var(--mpp-code);
  background-color: var(--mpp-code-bg);
  border: var(--mpp-code-border, 0);
  border-radius: 3px;
  padding: 1px 4px;
}}

{S} blockquote {{
  color: var(--mpp-quote);
  border-left-color: var(--mpp-quote-bar);
  background-color: var(--mpp-quote-bg);
}}
{S} blockquote blockquote {{
  color: var(--mpp-quote2);
  border-left-color: var(--mpp-quote2-bar);
  background-color: var(--mpp-quote2-bg);
}}

/* Tables, GitHub style: full grid border and striped body rows.
   Tints mix the text colour into the background, so they suit every preset and theme.
   A preset can set its own surface, header text and line colours (--mpp-table-*). */
{S} table {{
  border-collapse: collapse;
  border-spacing: 0;
  background-color: var(--mpp-table-bg, transparent);
}}
{S} :is(th, td) {{
  padding: 6px 13px;
  border: 1px solid var(--mpp-table-border, {TABLE_BORDER});
}}
{S} th {{ color: var(--mpp-table-head, inherit); }}
{S} thead :is(th, td) {{ border-bottom-color: {TABLE_HEAD_BORDER}; }}
{S} tbody tr:nth-child(2n) {{ background-color: color-mix(in srgb, currentColor 5%, transparent); }}

/* ---------- Exceptions ---------- */

/* Bold inside a heading or link keeps the heading or link colour */
{S} :is(h1, h2, h3, h4, h5, h6, a) strong {{ color: inherit; }}

/* Inline code inside a link, [`text`](url), takes the link colour.
   Must stay after the inline-code rule: same specificity, so the later rule wins. */
{S} a code {{
  color: inherit;
  background-color: color-mix(in srgb, currentColor 12%, transparent);
}}
"""
    header = (
        "/*\n"
        " * Markdown Preview Palettes\n"
        " * GENERATED by scripts/build.py from palettes/palettes.json. Do not edit by hand.\n"
        " * Preview only; Markdown files are never changed. High-contrast themes keep the VS Code defaults.\n"
        " */\n\n"
        "/* ---------- Preset colours (one block per preset and theme) ---------- */\n\n"
    )
    return header + "\n\n".join(blocks) + "\n" + rules


def build_css(presets):
    CSS_OUT.parent.mkdir(exist_ok=True)
    CSS_OUT.write_text(render_css(presets), encoding="utf-8")
    print(f"Wrote {CSS_OUT.relative_to(ROOT)} ({len(presets)} presets).")


# ---------- File lists (exact .gitignore / .vscodeignore rules, via git, without a repository) ----------


def list_files(*exclude_args):
    with tempfile.TemporaryDirectory() as git_dir:
        subprocess.run(["git", "init", "-q", "--bare", git_dir], check=True)
        out = subprocess.run(
            ["git", f"--git-dir={git_dir}", f"--work-tree={ROOT}", "ls-files", "--others", *exclude_args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    return sorted(Path(line) for line in out.splitlines() if line)


# ---------- VSIX packaging ----------


def build_vsix():
    pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    files = list_files("--exclude-standard", "--exclude-from=.vscodeignore")
    missing = [
        f for f in ("package.json", "extension.js", "media/preview.css", "README.md", "LICENSE") if Path(f) not in files
    ]
    if missing:
        sys.exit(f"Missing from package: {missing}")

    def target(path):
        return "extension/LICENSE.txt" if path == Path("LICENSE") else f"extension/{path.as_posix()}"

    exts = sorted({Path(target(f)).suffix for f in files} | {".vsixmanifest"})
    types = {
        ".json": "application/json",
        ".js": "application/javascript",
        ".css": "text/css",
        ".md": "text/markdown",
        ".txt": "text/plain",
        ".vsixmanifest": "text/xml",
        ".png": "image/png",
    }
    content_types = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        + "".join(f'<Default Extension="{e}" ContentType="{types.get(e, "application/octet-stream")}" />' for e in exts)
        + "</Types>\n"
    )
    assets = [
        ("Microsoft.VisualStudio.Code.Manifest", "extension/package.json"),
        ("Microsoft.VisualStudio.Services.Content.Details", "extension/README.md"),
        ("Microsoft.VisualStudio.Services.Content.License", "extension/LICENSE.txt"),
    ]
    if Path("CHANGELOG.md") in files:
        assets.append(("Microsoft.VisualStudio.Services.Content.Changelog", "extension/CHANGELOG.md"))
    manifest = f"""<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">
  <Metadata>
    <Identity Language="en-US" Id="{escape(pkg["name"])}" Version="{escape(pkg["version"])}" Publisher="{escape(pkg["publisher"])}" />
    <DisplayName>{escape(pkg["displayName"])}</DisplayName>
    <Description xml:space="preserve">{escape(pkg["description"])}</Description>
    <Tags>{escape(",".join(pkg.get("keywords", [])))}</Tags>
    <Categories>{escape(",".join(pkg.get("categories", [])))}</Categories>
    <GalleryFlags>Public</GalleryFlags>
    <Properties>
      <Property Id="Microsoft.VisualStudio.Code.Engine" Value="{escape(pkg["engines"]["vscode"])}" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionDependencies" Value="" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionPack" Value="" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="workspace" />
      <Property Id="Microsoft.VisualStudio.Code.ExecutesCode" Value="true" />
    </Properties>
    <License>extension/LICENSE.txt</License>
  </Metadata>
  <Installation>
    <InstallationTarget Id="Microsoft.VisualStudio.Code" />
  </Installation>
  <Dependencies />
  <Assets>
{chr(10).join(f'    <Asset Type="{t}" Path="{p}" Addressable="true" />' for t, p in assets)}
  </Assets>
</PackageManifest>
"""
    DIST.mkdir(exist_ok=True)
    out = DIST / f"{pkg['name']}-{pkg['version']}.vsix"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("extension.vsixmanifest", manifest)
        for f in files:
            z.write(ROOT / f, target(f))
    print(f"Wrote {out.relative_to(ROOT)} ({len(files)} files): " + ", ".join(f.as_posix() for f in files))


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "check":
        check(load_palettes())
    elif command == "css":
        presets = load_palettes()
        check(presets)
        build_css(presets)
    elif command == "package":
        presets = load_palettes()
        check(presets)
        build_css(presets)
        build_vsix()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
