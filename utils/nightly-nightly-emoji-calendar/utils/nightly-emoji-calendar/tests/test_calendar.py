import unittest
import importlib.util
import pathlib

# Load the utility module without polluting the import namespace
module_path = pathlib.Path(__file__).parents[1] / "src" / "calendar.py"
spec = importlib.util.spec_from_file_location("emoji_calendar", module_path)
emoji_calendar = importlib.util.module_from_spec(spec)
# Mock rationale: loading the generated module directly ensures tests run offline and deterministically.
spec.loader.exec_module(emoji_calendar)

render_month = emoji_calendar.render_month

class TestEmojiCalendar(unittest.TestCase):
    def test_march_2023(self):
        output = render_month(2023, 3)
        lines = output.splitlines()
        # Header must be present
        self.assertEqual(lines[0], "Mo Tu We Th Fr Sa Su")
        # March 2023 has 4 Saturdays and 4 Sundays
        self.assertEqual(output.count("🌞"), 4)  # Saturdays
        self.assertEqual(output.count("🌜"), 4)  # Sundays
        # Day 1 (Wednesday) should appear as " 1"
        self.assertIn(" 1", output)

if __name__ == "__main__":
    unittest.main()
