import unittest
from utils.nightly-emoji-mood-analyzer.src.analyzer import analyze_mood

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_positive_sentence(self):
        # Mock rationale: deterministic mapping based on keyword list.
        self.assertEqual(analyze_mood("I love this wonderful day!"), "😄")

    def test_negative_sentence(self):
        # Mock rationale: deterministic mapping based on keyword list.
        self.assertEqual(analyze_mood("I feel sad and gloomy today."), "😔")

    def test_neutral_sentence(self):
        # Mock rationale: no positive or negative keywords → neutral.
        self.assertEqual(analyze_mood("The sky is blue."), "😐")

    def test_mixed_sentence_more_positive(self):
        # Mock rationale: more positive keywords than negative.
        self.assertEqual(analyze_mood("I am happy but a bit sad"), "😄")

    def test_mixed_sentence_more_negative(self):
        # Mock rationale: more negative keywords than positive.
        self.assertEqual(analyze_mood("I hate the terrible weather"), "😔")

if __name__ == "__main__":
    unittest.main()
