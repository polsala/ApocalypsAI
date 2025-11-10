import unittest
from src.wordle_helper import filter_words

class TestWordleHelper(unittest.TestCase):
    def test_exact_match(self):
        # Pattern fully specified, no exclusions
        self.assertEqual(filter_words('apple', ''), ['apple'])

    def test_partial_pattern(self):
        # Known letters: a _ _ l e -> should match 'apple' only
        self.assertEqual(filter_words('a??le', ''), ['apple'])
        self.assertEqual(filter_words('a__le', ''), ['apple'])

    def test_excluded_letters(self):
        # Exclude any word containing 'x', 'y', or 'z'
        result = filter_words('?????', 'xyz')
        # All words in WORD_LIST except 'xenon', 'yacht', 'zebra'
        self.assertNotIn('xenon', result)
        self.assertNotIn('yacht', result)
        self.assertNotIn('zebra', result)
        # Ensure a known word still appears
        self.assertIn('apple', result)

    def test_complex_constraints(self):
        # Pattern: ??r?? (r in third position), exclude vowels
        result = filter_words('??r??', 'aeiou')
        # From the static list, only 'crane' and 'grape' contain vowels, so they are filtered out.
        # 'crane' has r in third position but contains 'a' and 'e' -> excluded.
        # 'grape' also contains vowels.
        # 'joker' has r in fourth position, not third.
        # 'knock' has no r.
        # 'tiger' has r in fifth.
        # The only candidate left with r third and no vowels is 'crane' (excluded) -> expect empty list.
        self.assertEqual(result, [])

    def test_invalid_pattern_length(self):
        with self.assertRaises(ValueError):
            filter_words('too-long', '')
        with self.assertRaises(ValueError):
            filter_words('short', '')

if __name__ == '__main__':
    unittest.main()
