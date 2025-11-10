import io
import sys
import unittest
from unittest.mock import patch
from datetime import date
import importlib.util
import pathlib

# Mock rationale: we mock datetime.date.today to make the quote deterministic.

def load_module():
    src_path = pathlib.Path(__file__).parent.parent / "src" / "main.py"
    spec = importlib.util.spec_from_file_location("quote_mod", src_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class TestDailyZenQuoteGenerator(unittest.TestCase):
    @patch.object(date, "today")
    def test_quote_of_fixed_date(self, mock_today):
        mock_today.return_value = date(2023, 1, 1)  # fixed date
        quote_mod = load_module()
        captured = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured
        try:
            quote_mod.main([])
        finally:
            sys.stdout = sys_stdout
        # Ordinal 2023-01-01 % 5 == 1, so expect second quote
        expected = "When the mind is still, the universe surrenders."
        self.assertEqual(captured.getvalue().strip(), expected)

if __name__ == "__main__":
    unittest.main()
