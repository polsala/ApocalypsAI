import unittest
import importlib.util
import pathlib
import datetime
from unittest.mock import patch


def load_module():
    """Load the emoji_clock module from the sibling src directory."""
    file_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "emoji_clock.py"
    spec = importlib.util.spec_from_file_location("emoji_clock", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestEmojiClock(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()
        cls.time_to_emoji = cls.mod.time_to_emoji
        cls.parse_time_string = cls.mod.parse_time_string

    def test_parse_time_string_valid(self):
        self.assertEqual(self.parse_time_string("09:07"), (9, 7))
        self.assertEqual(self.parse_time_string("23:59"), (23, 59))

    def test_parse_time_string_invalid(self):
        with self.assertRaises(ValueError):
            self.parse_time_string("9am")
        with self.assertRaises(ValueError):
            self.parse_time_string("24:00")

    def test_time_to_emoji_known(self):
        # 09:17 -> hour 🕘, minute rounded down to 15 -> 🕐
        self.assertEqual(self.time_to_emoji(9, 17), "🕘🕐")
        # 00:02 -> hour 🕛, minute 0 -> 🕛
        self.assertEqual(self.time_to_emoji(0, 2), "🕛🕛")
        # 14:44 -> hour 🕑 (14 → 2 pm), minute rounded down to 40 -> 🕘
        self.assertEqual(self.time_to_emoji(14, 44), "🕑🕘")

    @patch("datetime.datetime")
    def test_main_uses_current_time(self, mock_datetime):
        # Mock rationale: replace datetime.now with fixed value for deterministic test
        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 5, 23)
        # Reload module so it picks up the patched datetime
        mod = load_module()
        result = mod.time_to_emoji(5, 23)
        # 5:23 -> hour 🕔, minute rounded down to 20 -> 🕑
        self.assertEqual(result, "🕔🕑")


if __name__ == "__main__":
    unittest.main()
