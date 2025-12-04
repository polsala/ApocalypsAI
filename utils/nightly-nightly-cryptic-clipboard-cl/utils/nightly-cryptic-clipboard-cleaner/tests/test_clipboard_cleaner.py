import unittest
from src.clipboard_cleaner import clean_clipboard


class TestClipboardCleaner(unittest.TestCase):
    def test_ascii_preserved(self):
        self.assertEqual(clean_clipboard("Hello World"), "Hello World")

    def test_non_ascii_removed(self):
        # Contains em‑dash and non‑breaking space
        self.assertEqual(clean_clipboard("Hello—World\u00A0!"), "Hello-World !")

    def test_whitespace_collapsed(self):
        self.assertEqual(clean_clipboard("  Foo \t\n Bar  "), "Foo Bar")

    def test_combined(self):
        # Mixed Unicode characters, punctuation, and whitespace
        input_text = "\u2003\u00A0Café\u2009Müller—2023\u00A0\u2002"
        # Expected after cleaning: "Cafe Muller-2023"
        self.assertEqual(clean_clipboard(input_text), "Cafe Muller-2023")


if __name__ == "__main__":
    unittest.main()
