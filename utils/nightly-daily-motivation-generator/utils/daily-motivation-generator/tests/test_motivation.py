import unittest
from unittest.mock import patch
from src.motivation import get_motivation


class TestMotivation(unittest.TestCase):
    def test_get_motivation_returns_expected_format(self):
        # Mock random.choice to return a known quote
        with patch('src.motivation.random.choice') as mock_choice:
            mock_choice.return_value = ("Test quote", "Test Author")
            result = get_motivation()
            self.assertEqual(result, "Test quote — Test Author")
            # Ensure random.choice was called exactly once
            mock_choice.assert_called_once()

    def test_get_motivation_ignores_category(self):
        with patch('src.motivation.random.choice') as mock_choice:
            mock_choice.return_value = ("Another quote", "Another Author")
            result = get_motivation(category="any")
            self.assertEqual(result, "Another quote — Another Author")
            mock_choice.assert_called_once()


if __name__ == "__main__":
    unittest.main()
