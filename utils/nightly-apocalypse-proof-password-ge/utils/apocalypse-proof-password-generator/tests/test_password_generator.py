import unittest
from unittest.mock import patch
import sys
import os

# Add the src directory to the Python path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))))

from password_generator import generate_apocalypse_password, ADJECTIVES, NOUNS, SYMBOLS

class TestApocalypsePasswordGenerator(unittest.TestCase):

    @patch('secrets.choice')
    @patch('secrets.randbelow')
    def test_generate_default_password(self, mock_randbelow, mock_choice):
        # Mock rationale: Ensure deterministic output for `secrets.choice` and `secrets.randbelow`
        # so that the generated password is predictable for testing purposes.
        # This simulates specific random selections.

        # Sequence for secrets.choice:
        # 1. First ADJECTIVE
        # 2. First NOUN
        # 3. First SYMBOL
        # 4. Second ADJECTIVE
        # 5. Second NOUN
        mock_choice.side_effect = [
            ADJECTIVES[0], # Ancient
            NOUNS[0],      # Relic
            SYMBOLS[0],    # !
            ADJECTIVES[1], # Cosmic
            NOUNS[1]       # Comet
        ]

        # Sequence for secrets.randbelow (for digits):
        # 1. First digit (e.g., 5)
        # 2. Second digit (e.g., 9)
        mock_randbelow.side_effect = [5, 9]

        expected_password = "Ancient-Relic-59-!-Cosmic-Comet"
        generated_password = generate_apocalypse_password(num_digits=2, num_symbols=1)

        self.assertEqual(generated_password, expected_password)
        self.assertEqual(mock_choice.call_count, 5) # 2 Adjectives, 2 Nouns, 1 Symbol
        self.assertEqual(mock_randbelow.call_count, 2) # 2 Digits

    @patch('secrets.choice')
    @patch('secrets.randbelow')
    def test_generate_password_with_different_counts(self, mock_randbelow, mock_choice):
        # Mock rationale: Test with different numbers of digits and symbols.
        # Ensure deterministic output for `secrets.choice` and `secrets.randbelow`.

        # Sequence for secrets.choice:
        # 1. ADJECTIVES[2] (Silent)
        # 2. NOUNS[2] (Whisper)
        # 3. SYMBOLS[1] (@)
        # 4. ADJECTIVES[3] (Fiery)
        # 5. NOUNS[3] (Dust)
        mock_choice.side_effect = [
            ADJECTIVES[2], # Silent
            NOUNS[2],      # Whisper
            SYMBOLS[1],    # @
            ADJECTIVES[3], # Fiery
            NOUNS[3]       # Dust
        ]

        # Sequence for secrets.randbelow (for digits):
        # 1. First digit (e.g., 1)
        # 2. Second digit (e.g., 2)
        # 3. Third digit (e.g., 3)
        mock_randbelow.side_effect = [1, 2, 3]

        expected_password = "Silent-Whisper-123-@-Fiery-Dust"
        generated_password = generate_apocalypse_password(num_digits=3, num_symbols=1)

        self.assertEqual(generated_password, expected_password)
        self.assertEqual(mock_choice.call_count, 5) # 2 Adjectives, 2 Nouns, 1 Symbol
        self.assertEqual(mock_randbelow.call_count, 3) # 3 Digits

    def test_invalid_num_digits(self):
        # Mock rationale: No mocking needed as this tests input validation logic.
        with self.assertRaises(ValueError) as cm:
            generate_apocalypse_password(num_digits=0)
        self.assertIn("Number of digits must be at least 1.", str(cm.exception))

    def test_invalid_num_symbols(self):
        # Mock rationale: No mocking needed as this tests input validation logic.
        with self.assertRaises(ValueError) as cm:
            generate_apocalypse_password(num_symbols=0)
        self.assertIn("Number of symbols must be at least 1.", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
