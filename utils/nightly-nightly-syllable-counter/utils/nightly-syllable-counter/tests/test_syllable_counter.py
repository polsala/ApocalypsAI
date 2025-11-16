import unittest
from src.syllable_counter import count_syllables

class TestSyllableCounter(unittest.TestCase):
    def test_basic_words(self):
        cases = {
            "hello": 2,
            "world": 1,
            "beautiful": 3,
            "queue": 1,
            "rhythms": 1,
            "the": 1,
            "syllable": 3,
            "python": 2,
            "algorithm": 4,
            "e": 1,  # single vowel still counts as one syllable
        }
        for word, expected in cases.items():
            with self.subTest(word=word):
                self.assertEqual(count_syllables(word), expected)

    def test_punctuation_and_numbers(self):
        # Mock rationale: ensure non‑alphabetic characters are ignored.
        self.assertEqual(count_syllables("hello!"), 2)
        self.assertEqual(count_syllables("123abc"), 2)  # "abc" -> 1 vowel group, but "a" counts as 1
        self.assertEqual(count_syllables("co-op"), 2)   # "co" and "op" each have a vowel group

    def test_empty_and_nonalpha(self):
        self.assertEqual(count_syllables(""), 0)
        self.assertEqual(count_syllables("---"), 0)

if __name__ == "__main__":
    unittest.main()
