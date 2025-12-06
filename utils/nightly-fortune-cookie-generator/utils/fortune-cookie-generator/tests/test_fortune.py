import unittest
import sys
import os
from unittest.mock import patch

# Ensure src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fortune import get_fortune

class TestFortuneGenerator(unittest.TestCase):
    def test_random_fortune_deterministic(self):
        # Mock random.choice to always return the first element
        with patch("random.choice") as mock_choice:
            mock_choice.side_effect = lambda seq: seq[0]  # # Mock rationale: ensure deterministic output
            result = get_fortune()
            self.assertEqual(result, "You will find great success in unexpected places.")

    def test_category_filter(self):
        with patch("random.choice") as mock_choice:
            mock_choice.side_effect = lambda seq: seq[0]  # # Mock rationale: deterministic first match
            result = get_fortune("humor")
            # First humor fortune in the list
            self.assertEqual(result, "Never trust a computer you can't throw out a window.")

    def test_invalid_category(self):
        with self.assertRaises(ValueError) as cm:
            get_fortune("nonexistent")
        self.assertIn("No fortunes found for category", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
