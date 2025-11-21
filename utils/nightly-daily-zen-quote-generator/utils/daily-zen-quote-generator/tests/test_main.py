import builtins
import sys
from unittest import mock

# Mock rationale: we replace random.choice with a deterministic function so the test does not rely on randomness.

def test_get_random_quote_returns_mocked_value():
    from daily_zen_quote_generator.src.main import get_random_quote
    with mock.patch('random.choice', return_value='Mocked Zen Quote'):
        assert get_random_quote() == 'Mocked Zen Quote'

def test_cli_outputs_mocked_quote(capsys):
    # Mock the get_random_quote function used by the CLI.
    with mock.patch('daily_zen_quote_generator.src.main.get_random_quote', return_value='CLI Mock Quote'):
        # Import the module after patching to ensure the patched function is used.
        from daily_zen_quote_generator.src import main as cli_main
        cli_main.main()
        captured = capsys.readouterr()
        assert captured.out.strip() == 'CLI Mock Quote'
