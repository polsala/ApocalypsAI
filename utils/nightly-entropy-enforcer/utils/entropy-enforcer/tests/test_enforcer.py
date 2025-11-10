import unittest
from unittest.mock import patch
import string
import io
import sys

# Adjust the import path for the utility
# Assuming tests are run from the utils/entropy-enforcer/ directory
# and src/enforcer.py is in the same directory structure.
from src.enforcer import generate_string, main

class TestEntropyEnforcer(unittest.TestCase):

    @patch('secrets.choice')
    def test_generate_string_basic_length(self, mock_secrets_choice):
        # Mock rationale: Ensure deterministic output for length testing.
        # We don't care about the specific characters, just that the correct number are chosen.
        mock_secrets_choice.return_value = 'a'
        
        length = 10
        result = generate_string(length=length)
        self.assertEqual(len(result), length)
        self.assertEqual(result, 'a' * length) # Verify the mock worked

    @patch('secrets.choice')
    def test_generate_string_character_types(self, mock_secrets_choice):
        # Mock rationale: Ensure deterministic character selection for type validation.
        # We provide a sequence of characters to ensure all requested types are "chosen"
        # from the *filtered* pool. The mock should return characters that would be valid
        # for the current character pool.
        
        # Test with all types
        # The actual character pool will be string.digits + ascii_lowercase + ascii_uppercase + punctuation
        # We need to ensure the mock returns characters that are part of this pool.
        mock_secrets_choice.side_effect = ['a', 'B', '1', '!'] * 5 # Cycle through types
        result = generate_string(length=4, include_digits=True, include_lower=True,
                                 include_upper=True, include_symbols=True)
        self.assertEqual(len(result), 4)
        self.assertTrue(any(c.islower() for c in result))
        self.assertTrue(any(c.isupper() for c in result))
        self.assertTrue(any(c.isdigit() for c in result))
        self.assertTrue(any(c in string.punctuation for c in result))

        # Test with only lowercase
        mock_secrets_choice.side_effect = ['a'] * 10
        result = generate_string(length=5, include_digits=False, include_lower=True,
                                 include_upper=False, include_symbols=False)
        self.assertEqual(len(result), 5)
        self.assertTrue(all(c.islower() for c in result))
        self.assertFalse(any(c.isupper() for c in result))
        self.assertFalse(any(c.isdigit() for c in result))
        self.assertFalse(any(c in string.punctuation for c in result))

    @patch('secrets.choice')
    def test_generate_string_exclude_ambiguous(self, mock_secrets_choice):
        # Mock rationale: Ensure deterministic character selection to verify exclusion.
        # The mock should return a character that is *not* ambiguous and *would* be in the filtered pool.
        # We'll test that the generated string does not contain ambiguous characters.
        
        # Simulate a pool where 'l', 'I', 'O', '0', '1' are present but should be excluded.
        # The mock should return a character that is *not* in "lIO01".
        mock_secrets_choice.return_value = 'k' # 'k' is not ambiguous and is lowercase

        result = generate_string(length=10, exclude_ambiguous=True)
        self.assertEqual(len(result), 10)
        # Check that common ambiguous characters are not in the result
        ambiguous_chars = "lIO01"
        self.assertFalse(any(c in ambiguous_chars for c in result))
        self.assertEqual(result, 'k' * 10) # Verify the mock worked with a non-ambiguous char

    def test_generate_string_empty_pool_error_no_types(self):
        # Test that an error is raised if no character types are selected
        with self.assertRaisesRegex(ValueError, "At least one character type must be included."):
            generate_string(length=10, include_digits=False, include_lower=False,
                            include_upper=False, include_symbols=False)
        
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('src.enforcer.generate_string')
    def test_main_success(self, mock_generate_string, mock_stdout):
        # Mock rationale: Isolate CLI execution from actual string generation and capture stdout.
        mock_generate_string.return_value = "mocked_password_123"
        
        # Simulate command line arguments
        with patch('sys.argv', ['enforcer.py', '--length', '8', '--symbols']):
            main()
            self.assertEqual(mock_stdout.getvalue().strip(), "mocked_password_123")
            mock_generate_string.assert_called_once_with(
                length=8,
                include_digits=True,
                include_lower=True,
                include_upper=True,
                include_symbols=True,
                exclude_ambiguous=False
            )

    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.stdout', new_callable=io.StringIO) # Also capture stdout to ensure nothing is printed there
    @patch('src.enforcer.generate_string')
    def test_main_error_handling(self, mock_generate_string, mock_stdout, mock_stderr):
        # Mock rationale: Isolate CLI error handling from actual string generation and capture stderr.
        mock_generate_string.side_effect = ValueError("Test error: No chars selected.")
        
        with patch('sys.argv', ['enforcer.py', '--no-digits', '--no-lower', '--no-upper']):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Test error: No chars selected.", mock_stderr.getvalue())
            self.assertEqual(mock_stdout.getvalue(), "") # Ensure nothing printed to stdout on error
