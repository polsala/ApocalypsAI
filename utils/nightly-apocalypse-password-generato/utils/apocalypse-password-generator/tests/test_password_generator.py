import unittest
from unittest.mock import patch, MagicMock
import string
import sys
import io

# Mock rationale: We need to mock the random module to ensure deterministic test results.
# random.choice is used for selecting individual characters in random passwords.
# random.sample is used for selecting unique words in passphrases.
# random.choices (if used for repetition) would also be mocked.

# Add the src directory to the path for importing the module
sys.path.insert(0, 'src')
from password_generator import generate_random_password, generate_apocalypse_passphrase, APOCALYPSE_WORDS, main
sys.path.pop(0) # Clean up path

class TestPasswordGenerator(unittest.TestCase):

    @patch('random.choice')
    def test_generate_random_password_basic(self, mock_choice):
        # Mock rationale: Ensure random.choice returns predictable characters for testing.
        # We want to verify length and character set inclusion.
        mock_choice.side_effect = ['a', 'B', '1', '!'] * 3 # Cycle through characters

        password = generate_random_password(length=12, include_lowercase=True, include_uppercase=True, include_digits=True, include_symbols=True)
        self.assertEqual(len(password), 12)
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))
        self.assertEqual(password, "aB1!aB1!aB1!") # Verify the exact sequence

    @patch('random.choice')
    def test_generate_random_password_only_lowercase(self, mock_choice):
        # Mock rationale: Test specific character set inclusion.
        mock_choice.side_effect = ['x', 'y', 'z'] * 2
        password = generate_random_password(length=6, include_lowercase=True, include_uppercase=False, include_digits=False, include_symbols=False)
        self.assertEqual(len(password), 6)
        self.assertTrue(all(c.islower() for c in password))
        self.assertEqual(password, "xyzxyz")

    def test_generate_random_password_zero_length(self):
        # Mock rationale: Test edge case for invalid input.
        with self.assertRaises(ValueError) as cm:
            generate_random_password(length=0)
        self.assertEqual(str(cm.exception), "Password length must be positive.")

    def test_generate_random_password_no_char_types(self):
        # Mock rationale: Test edge case where no character types are selected.
        with self.assertRaises(ValueError) as cm:
            generate_random_password(length=10, include_lowercase=False, include_uppercase=False, include_digits=False, include_symbols=False)
        self.assertEqual(str(cm.exception), "At least one character type must be selected.")

    @patch('random.sample')
    def test_generate_apocalypse_passphrase_basic(self, mock_sample):
        # Mock rationale: Ensure random.sample returns predictable words for testing.
        mock_sample.return_value = ["wasteland", "bunker", "fallout", "mutant"]
        
        passphrase = generate_apocalypse_passphrase(num_words=4, separator="-")
        self.assertEqual(passphrase, "wasteland-bunker-fallout-mutant")
        mock_sample.assert_called_once_with(APOCALYPSE_WORDS, 4)

    @patch('random.sample')
    def test_generate_apocalypse_passphrase_custom_separator(self, mock_sample):
        # Mock rationale: Test custom separator.
        mock_sample.return_value = ["scavenger", "survival"]
        
        passphrase = generate_apocalypse_passphrase(num_words=2, separator=" ")
        self.assertEqual(passphrase, "scavenger survival")
        mock_sample.assert_called_once_with(APOCALYPSE_WORDS, 2)

    @patch('random.choice') # If num_words > len(APOCALYPSE_WORDS), it uses random.choice
    def test_generate_apocalypse_passphrase_more_words_than_unique(self, mock_choice):
        # Mock rationale: Test scenario where more words are requested than unique words available.
        # In this case, random.choice is used for repetition.
        mock_choice.side_effect = ["wasteland", "wasteland", "bunker"]
        
        # Assume APOCALYPSE_WORDS has at least 2 words for this test
        # We request 3 words, but mock_choice will provide them
        passphrase = generate_apocalypse_passphrase(num_words=3, separator=".")
        self.assertEqual(passphrase, "wasteland.wasteland.bunker")
        self.assertEqual(mock_choice.call_count, 3) # Ensure choice was called 3 times

    def test_generate_apocalypse_passphrase_zero_words(self):
        # Mock rationale: Test edge case for invalid input.
        with self.assertRaises(ValueError) as cm:
            generate_apocalypse_passphrase(num_words=0)
        self.assertEqual(str(cm.exception), "Number of words must be positive.")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('password_generator.generate_random_password')
    def test_main_random_mode(self, mock_generate_random_password, mock_parse_args, mock_stdout):
        # Mock rationale: Test the main function's interaction with argparse and the generator.
        # We mock parse_args to control CLI arguments and generate_random_password to control its output.
        mock_parse_args.return_value = MagicMock(
            mode="random",
            length=10,
            digits=True,
            symbols=False,
            uppercase=True,
            lowercase=False,
            words=None,
            separator=None
        )
        mock_generate_random_password.return_value = "TestP@ss12"

        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "TestP@ss12")
        mock_generate_random_password.assert_called_once_with(
            10, include_digits=True, include_symbols=False, include_uppercase=True, include_lowercase=False
        )

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('password_generator.generate_random_password')
    def test_main_random_mode_default_chars(self, mock_generate_random_password, mock_parse_args, mock_stdout):
        # Mock rationale: Test the main function's default behavior when no char types are specified.
        mock_parse_args.return_value = MagicMock(
            mode="random",
            length=15,
            digits=False, # All false, so defaults should kick in
            symbols=False,
            uppercase=False,
            lowercase=False,
            words=None,
            separator=None
        )
        mock_generate_random_password.return_value = "DefaultP@ssword"

        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "DefaultP@ssword")
        mock_generate_random_password.assert_called_once_with(
            15, include_digits=True, include_symbols=True, include_uppercase=True, include_lowercase=True
        )

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('password_generator.generate_apocalypse_passphrase')
    def test_main_passphrase_mode(self, mock_generate_apocalypse_passphrase, mock_parse_args, mock_stdout):
        # Mock rationale: Test the main function's interaction with argparse and the passphrase generator.
        mock_parse_args.return_value = MagicMock(
            mode="passphrase",
            length=None,
            digits=None,
            symbols=None,
            uppercase=None,
            lowercase=None,
            words=3,
            separator=" "
        )
        mock_generate_apocalypse_passphrase.return_value = "bunker survival outpost"

        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "bunker survival outpost")
        mock_generate_apocalypse_passphrase.assert_called_once_with(3, " ")

if __name__ == '__main__':
    unittest.main()
