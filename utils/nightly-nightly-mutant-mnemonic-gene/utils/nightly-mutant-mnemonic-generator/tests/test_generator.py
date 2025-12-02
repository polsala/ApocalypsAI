import unittest
import os
from unittest.mock import patch, mock_open
from io import StringIO

# Adjust sys.path to allow importing the generator module from src/
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import generator
sys.path.pop(0)

class TestMnemonicGenerator(unittest.TestCase):

    # Mock rationale: Provide a consistent, small word list for deterministic testing.
    # This avoids reliance on an external file and ensures tests are repeatable.
    MOCK_WORD_LIST_CONTENT = "alpha\nbeta\ngamma\ndelta\nepsilon\nzeta"
    MOCK_WORD_LIST = [w.strip() for w in MOCK_WORD_LIST_CONTENT.split('\n') if w.strip()]

    @patch('builtins.open', new_callable=mock_open, read_data=MOCK_WORD_LIST_CONTENT)
    @patch('os.path.exists', return_value=True)
    def setUp(self, mock_exists, mock_file):
        # Ensure the word list is loaded from the mock file for each test
        self.mock_words = generator.load_word_list(generator.WORD_LIST_PATH)
        self.assertEqual(self.mock_words, self.MOCK_WORD_LIST)

    def test_load_word_list_success(self):
        # This is implicitly tested in setUp, but explicitly check here
        self.assertEqual(self.mock_words, ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta'])

    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('os.path.exists', return_value=True)
    def test_load_word_list_empty(self, mock_exists, mock_file):
        # Mock rationale: Test the scenario where the word list file is empty.
        # This ensures the utility handles invalid input gracefully.
        with self.assertRaisesRegex(ValueError, "Word list '.*' is empty."):
            generator.load_word_list('dummy_path.txt')

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('os.path.exists', return_value=False)
    def test_load_word_list_not_found(self, mock_exists, mock_file):
        # Mock rationale: Test the scenario where the word list file does not exist.
        # This ensures the utility handles missing files gracefully.
        with self.assertRaisesRegex(FileNotFoundError, "Word list file not found at '.*'."):
            generator.load_word_list('non_existent_path.txt')

    def test_generate_mnemonic_basic(self):
        # Mock rationale: Use a fixed seed for random.Random to ensure deterministic output.
        # This makes the test repeatable and predictable.
        mnemonic = generator.generate_mnemonic(3, '-', self.mock_words, seed=42)
        self.assertEqual(mnemonic, 'gamma-zeta-alpha')

    def test_generate_mnemonic_different_words_count(self):
        mnemonic = generator.generate_mnemonic(2, '_', self.mock_words, seed=100)
        self.assertEqual(mnemonic, 'zeta_gamma')

    def test_generate_mnemonic_different_separator(self):
        mnemonic = generator.generate_mnemonic(3, ' ', self.mock_words, seed=1)
        self.assertEqual(mnemonic, 'zeta epsilon delta')

    def test_generate_mnemonic_all_words(self):
        # Mock rationale: Test generating a mnemonic using all available words.
        # This verifies the logic for handling the full word list.
        mnemonic = generator.generate_mnemonic(len(self.mock_words), '.', self.mock_words, seed=50)
        self.assertEqual(mnemonic, 'gamma.zeta.epsilon.beta.alpha.delta')

    def test_generate_mnemonic_too_many_words(self):
        # Mock rationale: Test the error handling when requesting more words than available.
        # This ensures the utility fails gracefully with invalid input.
        with self.assertRaisesRegex(ValueError, "Cannot generate 7 unique words from a list of only 6 words."):
            generator.generate_mnemonic(7, '-', self.mock_words, seed=123)

    def test_generate_mnemonic_zero_words(self):
        # Mock rationale: Test the error handling when requesting zero words.
        # This ensures the utility fails gracefully with invalid input.
        with self.assertRaisesRegex(ValueError, "Number of words must be positive."):
            generator.generate_mnemonic(0, '-', self.mock_words, seed=123)

    def test_generate_mnemonic_uniqueness(self):
        # Mock rationale: Verify that all words in the generated mnemonic are unique.
        # This is a core requirement for a good passphrase.
        mnemonic = generator.generate_mnemonic(len(self.mock_words), '-', self.mock_words, seed=99)
        words_in_mnemonic = mnemonic.split('-')
        self.assertEqual(len(words_in_mnemonic), len(set(words_in_mnemonic)))

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('generator.load_word_list', return_value=MOCK_WORD_LIST)
    @patch('generator.generate_mnemonic', return_value='test-mnemonic')
    def test_main_success(self, mock_generate, mock_load, mock_stderr, mock_stdout):
        # Mock rationale: Mocking load_word_list and generate_mnemonic to isolate
        # the main function's argument parsing and output behavior.
        # This ensures the CLI interface works as expected without full end-to-end execution.
        test_args = ['--words', '3', '--separator', '_']
        with patch('sys.argv', ['generator.py'] + test_args):
            generator.main()
            self.assertEqual(mock_stdout.getvalue().strip(), 'test-mnemonic')
            mock_load.assert_called_once_with(generator.WORD_LIST_PATH)
            mock_generate.assert_called_once_with(3, '_', self.MOCK_WORD_LIST, seed=None)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('generator.load_word_list', side_effect=FileNotFoundError('Mock file not found'))
    def test_main_error_handling(self, mock_load, mock_stderr, mock_stdout):
        # Mock rationale: Mocking load_word_list to simulate a file not found error.
        # This tests the main function's error handling and exit code.
        test_args = ['--words', '3']
        with patch('sys.argv', ['generator.py'] + test_args):
            with self.assertRaises(SystemExit) as cm:
                generator.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn('Error: Mock file not found', mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('generator.load_word_list', return_value=MOCK_WORD_LIST)
    @patch('generator.generate_mnemonic', side_effect=ValueError('Mock value error'))
    def test_main_generation_error(self, mock_generate, mock_load, mock_stderr, mock_stdout):
        # Mock rationale: Mocking generate_mnemonic to simulate a ValueError during generation.
        # This tests the main function's error handling and exit code for generation issues.
        test_args = ['--words', '100'] # Will cause ValueError with small mock list
        with patch('sys.argv', ['generator.py'] + test_args):
            with self.assertRaises(SystemExit) as cm:
                generator.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn('Error: Mock value error', mock_stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
