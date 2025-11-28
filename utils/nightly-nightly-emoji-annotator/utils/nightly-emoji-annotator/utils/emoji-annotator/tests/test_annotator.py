import unittest
from pathlib import Path
from unittest import mock

# Import the module under test
from ..src.annotator import annotate_text, main

class TestAnnotator(unittest.TestCase):
    def test_basic_replacements(self):
        input_text = "I love coffee and cats."
        expected = "I ❤️ ☕ and 🐱."
        self.assertEqual(annotate_text(input_text), expected)

    def test_case_insensitivity(self):
        input_text = "Fire and FIRE are hot."
        expected = "🔥 and 🔥 are hot."
        self.assertEqual(annotate_text(input_text), expected)

    def test_no_match(self)::
        input_text = "Just a plain sentence."
        self.assertEqual(annotate_text(input_text), input_text)

    def test_cli_success(self):
        # Mock file system interactions to keep the test offline and deterministic
        mock_input = mock.mock_open(read_data="I love pizza and music.")
        mock_output = mock.mock_open()
        with mock.patch('pathlib.Path.read_text', mock_input), \
             mock.patch('pathlib.Path.write_text', mock_output):
            # # Mock rationale: we replace actual disk I/O with in‑memory mocks
            exit_code = main(["dummy_input.txt", "dummy_output.txt"])
            self.assertEqual(exit_code, 0)
            # Verify that write_text was called with the correctly annotated string
            mock_output.assert_called_once_with("I ❤️ 🍕 and 🎵.", encoding="utf-8")

    def test_cli_missing_args(self):
        with self.assertRaises(SystemExit) as cm:
            # main expects exactly two args; providing none should cause a SystemExit with code 1
            main([])
        self.assertEqual(cm.exception.code, 1)

if __name__ == "__main__":
    unittest.main()
