import unittest
from unittest.mock import patch

# Import the function from the sibling src package.
from src.zen_quote import get_random_quote


class TestZenQuote(unittest.TestCase):
    def test_random_quote_no_theme(self):
        # Mock rationale: ensure deterministic output by mocking random.choice
        with patch('random.choice', return_value="Mocked Quote"):
            self.assertEqual(get_random_quote(), "Mocked Quote")

    def test_random_quote_with_theme(self):
        # Mock rationale: deterministic selection from the filtered list
        with patch('random.choice', return_value="The journey of a thousand miles begins with one step."):
            self.assertEqual(get_random_quote(theme="motivation"), "The journey of a thousand miles begins with one step.")

    def test_invalid_theme_raises(self):
        with self.assertRaises(ValueError):
            get_random_quote(theme="nonexistent")


if __name__ == "__main__":
    unittest.main()
