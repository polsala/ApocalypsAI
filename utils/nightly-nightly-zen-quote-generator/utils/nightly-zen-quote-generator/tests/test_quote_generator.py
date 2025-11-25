import builtins
import io
import os
import sys
import unittest
from unittest import mock
from pathlib import Path

# Mock rationale: deterministic selection of quote via patching random.choice
from utils.nightly_zen_quote_generator.src import quote_generator

class TestQuoteGenerator(unittest.TestCase):
    def setUp(self):
        # Ensure a clean stdout capture for each test
        self.captured_stdout = io.StringIO()
        self.captured_stderr = io.StringIO()
        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr
        sys.stdout = self.captured_stdout
        sys.stderr = self.captured_stderr

    def tearDown(self):
        sys.stdout = self._orig_stdout
        sys.stderr = self._orig_stderr

    @mock.patch('random.choice', return_value="Silence is a source of great strength.")
    def test_get_random_quote_no_filter(self, mock_choice):
        quote = quote_generator.get_random_quote()
        self.assertEqual(quote, "Silence is a source of great strength.")
        mock_choice.assert_called_once()

    @mock.patch('random.choice', return_value="The journey of a thousand miles begins with one step.")
    def test_get_random_quote_with_length_pass(self, mock_choice):
        quote = quote_generator.get_random_quote(max_length=80)
        self.assertIsNotNone(quote)
        self.assertTrue(len(quote) <= 80)

    @mock.patch('random.choice', return_value="The journey of a thousand miles begins with one step.")
    def test_get_random_quote_with_length_fail(self, mock_choice):
        quote = quote_generator.get_random_quote(max_length=10)
        self.assertIsNone(quote)

    @mock.patch('random.choice', return_value="Let go or be dragged.")
    def test_cli_stdout(self, mock_choice):
        exit_code = quote_generator.main([])
        self.assertEqual(exit_code, 0)
        self.assertIn("Let go or be dragged.", self.captured_stdout.getvalue().strip())

    @mock.patch('random.choice', return_value="Let go or be dragged.")
    def test_cli_max_length_filter_fails(self, mock_choice):
        exit_code = quote_generator.main(["--max-length", "5"])
        self.assertEqual(exit_code, 1)
        self.assertIn("No quote fits the length constraint", self.captured_stderr.getvalue())

    @mock.patch('random.choice', return_value="Nature does not hurry, yet everything is accomplished.")
    def test_cli_output_to_file(self, mock_choice):
        tmp_path = Path(self._temp_dir())
        out_file = tmp_path / "quote.txt"
        exit_code = quote_generator.main(["--output", str(out_file)])
        self.assertEqual(exit_code, 0)
        self.assertTrue(out_file.is_file())
        content = out_file.read_text(encoding="utf-8").strip()
        self.assertEqual(content, "Nature does not hurry, yet everything is accomplished.")

    def _temp_dir(self) -> str:
        """Create a temporary directory that is automatically cleaned up.

        Using the built‑in ``tempfile`` module would add an import, but the
        overhead is negligible and keeps the test self‑contained.
        """
        import tempfile
        return tempfile.mkdtemp()

if __name__ == "__main__":
    unittest.main()
