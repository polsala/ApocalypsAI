import json
import unittest
from pathlib import Path
from src.logger import load_entries, summarize_moods

# Mock rationale: All tests use in‑memory data or temporary files; no network calls.

class TestEmojiMoodLogger(unittest.TestCase):
    def test_load_entries_success(self):
        # Prepare a temporary JSON file
        data = [
            {"date": "2025-11-01", "mood": 4},
            {"date": "2025-11-01", "mood": 3},
            {"date": "2025-11-02", "mood": 5},
        ]
        tmp = Path("tmp_moods.json")
        tmp.write_text(json.dumps(data), encoding="utf-8")
        try:
            loaded = load_entries(tmp)
            self.assertEqual(loaded, data)
        finally:
            tmp.unlink()

    def test_load_entries_invalid_structure(self):
        tmp = Path("bad.json")
        tmp.write_text(json.dumps({"not": "a list"}), encoding="utf-8")
        try:
            with self.assertRaises(ValueError):
                load_entries(tmp)
        finally:
            tmp.unlink()

    def test_summarize_moods(self):
        entries = [
            {"date": "2025-11-01", "mood": 4},
            {"date": "2025-11-01", "mood": 3},
            {"date": "2025-11-02", "mood": 5},
            {"date": "2025-11-02", "mood": 5},
        ]
        expected = "2025-11-01: 🙂\n2025-11-02: 😄"
        self.assertEqual(summarize_moods(entries), expected)

    def test_emoji_boundaries(self):
        # Directly test the private mapping via summarize_moods edge cases
        cases = [
            (1, "😢"),
            (2, "🙁"),
            (3, "😐"),
            (4, "🙂"),
            (5, "😄"),
        ]
        for mood, emoji in cases:
            with self.subTest(mood=mood):
                entries = [{"date": "2025-11-03", "mood": mood}]
                self.assertEqual(summarize_moods(entries), f"2025-11-03: {emoji}")

if __name__ == "__main__":
    unittest.main()
