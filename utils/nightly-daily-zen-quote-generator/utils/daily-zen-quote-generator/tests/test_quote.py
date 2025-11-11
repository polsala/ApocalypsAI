import datetime
import builtins
from unittest import mock

# Mock rationale: ensure deterministic output regardless of the actual current date.

from daily_zen_quote_generator import get_quote

def test_get_quote_fixed_date():
    # 2023-01-01 has ordinal 738156; with 8 quotes, index = 738156 % 8 = 4
    fixed_date = datetime.date(2023, 1, 1)
    expected = "\"Know yourself and you will win all battles.\" – Sun Tzu"
    assert get_quote(fixed_date) == expected

def test_get_quote_today_uses_mocked_today():
    mock_today = datetime.date(2022, 12, 31)  # ordinal 738155, index = 3
    with mock.patch.object(datetime.date, "today", return_value=mock_today):
        result = get_quote()
    expected = "\"The obstacle is the path.\" – Zen Proverb"
    assert result == expected

def test_cli_output(capsys):
    # Simulate running the module as a script with a mocked date.
    mock_today = datetime.date(2022, 12, 30)  # ordinal 738154, index = 2
    with mock.patch.object(datetime.date, "today", return_value=mock_today):
        # Import the module fresh to trigger __main__ guard via runpy
        import importlib
        import runpy
        runpy.run_module("daily_zen_quote_generator", run_name="__main__")
    captured = capsys.readouterr()
    expected = "\"Simplicity is the ultimate sophistication.\" – Leonardo da Vinci\n"
    assert captured.out == expected
