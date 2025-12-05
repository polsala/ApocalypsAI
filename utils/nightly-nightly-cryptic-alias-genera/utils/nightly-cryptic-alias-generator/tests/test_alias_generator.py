import unittest
import sys
import os
from unittest.mock import patch

# Add the src directory to the Python path to allow importing alias_generator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from alias_generator import generate_alias, ADJECTIVES, NOUNS

class TestAliasGenerator(unittest.TestCase):

    def test_deterministic_output(self):
        """
        Tests that the same input always produces the same alias.
        """
        input_str_1 = "utils/nightly-nightly-config-schema-valida/src/validator.py"
        input_str_2 = "utils/nightly-nightly-config-schema-valida/src/validator.py" # Same as 1
        input_str_3 = "another/unique/path/to/file.txt"

        alias_1a = generate_alias(input_str_1)
        alias_1b = generate_alias(input_str_2) # Should be identical to alias_1a
        alias_3a = generate_alias(input_str_3)
        alias_3b = generate_alias(input_str_3) # Should be identical to alias_3a

        self.assertEqual(alias_1a, alias_1b)
        self.assertEqual(alias_3a, alias_3b)
        self.assertNotEqual(alias_1a, alias_3a) # Different inputs should yield different aliases (highly probable)

    def test_empty_input(self):
        """
        Tests the behavior with an empty input string.
        """
        self.assertEqual(generate_alias(""), "Empty Void")

    def test_output_format(self):
        """
        Tests that the output alias is a two-word string.
        """
        alias = generate_alias("some/random/input")
        parts = alias.split()
        self.assertEqual(len(parts), 2)
        self.assertTrue(parts[0][0].isupper()) # First letter of adjective is uppercase
        self.assertTrue(parts[1][0].isupper()) # First letter of noun is uppercase

    def test_word_selection_from_lists(self):
        """
        Tests that the generated words are indeed from the predefined lists.
        """
        alias = generate_alias("test-string-for-words")
        adjective, noun = alias.split()
        self.assertIn(adjective, ADJECTIVES)
        self.assertIn(noun, NOUNS)

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w')) # Mock rationale: Suppress print output from main() to prevent test output pollution.
    @patch('sys.argv', ['alias_generator.py', 'test_cli_input']) # Mock rationale: Simulate command-line arguments for the main function.
    def test_main_function_output(self, mock_stdout):
        """
        Tests the main function's output when run from the command line.
        """
        # We need to capture stdout to check what main() prints
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output

        # Run the main function
        import alias_generator
        alias_generator.main()

        sys.stdout = sys.__stdout__ # Restore stdout

        expected_alias = generate_alias('test_cli_input')
        self.assertEqual(captured_output.getvalue().strip(), expected_alias)

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w')) # Mock rationale: Suppress print output from main() to prevent test output pollution.
    @patch('sys.stderr', new_callable=lambda: open(os.devnull, 'w')) # Mock rationale: Suppress error output from main() to prevent test output pollution.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner prematurely.
    @patch('sys.argv', ['alias_generator.py']) # Mock rationale: Simulate command-line arguments with no input for error handling test.
    def test_main_function_no_args(self, mock_exit, mock_stderr, mock_stdout):
        """
        Tests the main function's behavior when no arguments are provided.
        """
        import alias_generator
        alias_generator.main()
        mock_exit.assert_called_with(1) # Expect sys.exit(1) for incorrect usage

if __name__ == '__main__':
    unittest.main()
