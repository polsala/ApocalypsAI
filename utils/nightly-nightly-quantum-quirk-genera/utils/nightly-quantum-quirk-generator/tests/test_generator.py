import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add the src directory to the path for importing generator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from generator import generate_passphrase, DEFAULT_WORDLIST, main

class TestPassphraseGenerator(unittest.TestCase):

    @patch('random.SystemRandom')
    def test_generate_passphrase_default(self, mock_system_random):
        # Mock rationale: Ensure deterministic word selection for testing.
        # We control which words are "randomly" chosen from the wordlist.
        mock_rng_instance = MagicMock()
        mock_system_random.return_value = mock_rng_instance
        mock_rng_instance.sample.return_value = ["apocalypse", "wasteland", "mutant", "scavenger"]

        passphrase = generate_passphrase()
        self.assertEqual(passphrase, "apocalypse-wasteland-mutant-scavenger")
        mock_rng_instance.sample.assert_called_once_with(DEFAULT_WORDLIST, 4)

    @patch('random.SystemRandom')
    def test_generate_passphrase_custom_words_and_separator(self, mock_system_random):
        # Mock rationale: Ensure deterministic word selection for testing.
        # We control which words are "randomly" chosen from the wordlist.
        mock_rng_instance = MagicMock()
        mock_system_random.return_value = mock_rng_instance
        custom_wordlist = ["alpha", "beta", "gamma", "delta", "epsilon"]
        mock_rng_instance.sample.return_value = ["alpha", "gamma", "epsilon"]

        passphrase = generate_passphrase(num_words=3, separator=".", wordlist=custom_wordlist)
        self.assertEqual(passphrase, "alpha.gamma.epsilon")
        mock_rng_instance.sample.assert_called_once_with(custom_wordlist, 3)

    def test_generate_passphrase_invalid_num_words_low(self):
        with self.assertRaisesRegex(ValueError, "Number of words must be between 3 and 10."):
            generate_passphrase(num_words=2)

    def test_generate_passphrase_invalid_num_words_high(self):
        with self.assertRaisesRegex(ValueError, "Number of words must be between 3 and 10."):
            generate_passphrase(num_words=11)

    def test_generate_passphrase_wordlist_too_small(self):
        small_wordlist = ["one", "two"]
        with self.assertRaisesRegex(ValueError, "Wordlist must contain at least 3 unique words."):
            generate_passphrase(num_words=3, wordlist=small_wordlist)

    @patch('random.SystemRandom')
    def test_main_default_args(self, mock_system_random):
        # Mock rationale: Ensure deterministic word selection for testing the CLI.
        mock_rng_instance = MagicMock()
        mock_system_random.return_value = mock_rng_instance
        mock_rng_instance.sample.return_value = ["apocalypse", "wasteland", "mutant", "scavenger"]

        # Mock stdout to capture print output
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Mock sys.argv to simulate command-line arguments
        with patch('sys.argv', ['generator.py']):
            main()
        
        sys.stdout = sys.__stdout__ # Reset stdout
        self.assertEqual(captured_output.getvalue().strip(), "apocalypse-wasteland-mutant-scavenger")

    @patch('random.SystemRandom')
    def test_main_custom_args(self, mock_system_random):
        # Mock rationale: Ensure deterministic word selection for testing the CLI.
        mock_rng_instance = MagicMock()
        mock_system_random.return_value = mock_rng_instance
        mock_rng_instance.sample.return_value = ["alpha", "beta", "gamma"]

        captured_output = StringIO()
        sys.stdout = captured_output
        
        with patch('sys.argv', ['generator.py', '-n', '3', '-s', '_']):
            main()
        
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "alpha_beta_gamma")

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="word1\nword2\nword3\nword4")
    @patch('random.SystemRandom')
    def test_main_with_wordlist_file(self, mock_system_random, mock_open, mock_exists):
        # Mock rationale: Simulate file existence and content for wordlist loading.
        # Mock rationale: Ensure deterministic word selection from the mocked file content.
        mock_rng_instance = MagicMock()
        mock_system_random.return_value = mock_rng_instance
        mock_rng_instance.sample.return_value = ["word1", "word3", "word4"]

        captured_output = StringIO()
        sys.stdout = captured_output
        
        with patch('sys.argv', ['generator.py', '-n', '3', '-w', 'my_wordlist.txt']):
            main()
        
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "word1-word3-word4")
        mock_open.assert_called_once_with('my_wordlist.txt', 'r')
        mock_rng_instance.sample.assert_called_once_with(["word1", "word2", "word3", "word4"], 3)

    @patch('os.path.exists', return_value=False)
    def test_main_wordlist_file_not_found(self, mock_exists):
        # Mock rationale: Simulate a non-existent file to test error handling.
        captured_output = StringIO()
        sys.stderr = captured_output
        
        with patch('sys.argv', ['generator.py', '-w', 'non_existent.txt']), \
             self.assertRaises(SystemExit) as cm: # main() calls exit(1)
            main()
        
        sys.stderr = sys.__stdout__
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Wordlist file 'non_existent.txt' not found.", captured_output.getvalue())

    def test_main_invalid_num_words_cli(self):
        captured_output = StringIO()
        sys.stderr = captured_output
        
        with patch('sys.argv', ['generator.py', '-n', '2']), \
             self.assertRaises(SystemExit) as cm:
            main()
        
        sys.stderr = sys.__stdout__
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Number of words must be between 3 and 10.", captured_output.getvalue())

# Restore original path after tests
sys.path.pop(0)

if __name__ == '__main__':
    unittest.main()
