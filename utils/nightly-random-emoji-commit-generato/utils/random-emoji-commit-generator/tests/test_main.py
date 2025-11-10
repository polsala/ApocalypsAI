import os
import sys
import subprocess
import unittest
from unittest.mock import patch

# Add the src directory to sys.path so we can import the module under test
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, src_path)

from main import generate_message

class TestEmojiCommitGenerator(unittest.TestCase):
    @patch('random.choice', return_value='🚀')
    def test_generate_message(self, mock_choice):
        # Mock rationale: deterministic emoji selection for repeatable test
        self.assertEqual(generate_message("Add new feature"), "🚀 Add new feature")
        mock_choice.assert_called_once()

    @patch('random.choice', return_value='🚀')
    def test_cli_output(self, mock_choice):
        # Mock rationale: deterministic CLI output without external randomness
        script = os.path.join(src_path, 'main.py')
        result = subprocess.run([sys.executable, script, "Improve docs"], capture_output=True, text=True)
        self.assertEqual(result.stdout.strip(), "🚀 Improve docs")
        self.assertEqual(result.returncode, 0)

if __name__ == "__main__":
    unittest.main()
