import unittest
from unittest.mock import patch
import sys
import io
from src.fortune_teller import get_fortune, FORTUNES, main

class TestFortuneTeller(unittest.TestCase):

    def test_get_fortune_returns_string(self):
        """
        Test that get_fortune always returns a string.
        """
        fortune = get_fortune()
        self.assertIsInstance(fortune, str)
        self.assertGreater(len(fortune), 0)

    @patch('random.choice')
    def test_get_fortune_selects_from_fortunes_list(self, mock_choice):
        """
        Test that get_fortune uses random.choice to select from the FORTUNES list.
        # Mock rationale: random.choice is non-deterministic. Mocking it ensures
        # that we can predict the output and verify it comes from our predefined list.
        """
        expected_fortune = "This is a mock fortune."
        mock_choice.return_value = expected_fortune
        
        fortune = get_fortune()
        
        mock_choice.assert_called_once_with(FORTUNES)
        self.assertEqual(fortune, expected_fortune)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.fortune_teller.get_fortune')
    def test_main_output_no_args(self, mock_get_fortune, mock_stdout):
        """
        Test the main function's output when no arguments are provided.
        # Mock rationale: sys.stdout is mocked to capture printed output for assertion.
        # src.fortune_teller.get_fortune is mocked to control the fortune returned
        # and ensure deterministic output for testing the CLI interface.
        """
        mock_get_fortune.return_value = "A test fortune for you."
        
        # Temporarily modify sys.argv to simulate no arguments
        original_argv = sys.argv
        sys.argv = ['fortune_teller.py']
        
        try:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("For your current coding challenge:", output)
            self.assertIn("✨ Your debugging fortune: A test fortune for you. ✨", output)
            self.assertIn("May your code compile and your tests pass!", output)
            mock_get_fortune.assert_called_once()
        finally:
            sys.argv = original_argv # Restore sys.argv

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.fortune_teller.get_fortune')
    def test_main_output_with_args(self, mock_get_fortune, mock_stdout):
        """
        Test the main function's output when arguments (an error message) are provided.
        # Mock rationale: sys.stdout is mocked to capture printed output for assertion.
        # src.fortune_teller.get_fortune is mocked to control the fortune returned
        # and ensure deterministic output for testing the CLI interface.
        """
        mock_get_fortune.return_value = "Another test fortune."
        test_error_message = "Error: File not found"
        
        # Temporarily modify sys.argv to simulate arguments
        original_argv = sys.argv
        sys.argv = ['fortune_teller.py', test_error_message]
        
        try:
            main()
            output = mock_stdout.getvalue()
            self.assertIn(f"For your error: '{test_error_message}'", output)
            self.assertIn("✨ Your debugging fortune: Another test fortune. ✨", output)
            self.assertIn("May your code compile and your tests pass!", output)
            mock_get_fortune.assert_called_once()
        finally:
            sys.argv = original_argv # Restore sys.argv

if __name__ == '__main__':
    unittest.main()
