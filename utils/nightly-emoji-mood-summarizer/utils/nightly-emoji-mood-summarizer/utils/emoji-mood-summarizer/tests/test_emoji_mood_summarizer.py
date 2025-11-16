import unittest
from emoji_mood_summarizer import summarize_moods

class TestEmojiMoodSummarizer(unittest.TestCase):
    def test_basic_happy(self):
        self.assertEqual(summarize_moods(["happy", "sad", "happy"]), "😊")

    def test_basic_sad(self):
        self.assertEqual(summarize_moods(["sad", "sad", "happy"]), "😢")

    def test_tie_resolves_by_order(self):
        # happy and angry both appear twice; happy wins due to order precedence
        self.assertEqual(summarize_moods(["happy", "angry", "happy", "angry"]), "😊")

    def test_unknown_mood_fallback(self):
        self.assertEqual(summarize_moods(["confused", "confused"]), "🤔")

    def test_empty_input(self):
        self.assertEqual(summarize_moods([]), "🤔")

    def test_normalization(self):
        # Mock rationale: ensure whitespace and case are ignored
        self.assertEqual(summarize_moods(["  Happy ", "HAPPY", "happy"]), "😊")

if __name__ == "__main__":
    unittest.main()
