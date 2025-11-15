import unittest
import sys
import pathlib
from unittest.mock import patch

# Adjust import path to locate the src module
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from compliment import get_compliment, _COMPLIMENTS

class TestComplimentGenerator(unittest.TestCase):
    def test_general_category(self):
        """# Mock rationale: force deterministic output by mocking random.choice"""
        with patch('random.choice', lambda seq: seq[0]):
            compliment = get_compliment('general')
            self.assertEqual(compliment, _COMPLIMENTS['general'][0])

    def test_unknown_category_falls_back(self):
        """# Mock rationale: ensure fallback to full pool works deterministically"""
        with patch('random.choice', lambda seq: seq[0]):
            compliment = get_compliment('unknown')
            all_compliments = [c for lst in _COMPLIMENTS.values() for c in lst]
            self.assertEqual(compliment, all_compliments[0])

    def test_no_category(self):
        """# Mock rationale: test deterministic selection from the full pool"""
        with patch('random.choice', lambda seq: seq[-1]):
            compliment = get_compliment()
            all_compliments = [c for lst in _COMPLIMENTS.values() for c in lst]
            self.assertEqual(compliment, all_compliments[-1])

if __name__ == '__main__':
    unittest.main()
