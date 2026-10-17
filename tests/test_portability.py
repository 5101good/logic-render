"""Validate UTF-8 package files independently of the system text encoding."""

import io
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.validate import validate

ROOT = Path(__file__).resolve().parents[1]


class EncodingPortabilityTest(unittest.TestCase):
    def test_chinese_package_validates_under_legacy_default_encoding(self):
        original = io.text_encoding

        def legacy_default(encoding, stacklevel=2):
            return original(encoding or "cp1252", stacklevel)

        with patch("io.text_encoding", side_effect=legacy_default):
            self.assertEqual(validate(ROOT), [])


if __name__ == "__main__":
    unittest.main()
