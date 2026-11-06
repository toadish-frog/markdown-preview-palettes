"""Unit tests for scripts/build.py. Run: python3 -m unittest discover -s test -v"""

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build  # noqa: E402


class ColourMaths(unittest.TestCase):
    def test_contrast_extremes(self):
        self.assertAlmostEqual(build.contrast((0, 0, 0), (255, 255, 255)), 21.0, places=2)
        self.assertAlmostEqual(build.contrast((120, 120, 120), (120, 120, 120)), 1.0, places=2)

    def test_blend_and_rgba(self):
        self.assertEqual(build.blend("#ffffff", 0.5, (0, 0, 0)), (128, 128, 128))
        self.assertEqual(build.rgba("#ff0000", 0.25), "rgba(255, 0, 0, 0.25)")


class Palettes(unittest.TestCase):
    def setUp(self):
        self.presets = build.load_palettes()

    def test_repository_palettes_are_valid(self):
        self.assertEqual(build.validate(self.presets), [])

    def test_repository_palettes_pass_contrast(self):
        build.check(self.presets, quiet=True)  # exits non-zero on failure

    def test_validation_catches_bad_input(self):
        bad = json.loads(json.dumps(self.presets))
        bad["teal"]["dark"]["h1"] = "red"
        del bad["teal"]["light"]["bold"]
        bad["teal"]["dark"]["shadow"] = "#000000"
        bad["Bad Name"] = bad["mono"]
        errors = " | ".join(build.validate(bad))
        for expected in ("teal.dark.h1", "teal.light.bold: missing", "teal.dark.shadow: unknown key", "Bad Name"):
            self.assertIn(expected, errors)

    def test_low_contrast_fails(self):
        dim = json.loads(json.dumps(self.presets))
        dim["mono"]["dark"]["h3"] = "#2a2a2a"
        with self.assertRaises(SystemExit):
            build.check(dim, quiet=True)


