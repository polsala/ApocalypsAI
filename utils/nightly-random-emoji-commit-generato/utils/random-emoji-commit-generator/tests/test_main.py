import unittest
from unittest.mock import patch
import sys
from pathlib import Path

# Mock rationale: Ensure deterministic output by fixing random choices.
# Adjust sys.path to import the module from src/
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from main import generate_message

class TestGenerateMessage(unittest.TestCase):
    @patch('random.sample')
    @patch('random.choice')
    def test_generate_message_deterministic(self, mock_choice, mock_sample):
        mock_sample.return_value = ["🚀", "✨"]
        mock_choice.return_value = "Add feature"
        result = generate_message(num_emojis=2)
        self.assertEqual(result, "🚀✨ Add feature")
        mock_sample.assert_called_once()
        mock_choice.assert_called_once()

    def test_invalid_num_emojis(self):
        with self.assertRaises(ValueError):
            generate_message(num_emojis=0)

if __name__ == '__main__':
    unittest.main()
