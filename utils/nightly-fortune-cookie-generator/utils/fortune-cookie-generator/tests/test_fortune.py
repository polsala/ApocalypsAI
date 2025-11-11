import unittest
from unittest.mock import patch
import sys
from pathlib import Path

# Ensure the src directory is on sys.path for import
src_path = Path(__file__).resolve().parents[2] / "src"
sys.path.append(str(src_path))

from fortune import get_fortune, _FORTUNES

class TestFortuneCookieGenerator(unittest.TestCase):
    def test_get_fortune_returns_string(self):
        # Mock rationale: deterministic choice for test
        with patch('random.choice', return_value=_FORTUNES[0]) as mock_choice:
            result = get_fortune()
            mock_choice.assert_called_once_with(_FORTUNES)
            self.assertEqual(result, _FORTUNES[0])

    def test_fortune_list_is_non_empty(self):
        self.assertTrue(len(_FORTUNES) > 0)

if __name__ == "__main__":
    unittest.main()