class GeneratedCss(unittest.TestCase):
    def test_committed_css_is_up_to_date(self):
        expected = build.render_css(build.load_palettes())
        actual = build.CSS_OUT.read_text(encoding="utf-8")
        self.assertEqual(actual, expected, "media/preview.css is stale: run python3 scripts/build.py css")

    def test_every_preset_has_dark_and_light_blocks(self):
        css = build.render_css(build.load_palettes())
        for name in build.load_palettes():
            for theme in build.THEMES:
                self.assertIn(
                    f'body.vscode-{theme}:not(.vscode-high-contrast):has(.mpp-preset[data-preset="{name}"])', css
                )

    def test_tables_have_grid_and_striped_rows(self):
        css = build.render_css(build.load_palettes())
        self.assertIn(f"{build.SCOPE} :is(th, td) {{", css)
        self.assertRegex(css, r":is\(th, td\) \{[^}]*border: 1px solid")
        self.assertIn(f"{build.SCOPE} tbody tr:nth-child(2n) {{ background-color:", css)

    def test_text_key_sets_body_colour_and_is_contrast_checked(self):
        presets = build.load_palettes()
        presets["mono"]["dark"]["text"] = "#123456"
        self.assertIn("  color: #123456;", build.preset_block("mono", "dark", presets["mono"]["dark"]))
        presets["mono"]["dark"]["text"] = "#2a2a2a"
        with self.assertRaises(SystemExit):
            build.check(presets, quiet=True)

    def test_code_box_and_link_underline_options(self):
        c = dict(build.load_palettes()["mono"]["dark"], codeTint="#ffffff", codeTintAlpha=0.05, codeBorderAlpha=0.1)
        c["linkUnderline"] = True
        block = build.preset_block("mono", "dark", c)
        self.assertIn("--mpp-code-bg: rgba(255, 255, 255, 0.05);", block)
        self.assertIn("--mpp-code-border: 0.5px solid rgba(255, 255, 255, 0.10);", block)
        self.assertIn("text-decoration: underline;", block)
        plain = build.preset_block("mono", "dark", build.load_palettes()["mono"]["dark"])
        self.assertNotIn("--mpp-code-border", plain)
        self.assertNotIn("text-decoration", plain)

    def test_external_only_link_underline(self):
        c = dict(build.load_palettes()["mono"]["dark"], linkUnderline="external")
        scope = 'body.vscode-dark:not(.vscode-high-contrast):has(.mpp-preset[data-preset="mono"])'
        block = build.preset_block("mono", "dark", c)
        # Web and mail links are underlined; any link is underlined on hover; other links are not otherwise
        self.assertIn(
            f'{scope} a:is([data-href^="http:" i], [data-href^="https:" i], [data-href^="mailto:" i]) {{', block
        )
        self.assertIn(f"{scope} a:hover {{", block)
        self.assertNotIn(f"{scope} a {{", block)
        every = build.preset_block("mono", "dark", dict(c, linkUnderline=True))
        self.assertIn(f"{scope} a {{", every)

    def test_option_types_are_validated(self):
        bad = build.load_palettes()
        bad["mono"]["dark"].update(codeTintAlpha=0, codeBorderAlpha="0.1", linkUnderline="yes")
        errors = " | ".join(build.validate(bad))
        for key in ("codeTintAlpha", "codeBorderAlpha", "linkUnderline"):
            self.assertIn(f"mono.dark.{key}", errors)

    def test_table_options(self):
        c = dict(
            build.load_palettes()["mono"]["dark"],
            tableBg="#1a1a19",
            tableHead="#ffffff",
            tableBorder="#ffffff",
            tableBorderAlpha=0.1,
            tableHeadBorder="#3e3e3e",
            tableRadius=11,
            tableHeadBg="#ffffff",
            tableHeadBgAlpha=0.05,
            tableHeadWeight=500,
        )
        block = build.preset_block("mono", "dark", c)
        for expected in (
            "--mpp-table-bg: #1a1a19;",
            "--mpp-table-head: #ffffff;",
            "--mpp-table-border: rgba(255, 255, 255, 0.10);",
            "--mpp-table-head-border: rgba(62, 62, 62, 1.00);",
            "border-collapse: separate;",
            "border-radius: 11px;",
            "thead :is(th, td) { background-color: rgba(255, 255, 255, 0.05); }",
            "th { font-weight: 500; }",
        ):
            self.assertIn(expected, block)
        plain = build.preset_block("mono", "dark", build.load_palettes()["mono"]["dark"])
        self.assertNotIn("--mpp-table", plain)
        self.assertNotIn("border-collapse", plain)

    def test_table_options_are_validated_and_contrast_checked(self):
        bad = build.load_palettes()
        bad["mono"]["dark"].update(tableRadius=0, tableBorderAlpha=2, tableBg="grey", tableHeadWeight=50)
        bad["mono"]["light"].update(tableRadius=True)
        errors = " | ".join(build.validate(bad))
        for key in (
            "dark.tableRadius",
            "dark.tableBorderAlpha",
            "dark.tableBg",
            "dark.tableHeadWeight",
            "light.tableRadius",
        ):
            self.assertIn(f"mono.{key}", errors)
        dim = build.load_palettes()
        dim["mono"]["dark"].update(tableBg="#d0d0d0")
        dim["mono"]["dark"]["tableHead"] = "#ffffff"
        with self.assertRaises(SystemExit):
            build.check(dim, quiet=True)

    def test_code_block_syntax_colours_are_never_changed(self):
        css = build.render_css(build.load_palettes())
        self.assertNotIn("hljs-", css)  # no syntax-token selectors
        # Only a preset's code-block box may be styled, and never its text colour
        for rule in re.findall(r"^([^{}\n]*\bpre\b[^{}\n]*)\{([^}]*)\}", css, re.M):
            selector, body = rule
            if ":not(pre) > code" in selector:
                continue
            self.assertIn("data-preset=", selector)
            self.assertNotRegex(body, r"(^|[\s;])color:")

    def test_ember_options(self):
        c = build.load_palettes()["ember"]["dark"]
        block = build.preset_block("ember", "dark", c)
        for expected in (
            "  font-weight: 600;",
            "  border-bottom: 1px solid #d4a27f;",
            "a:hover { text-decoration: none; border-bottom-width: 2px; }",
            "  border-radius: 6px;",
            "  padding: 2px 8px;",
            "  background-color: #0b0c0e;",
            "  border: 1px solid rgba(255, 255, 255, 0.10);",
            ":is(blockquote.mpp-alert-tip, .markdown-alert.markdown-alert-tip) { color: #86efac; "
            "background-color: rgba(22, 163, 74, 0.20); border-color: #14532d; }",
            ".markdown-alert.markdown-alert-warning) { color: #fde047;",
            "position: relative; padding-left: 48px;",
            "> .markdown-alert-title { position: absolute; top: 18px; left: 20px;",
            "> .markdown-alert-title svg { width: 18px; height: 18px;",
            ".mpp-alert-title-only) { display: none; }",
        ):
            self.assertIn(expected, block)
        plain = build.preset_block("mono", "dark", build.load_palettes()["mono"]["dark"])
        for absent in ("mpp-alert", "border-bottom:", " pre {", "font-weight"):
            self.assertNotIn(absent, plain)
        folio = build.preset_block("folio", "dark", build.load_palettes()["folio"]["dark"])
        for absent in ("border-bottom:", " pre {", "  font-weight:"):  # no link weight or code box
            self.assertNotIn(absent, folio)

    def test_folio_callouts(self):
        block = build.preset_block("folio", "dark", build.load_palettes()["folio"]["dark"])
        for expected in (
            ":is(blockquote.mpp-alert-note, .markdown-alert.markdown-alert-note) { color: #6da7ec; "
            "background-color: rgba(3, 32, 66, 1.00); border-color: #0d366b; }",
            "  border-radius: 11px;",
            "  padding: 10px 14px;",
            "position: relative; padding-left: 42px;",
            "> .markdown-alert-title { position: absolute; top: 11px; left: 14px;",
            "> .markdown-alert-title svg { width: 20px; height: 20px;",
            "a { text-decoration: underline; text-decoration-color: color-mix(in srgb, currentColor 65%, transparent);",
        ):
            self.assertIn(expected, block)
        bad = build.load_palettes()
        bad["folio"]["dark"].update(alertIcon=40, alertIconGap=0)
        errors = " | ".join(build.validate(bad))
        for key in ("alertIcon", "alertIconGap"):
            self.assertIn(f"folio.dark.{key}", errors)

    def test_ember_options_are_validated(self):
        bad = build.load_palettes()
        dark = bad["ember"]["dark"]
        dark.update(linkWeight=950, codePadding="2 8", preRadius=0, preBorder="white")
        dark["alerts"] = dict(dark["alerts"], tip={"text": "#86efac", "bg": "green"}, danger={})
        bad["ember"]["light"]["alerts"] = "blue"
        errors = " | ".join(build.validate(bad))
        for expected in (
            "ember.dark.linkWeight",
            "ember.dark.codePadding",
            "ember.dark.preRadius",
            "ember.dark.preBorder",
            "ember.dark.alerts.tip.bg",
            "ember.dark.alerts.tip.border: missing",
            "ember.dark.alerts.danger: unknown alert type",
            "ember.light.alerts: must be an object",
        ):
            self.assertIn(expected, errors)

    def test_alert_text_is_contrast_checked(self):
        dim = build.load_palettes()
        dim["ember"]["light"]["alerts"]["tip"]["text"] = "#e0f5e6"
        with self.assertRaises(SystemExit):
            build.check(dim, quiet=True)


class PresetNamesStayInSync(unittest.TestCase):
    """The preset list lives in three files; they must agree."""

    def test_names_match(self):
        palettes = set(build.load_palettes())
        pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        setting = pkg["contributes"]["configuration"]["properties"]["markdownPreviewPalettes.preset"]
        js = (ROOT / "extension.js").read_text(encoding="utf-8")
        js_names = set(re.findall(r"'([a-z]+)'", re.search(r"PRESETS = new Set\(\[(.*?)\]\)", js).group(1)))

        self.assertEqual(set(setting["enum"]), palettes | {"default"})
        self.assertEqual(js_names, palettes | {"default"})
        self.assertEqual(len(setting["enum"]), len(setting["enumDescriptions"]))
        self.assertIn(setting["default"], palettes)


if __name__ == "__main__":
    unittest.main()
