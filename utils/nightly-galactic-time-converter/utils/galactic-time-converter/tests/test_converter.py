import unittest
import sys
import pathlib

# Add the src directory of this utility to ``sys.path`` so we can import ``converter``
utils_root = pathlib.Path(__file__).resolve().parents[2]
src_path = utils_root / "src"
sys.path.append(str(src_path))

from converter import unix_to_galactic, galactic_to_unix

class TestGalacticConverter(unittest.TestCase):
    def test_unix_to_galactic(self):
        # 2021‑01‑01 00:00:00 UTC = 1609459200
        # After adding the 1,000,000‑second offset we get 2021‑01‑12 13:46:40 UTC
        self.assertEqual(unix_to_galactic(1609459200), "GT-20210112-134640")

    def test_galactic_to_unix(self):
        self.assertEqual(galactic_to_unix("GT-20210112-134640"), 1609459200)

    def test_invalid_galactic_format(self):
        with self.assertRaises(ValueError):
            galactic_to_unix("INVALID-STRING")

    def test_negative_unix_timestamp(self):
        with self.assertRaises(ValueError):
            unix_to_galactic(-1)

if __name__ == "__main__":
    unittest.main()
