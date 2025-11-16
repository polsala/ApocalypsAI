import os
import sys
import unittest

# Add the src directory to the import path so we can import the translator module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from translator import translate

class TestEmojiTranslator(unittest.TestCase):
    def test_basic_replacement(self):
        # Mock rationale: deterministic mapping ensures predictable output
        input_text = "I love my cat and dog."
        expected = "I ❤️ my 🐱 and 🐶."
        self.assertEqual(translate(input_text), expected)

    def test_case_insensitivity_and_punctuation(self):
        # Mock rationale: regex is case‑insensitive and respects word boundaries
        input_text = "She smiles at the Star!"
        # "smiles" does not match "smile", only "Star" matches.
        expected = "She smiles at the ⭐!"
        self.assertEqual(translate(input_text), expected)

    def test_no_match(self):
        # Mock rationale: text without keywords remains unchanged
        self.assertEqual(translate("Just a normal sentence."), "Just a normal sentence.")

if __name__ == "__main__":
    unittest.main()
