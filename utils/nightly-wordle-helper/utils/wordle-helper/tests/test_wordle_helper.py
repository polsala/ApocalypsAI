import unittest
from src.wordle_helper import filter_words

class TestWordleHelper(unittest.TestCase):
    def test_green_and_black(self):
        # Guess: apple, Pattern: ggggb (first four letters green, last black)
        wordlist = ["apple", "apply", "ample"]
        result = filter_words("apple", "ggggb", wordlist)
        self.assertEqual(result, ["apply"])

    def test_all_green(self):
        wordlist = ["crane", "slate", "flame"]
        result = filter_words("crane", "ggggg", wordlist)
        self.assertEqual(result, ["crane"])

    def test_invalid_length(self):
        wordlist = ["apple"]
        with self.assertRaises(ValueError):
            filter_words("app", "ggg", wordlist)

if __name__ == "__main__":
    unittest.main()
