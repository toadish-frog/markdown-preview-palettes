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

    def test_code_blocks_are_not_styled(self):
        css = build.render_css(build.load_palettes())
        self.assertNotRegex(css, r"(^|\s)pre(\s|>|\{)")  # only ':not(pre) > code' may mention pre


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
