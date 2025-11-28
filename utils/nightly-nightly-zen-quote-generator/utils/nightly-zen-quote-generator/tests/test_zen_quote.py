import unittest
from unittest.mock import patch
import importlib.util
import pathlib
import sys

def _load_zen_module():
    """Dynamically load the zen_quote module from the source directory.

    This avoids package‑name issues caused by hyphens in the utility folder name.
    """
    module_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "zen_quote.py"
    spec = importlib.util.spec_from_file_location("zen_quote", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["zen_quote"] = module
    spec.loader.exec_module(module)
    return module

zen_module = _load_zen_module()
get_random_quote = zen_module.get_random_quote

class TestZenQuoteGenerator(unittest.TestCase):
    @patch('random.choice')
    def test_get_random_quote_returns_mocked(self, mock_choice):
        # Mock rationale: Ensure deterministic output by fixing the random.choice result.
        mock_choice.return_value = "Mocked Zen Quote"
        quote = get_random_quote()
        self.assertEqual(quote, "Mocked Zen Quote")
        mock_choice.assert_called_once()

if __name__ == "__main__":
    unittest.main()
