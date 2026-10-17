"""Reject incomplete or inconsistent template releases."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate import png_dimensions, validate

ROOT = Path(__file__).resolve().parents[1]


class AssetIntegrityTest(unittest.TestCase):
    def test_truncated_png_is_rejected(self):
        data = (ROOT / "skills/logic-render/assets/layered-01.png").read_bytes()
        with self.assertRaises(ValueError):
            png_dimensions(data[:-8])

    def test_manifest_disagrees_with_image_and_panel_guide(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
            shutil.copy2(ROOT / "LICENSE", root / "LICENSE")
            manifest_path = root / "skills/logic-render/assets/manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            entry = manifest["assets"][0]
            entry["sha256"] = "0" * 64
            entry["width"] += 1
            entry["panels"][0]["title"] = "Wrong panel"
            entry["panels"][0]["column"] = 2
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            errors = "\n".join(validate(root))
            for expected in ("hash mismatch", "dimensions differ", "panel title/index", "panel positions"):
                self.assertIn(expected, errors)

    def test_unlisted_asset_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
            shutil.copy2(ROOT / "LICENSE", root / "LICENSE")
            (root / "skills/logic-render/assets/unlisted.svg").write_text("<svg/>", encoding="utf-8")
            self.assertTrue(any("asset inventory differs" in error for error in validate(root)))


if __name__ == "__main__":
    unittest.main()
