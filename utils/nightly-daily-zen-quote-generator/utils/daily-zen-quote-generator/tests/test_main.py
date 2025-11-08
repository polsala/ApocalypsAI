import unittest
from unittest.mock import patch

# Import the module under test
from src import main as quote_mod

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_random_quote_selection_is_deterministic_with_mock(self):
        """Ensure that the CLI prints the expected quote when random.choice is mocked.

        # Mock rationale: By patching ``random.choice`` we make the selection deterministic,
        # allowing the test to run offline without relying on actual randomness.
        """
        mock_quote = {"text": "Mocked Zen wisdom.", "tags": ["mock"]}
        with patch('random.choice', return_value=mock_quote):
            # Capture stdout
            with patch('builtins.print') as mock_print:
                quote_mod.main()
                mock_print.assert_called_once_with("Mocked Zen wisdom.")

    def test_theme_filter_returns_correct_subset(self):
        """Verify that filtering by a known theme returns only matching quotes.

        # Mock rationale: Directly call the helper without network or randomness.
        """
        filtered = quote_mod.filter_quotes('mindfulness')
        self.assertTrue(all('mindfulness' in [t.lower() for t in q['tags']] for q in filtered))
        # Ensure that at least one quote is returned (based on the static list above)
        self.assertGreater(len(filtered), 0)

    def test_no_quotes_for_unknown_theme(self):
        """When a theme has no matches, the CLI should inform the user.

        # Mock rationale: Patch ``print`` to capture the user‑facing message.
        """
        with patch('builtins.print') as mock_print:
            # Simulate CLI args by monkey‑patching argparse.Namespace
            with patch('argparse.ArgumentParser.parse_args', return_value=type('Args', (), {'theme': 'nonexistent'})):
                quote_mod.main()
                mock_print.assert_called_once_with("No quotes found for theme 'nonexistent'.")

if __name__ == '__main__':
    unittest.main()
