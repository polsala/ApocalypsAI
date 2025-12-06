import unittest
import sys
import pathlib
from unittest.mock import patch

# Mock rationale: adjust sys.path to import the module from src without installing as a package.
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2] / "src"))

from quote_dispenser import get_random_quote

class TestQuoteDispenser(unittest.TestCase):
    def test_mocked_choice(self):
        # Mock rationale: patching random.choice guarantees a known output, making the test deterministic.
        with patch('random.choice', return_value="The last backup fell silent.") as mock_choice:
            quote = get_random_quote()
            mock_choice.assert_called_once()
            self.assertEqual(quote, "The last backup fell silent.")

    def test_random_output_is_valid(self):
        # Mock rationale: ensure the returned quote is one of the known list without fixing seed.
        quote = get_random_quote()
        self.assertIn(quote, [
            "When the sky cracks, the earth whispers.",
            "Ashes to ash, dust to dust, code to code.",
            "The last backup fell silent.",
            "Even the servers sigh under the weight of silence.",
            "In the void, logs become legends."
        ])

if __name__ == "__main__":
    unittest.main()
