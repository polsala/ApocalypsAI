import unittest
from unittest import mock
import pathlib
import importlib.util
import sys

# Helper to load the module from the source file without relying on package imports
def load_quote_module():
    module_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "quote.py"
    spec = importlib.util.spec_from_file_location("quote", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class TestQuoteUtility(unittest.TestCase):
    def setUp(self):
        self.quote_mod = load_quote_module()
        self.sample_quotes = ["Test quote one.", "Test quote two."]

    @mock.patch.object(random, "choice")
    def test_get_random_quote_uses_random_choice(self, mock_choice):
        # Mock random.choice to return the first quote
        mock_choice.return_value = self.sample_quotes[0]
        result = self.quote_mod.get_random_quote(self.sample_quotes)
        mock_choice.assert_called_once_with(self.sample_quotes)
        self.assertEqual(result, self.sample_quotes[0])

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='["Mocked quote"]')
    def test_load_quotes_reads_file(self, mock_file):
        dummy_path = pathlib.Path("dummy/quotes.json")
        quotes = self.quote_mod.load_quotes(dummy_path)
        mock_file.assert_called_once_with(dummy_path, encoding="utf-8")
        self.assertEqual(quotes, ["Mocked quote"])

    def test_main_successful_output(self):
        # Mock load_quotes and get_random_quote to control the flow
        with mock.patch.object(self.quote_mod, "load_quotes", return_value=self.sample_quotes), \
             mock.patch.object(self.quote_mod, "get_random_quote", return_value=self.sample_quotes[1]), \
             mock.patch.object(sys, "stdout", new_callable=mock.Mock) as mock_stdout:
            self.quote_mod.main()
            mock_stdout.write.assert_called_with(self.sample_quotes[1] + "\n")

    def test_main_handles_error(self):
        # Force load_quotes to raise an exception
        with mock.patch.object(self.quote_mod, "load_quotes", side_effect=FileNotFoundError("missing")), \
             mock.patch.object(sys, "stderr", new_callable=mock.Mock) as mock_stderr, \
             self.assertRaises(SystemExit) as cm:
            self.quote_mod.main()
        self.assertEqual(cm.exception.code, 1)
        mock_stderr.write.assert_called()

if __name__ == "__main__":
    unittest.main()
