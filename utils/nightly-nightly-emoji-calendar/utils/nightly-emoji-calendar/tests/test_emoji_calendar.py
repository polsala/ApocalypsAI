import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we patch datetime.date.today to a fixed date so the CLI output is deterministic.
from utils.nightly-emoji-calendar.src.emoji_calendar import (
    get_emoji_for_date,
    build_month_grid,
    render_grid,
)

class TestEmojiCalendar(unittest.TestCase):
    def test_get_emoji_for_date(self):
        # Monday
        self.assertEqual(get_emoji_for_date(datetime.date(2025, 1, 6)), "🌞")
        # Wednesday
        self.assertEqual(get_emoji_for_date(datetime.date(2025, 1, 8)), "🌟")
        # Sunday
        self.assertEqual(get_emoji_for_date(datetime.date(2025, 1, 12)), "🍳")

    @patch("datetime.date")
    def test_build_month_grid_february_non_leap(self, mock_date):
        # Mock today to Feb 2023 (non‑leap year) – the function does not use today directly,
        # but we keep the patch to illustrate offline deterministic testing.
        mock_date.today.return_value = datetime.date(2023, 2, 1)
        weeks = build_month_grid(2023, 2)
        # February 2023 starts on Wednesday (weekday 2) and has 28 days.
        # Verify first week length and first day emoji.
        self.assertEqual(len(weeks), 5)  # 5 weeks displayed
        first_week = weeks[0]
        # Monday and Tuesday are padding (None)
        self.assertIsNone(first_week[0])
        self.assertIsNone(first_week[1])
        # Wednesday Feb 1 -> 🌟
        self.assertEqual(first_week[2], "🌟")
        # Verify last day (Feb 28, 2023) is a Tuesday -> 🌜
        last_week = weeks[-1]
        self.assertEqual(last_week[1], "🌜")

    def test_render_grid(self):
        weeks = [
            ["🌞", "🌜", "🌟", "🌈", "🎉", "🛌", "🍳"],
            ["🌞", "🌜", "🌟", "🌈", "🎉", "🛌", "🍳"],
        ]
        rendered = render_grid(weeks)
        expected = "🌞 🌜 🌟 🌈 🎉 🛌 🍳\n🌞 🌜 🌟 🌈 🎉 🛌 🍳"
        self.assertEqual(rendered, expected)

if __name__ == "__main__":
    unittest.main()
