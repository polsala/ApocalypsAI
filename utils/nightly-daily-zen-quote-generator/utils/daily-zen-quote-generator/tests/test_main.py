import unittest
import importlib.util
import pathlib
import io
from contextlib import redirect_stdout
from datetime import date


def load_module():
    """Load the ``main`` module from the sibling ``src`` directory.

    Mock rationale: using ``importlib`` avoids import‑time side effects and works
    with the hyphenated utility folder name.
    """
    src_path = pathlib.Path(__file__).parent.parent / "src" / "main.py"
    spec = importlib.util.spec_from_file_location("quote_gen", src_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestDailyZenQuoteGenerator(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_get_quote_fixed_date(self):
        # Mock rationale: deterministic date ensures predictable quote
        test_date = date(2023, 1, 1)
        quote = self.mod.get_quote(test_date)
        quotes = self.mod.load_quotes()
        expected = quotes[test_date.toordinal() % len(quotes)]
        self.assertEqual(quote, expected)

    def test_cli_output(self):
        # Mock rationale: replace ``date.today`` to control CLI output
        original_today = self.mod.date.today
        self.mod.date.today = lambda: date(2023, 1, 2)
        try:
            f = io.StringIO()
            with redirect_stdout(f):
                self.mod.main()
            output = f.getvalue().strip()
            quotes = self.mod.load_quotes()
            expected = quotes[date(2023, 1, 2).toordinal() % len(quotes)]
            self.assertEqual(output, expected)
        finally:
            self.mod.date.today = original_today


if __name__ == "__main__":
    unittest.main()
