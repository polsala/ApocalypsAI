import unittest
from unittest.mock import patch
import importlib.util
import pathlib

# Mock rationale: Ensure deterministic output by fixing random.choice result.

def load_module():
    """Dynamically load the cryptic_word module from the source directory."""
    file_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "cryptic_word.py"
    spec = importlib.util.spec_from_file_location("cryptic_word", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestCrypticWord(unittest.TestCase):
    @patch('random.choice')
    def test_get_random_word_returns_expected(self, mock_choice):
        # Mock rationale: Provide a known word entry.
        mock_choice.return_value = {"word": "ephemeral", "definition": "lasting for a very short time"}
        cryptic_word = load_module()
        result = cryptic_word.get_random_word()
        expected = {"word": "ephemeral", "definition": "lasting for a very short time"}
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
