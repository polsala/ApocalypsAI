import unittest
from utils.emoji-mood-analyzer.src.emoji_mood import analyze_mood

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_happy_sentence(self):
        text = "I love this wonderful, fantastic day!"
        self.assertEqual(analyze_mood(text), "😊")

    def test_sad_sentence(self):
        text = "I hate this terrible, awful situation."
        self.assertEqual(analyze_mood(text), "😞")

    def test_neutral_sentence(self):
        text = "The sky is blue and the grass is green."
        self.assertEqual(analyze_mood(text), "😐")

    def test_mixed_sentence_more_positive(self):
        text = "I love the food but hate the service."
        # Positive: love (1), Negative: hate (1) → score 0 → neutral
        self.assertEqual(analyze_mood(text), "😐")

    def test_mixed_sentence_more_negative(self):
        text = "The movie was good but the ending was terrible and awful."
        # Positive: good (1), Negative: terrible, awful (2) → score -1 → sad
        self.assertEqual(analyze_mood(text), "😞")

    def test_case_insensitivity(self):
        text = "I LoVe this!"
        self.assertEqual(analyze_mood(text), "😊")

    def test_punctuation_handling(self):
        text = "Wow... great!"
        self.assertEqual(analyze_mood(text), "😊")

if __name__ == "__main__":
    unittest.main()
