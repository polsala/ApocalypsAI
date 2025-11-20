import json
import unittest
from unittest.mock import mock_open, patch

# Import the class from the utility package
from emoji_mood_tracker.src.mood_tracker import MoodTracker


class TestMoodTracker(unittest.TestCase):
    def test_add_creates_file(self):
        # Mock rationale: ensure that writing to the file stores the correct JSON structure
        m = mock_open()
        with patch("os.path.exists", return_value=False), \
             patch("builtins.open", m):
            tracker = MoodTracker(path="dummy.json")
            tracker.add("2023-01-01", "😊")
            m.assert_called_with("dummy.json", "w", encoding="utf-8")
            handle = m()
            written = "".join(call.args[0] for call in handle.write.call_args_list)
            self.assertIn('"2023-01-01": "😊"', written)

    def test_stats_computation(self):
        # Mock rationale: provide pre‑loaded JSON data and verify stats calculation
        data = {"2023-01-01": "😊", "2023-01-02": "😢", "2023-01-03": "😊"}
        m = mock_open(read_data=json.dumps(data))
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", m):
            tracker = MoodTracker(path="dummy.json")
            stats = tracker.stats()
            self.assertEqual(stats["total"], 3)
            self.assertEqual(stats["most_common"], "😊")
            self.assertEqual(stats["entries"][0], ("2023-01-01", "😊"))


if __name__ == "__main__":
    unittest.main()
