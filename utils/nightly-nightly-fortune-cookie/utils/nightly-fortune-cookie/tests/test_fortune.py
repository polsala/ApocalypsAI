import unittest
from unittest.mock import patch

# Mock rationale: we patch ``random.choice`` to return a known value so the test
# does not depend on randomness or external state.

from src.fortune import get_fortune, FORTUNES

class TestFortuneCookie(unittest.TestCase):
    def test_get_fortune_returns_expected_when_mocked(self):
        expected = FORTUNES[0]
        with patch('random.choice', return_value=expected) as mock_choice:
            result = get_fortune()
            mock_choice.assert_called_once_with(FORTUNES)
            self.assertEqual(result, expected)

    def test_fortunes_list_is_non_empty(self):
        self.assertTrue(len(FORTUNES) > 0, "FORTUNES list should contain at least one message")

if __name__ == "__main__":
    unittest.main()
