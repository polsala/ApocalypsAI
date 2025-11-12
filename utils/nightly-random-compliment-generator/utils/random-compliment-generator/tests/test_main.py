import sys
import pathlib
# Add the src directory to sys.path so we can import main directly.
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import unittest
from unittest import mock

from main import get_compliment

class TestRandomComplimentGenerator(unittest.TestCase):
    def test_deterministic_with_seed(self):
        """With a fixed seed, the output should be reproducible."""
        first = get_compliment(seed=123)
        second = get_compliment(seed=123)
        self.assertEqual(first, second)

    @mock.patch("random.choice")
    def test_random_choice_called(self, mock_choice):
        """Mock rationale: ensure random.choice is used to select compliment."""
        mock_choice.return_value = "Mocked compliment"
        result = get_compliment()
        mock_choice.assert_called_once()
        self.assertEqual(result, "Mocked compliment")

if __name__ == "__main__":
    unittest.main()
