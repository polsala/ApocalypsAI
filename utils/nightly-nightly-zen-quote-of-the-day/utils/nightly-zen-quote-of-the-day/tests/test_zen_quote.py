import unittest
from unittest.mock import patch
import sys
from pathlib import Path

# Add the src directory to sys.path so we can import zen_quote
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from zen_quote import get_quote


class TestZenQuote(unittest.TestCase):
    def test_get_quote_deterministic(self):
        # Mock random.choice to return a known quote
        with patch('random.choice', return_value="The journey of a thousand miles begins with one step.") as mock_choice:
            quote = get_quote()
            mock_choice.assert_called_once()
            self.assertEqual(quote, "The journey of a thousand miles begins with one step.")  # Mock rationale: deterministic test


if __name__ == "__main__":
    unittest.main()
