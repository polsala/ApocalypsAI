import unittest
from unittest import mock

# Import the module under test
from src.compliment import get_compliment, _COMPLIMENTS, _DEFAULT_CATEGORY

class TestComplimentGenerator(unittest.TestCase):
    def test_default_category_when_none_provided(self):
        # Mock random.choice to return the first element of the list
        with mock.patch('random.choice', side_effect=lambda seq: seq[0]) as mock_choice:
            result = get_compliment()
            self.assertEqual(result, _COMPLIMENTS[_DEFAULT_CATEGORY][0])
            mock_choice.assert_called_once()

    def test_specific_known_category(self):
        with mock.patch('random.choice', side_effect=lambda seq: seq[-1]) as mock_choice:
            result = get_compliment('code')
            self.assertEqual(result, _COMPLIMENTS['code'][-1])
            mock_choice.assert_called_once()

    def test_unknown_category_falls_back_to_default(self):
        with mock.patch('random.choice', side_effect=lambda seq: seq[1]) as mock_choice:
            result = get_compliment('nonexistent')
            self.assertEqual(result, _COMPLIMENTS[_DEFAULT_CATEGORY][1])
            mock_choice.assert_called_once()

    def test_category_case_sensitivity(self):
        # The implementation is case‑sensitive; ensure it falls back correctly.
        with mock.patch('random.choice', side_effect=lambda seq: seq[0]) as mock_choice:
            result = get_compliment('CODE')  # Uppercase should not match
            self.assertEqual(result, _COMPLIMENTS[_DEFAULT_CATEGORY][0])
            mock_choice.assert_called_once()

# Mock rationale: All tests replace `random.choice` with a deterministic lambda so
# they never depend on actual randomness or external state. This keeps the suite
# fully offline and repeatable.

if __name__ == '__main__':
    unittest.main()
