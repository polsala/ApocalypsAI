import os
import sys
import unittest

# Add the src directory to sys.path so we can import the parser module.
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..', 'src'))
sys.path.append(SRC_DIR)

from parser import parse_duration  # type: ignore


class TestParseDuration(unittest.TestCase):
    def test_seconds_only(self):
        self.assertEqual(parse_duration('45s'), 45)

    def test_minutes_and_seconds(self):
        self.assertEqual(parse_duration('2m30s'), 150)

    def test_hours_and_minutes_with_space(self):
        self.assertEqual(parse_duration('1h 15m'), 4500)

    def test_full_combination(self):
        # 1 day = 86400, 2h = 7200, 3m = 180, 4s = 4 => total 93784
        self.assertEqual(parse_duration('1d2h3m4s'), 93784)

    def test_mixed_case_and_extra_spaces(self):
        # 3d = 259200, 4h = 14400, 5m = 300, 6s = 6 => total 273906
        self.assertEqual(parse_duration(' 3D 4h 5M 6s '), 273906)

    def test_invalid_fragments_are_ignored(self):
        # "abc" and "5x" are ignored; only "10m" counts (600 seconds)
        self.assertEqual(parse_duration('abc 5x 10m'), 600)

    def test_no_valid_units(self):
        self.assertEqual(parse_duration('nothing here'), 0)


if __name__ == '__main__':
    unittest.main()
