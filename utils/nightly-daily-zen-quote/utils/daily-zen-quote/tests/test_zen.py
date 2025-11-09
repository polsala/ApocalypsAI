import unittest
from unittest.mock import patch

# Import the module under test
from src.zen import get_random_quote, filter_by_max_length, QUOTES


class TestZenUtility(unittest.TestCase):
    def test_get_random_quote_returns_tuple(self):
        """Ensure the function returns a (quote, author) tuple of strings."""
        quote, author = get_random_quote()
        self.assertIsInstance(quote, str)
        self.assertIsInstance(author, str)
        self.assertIn((quote, author), QUOTES)

    def test_get_random_quote_deterministic_with_seed(self):
        """Deterministic output when a seed is supplied.

        # Mock rationale: we rely on Python's deterministic PRNG; using a fixed
        # seed guarantees the same choice across runs, making the test offline.
        """
        quote1, author1 = get_random_quote(seed=12345)
        quote2, author2 = get_random_quote(seed=12345)
        self.assertEqual((quote1, author1), (quote2, author2))

    def test_filter_by_max_length_respects_constraint(self):
        """Only quotes whose length <= max_len are considered.

        # Mock rationale: we construct a max_len that excludes at least one entry
        # and verify the returned quote satisfies the condition.
        """
        max_len = 50  # Short enough to filter out longer quotes
        quote, author = filter_by_max_length(max_len, seed=0)
        self.assertLessEqual(len(quote), max_len)
        self.assertIn((quote, author), QUOTES)

    def test_filter_by_max_length_no_match_raises(self):
        """When no quote fits the length, a ValueError is raised.

        # Mock rationale: we set max_len to 1, which no quote can satisfy.
        """
        with self.assertRaises(ValueError):
            filter_by_max_length(1)

    @patch('random.choice')
    def test_get_random_quote_uses_random_choice(self, mock_choice):
        """Patch ``random.choice`` to ensure the function delegates correctly.

        # Mock rationale: by mocking ``random.choice`` we avoid any randomness and
        # can assert the exact interaction contract.
        """
        mock_choice.return_value = ("Mocked quote", "Mocked author")
        quote, author = get_random_quote()
        mock_choice.assert_called_once_with(QUOTES)
        self.assertEqual(quote, "Mocked quote")
        self.assertEqual(author, "Mocked author")

    @patch('random.choice')
    def test_filter_by_max_length_uses_random_choice(self, mock_choice):
        """Patch ``random.choice`` for the filtered path.

        # Mock rationale: ensures the filtered list is passed to ``random.choice``.
        """
        mock_choice.return_value = ("Short quote", "Author")
        max_len = 100
        quote, author = filter_by_max_length(max_len)
        # Build expected filtered list manually
        expected_filtered = [(q, a) for q, a in QUOTES if len(q) <= max_len]
        mock_choice.assert_called_once_with(expected_filtered)
        self.assertEqual((quote, author), ("Short quote", "Author"))


if __name__ == "__main__":
    unittest.main()
