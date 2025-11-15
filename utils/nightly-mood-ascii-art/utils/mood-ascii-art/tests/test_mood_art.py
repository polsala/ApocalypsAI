import unittest
from src.mood_art import get_art, MOOD_ART


class TestMoodArt(unittest.TestCase):
    def test_known_moods(self):
        """Ensure each supported mood returns its specific ASCII art."""
        for mood in ["happy", "sad", "angry", "surprised", "neutral"]:
            with self.subTest(mood=mood):
                art = get_art(mood)
                self.assertEqual(art, MOOD_ART[mood])

    def test_case_insensitivity(self):
        """Mood lookup should be case‑insensitive and trim whitespace."""
        self.assertEqual(get_art("  HaPpY  "), MOOD_ART["happy"])
        self.assertEqual(get_art("SAD"), MOOD_ART["sad"])

    def test_unknown_mood_fallback(self):
        """Unknown moods should return the default art.
        # Mock rationale: No external calls; deterministic fallback.
        """
        self.assertEqual(get_art("confused"), MOOD_ART["default"])
        self.assertEqual(get_art(""), MOOD_ART["default"])


if __name__ == "__main__":
    unittest.main()
