import os
import json
import tempfile
import unittest
from pathlib import Path
from typing import List

# Import the module under test. Adjust sys.path so the relative import works.
import sys
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from main import log_mood, get_summary, _save_data, _load_data, _storage_path

class TestDailyEmojiMoodTracker(unittest.TestCase):
    def setUp(self) -> None:
        # Create a temporary file to act as our JSON storage.
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = Path(self.temp_dir.name) / "mood.json"
        # Point the utility to the temporary file via env var.
        os.environ["DAILY_EMOJI_MOOD_PATH"] = str(self.temp_file)
        # Ensure a clean start.
        if self.temp_file.exists():
            self.temp_file.unlink()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()
        os.environ.pop("DAILY_EMOJI_MOOD_PATH", None)

    def test_log_and_load_single_entry(self):
        # Mock rationale: deterministic test – we control the storage path.
        log_mood("😀", "Happy day")
        # Verify file exists and contains exactly one entry.
        self.assertTrue(self.temp_file.is_file())
        with self.temp_file.open("r", encoding="utf-8") as f:
            data: List[dict] = json.load(f)
        self.assertEqual(len(data), 1)
        entry = data[0]
        self.assertEqual(entry["emoji"], "😀")
        self.assertEqual(entry["note"], "Happy day")
        self.assertIn("timestamp", entry)

    def test_summary_returns_correct_number_of_entries(self):
        # Log three entries.
        log_mood("😴", "Too early")
        log_mood("🤔", "Thinking")
        log_mood("🥳", "Celebration")
        # Request last 2 entries.
        recent = get_summary(last=2)
        self.assertEqual(len(recent), 2)
        # The most recent should be the last logged (🥳).
        self.assertEqual(recent[0]["emoji"], "🥳")
        self.assertEqual(recent[1]["emoji"], "🤔")

    def test_load_from_nonexistent_file_returns_empty_list(self):
        # Ensure the storage file does not exist.
        if self.temp_file.is_file():
            self.temp_file.unlink()
        data = _load_data()
        self.assertEqual(data, [])

    def test_save_and_load_roundtrip(self):
        entries = [
            {"timestamp": "2025-01-01T00:00:00Z", "emoji": "🌞", "note": "Sunrise"},
            {"timestamp": "2025-01-02T00:00:00Z", "emoji": "🌧️", "note": "Rainy"},
        ]
        _save_data(entries)
        loaded = _load_data()
        self.assertEqual(loaded, entries)

    def test_log_mood_without_emoji_raises(self):
        with self.assertRaises(ValueError):
            log_mood("", "No emoji")

if __name__ == "__main__":
    unittest.main()
