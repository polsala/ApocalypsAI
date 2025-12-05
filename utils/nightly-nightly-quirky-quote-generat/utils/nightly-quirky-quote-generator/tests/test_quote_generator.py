import builtins
import random
import datetime
import importlib.util
import sys
from unittest import mock

# Mock rationale: Ensure deterministic choice without external randomness.
def test_get_random_quote_deterministic():
    # Mock random.choice to always return the first element
    with mock.patch('random.choice', return_value="Mocked Quote"):
        from src.quote_generator import get_random_quote
        assert get_random_quote() == "Mocked Quote"

def test_format_quote_uses_today_date():
    # Mock datetime.date.today to return a fixed date
    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2023, 1, 1)

    with mock.patch('datetime.date', MockDate):
        from src.quote_generator import format_quote
        result = format_quote("Test Quote")
        assert result == "2023-01-01: Test Quote"

def test_cli_output(capsys):
    # Mock random.choice to return a known quote
    with mock.patch('random.choice', return_value="CLI Quote"):
        # Import the module fresh to avoid seed side‑effects
        spec = importlib.util.find_spec('src.quote_generator')
        module = importlib.util.module_from_spec(spec)
        sys.modules['src.quote_generator'] = module
        spec.loader.exec_module(module)

        # Run main()
        module.main()
        captured = capsys.readouterr()
        # Mock date to a known value
        today = datetime.date.today().isoformat()
        expected = f"{today}: CLI Quote\n"
        assert captured.out == expected
