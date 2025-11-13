import datetime
import builtins
import sys
from unittest import mock

# Mock rationale: All external influences (current date, stdout) are mocked so the tests run deterministically offline.

# Import the module under test.
sys.path.append("../src")  # Adjust path for test discovery when run from the utils folder.
from main import get_quote, main


def test_get_quote_fixed_date():
    # January 1st should map to the first quote.
    date = datetime.date(2023, 1, 1)
    expected = "The journey of a thousand miles begins with one step."
    assert get_quote(date) == expected


def test_get_quote_wrap_around():
    # With 5 quotes, day 6 should wrap to the first quote again.
    date = datetime.date(2023, 1, 6)  # 6th day of year
    expected = "The journey of a thousand miles begins with one step."
    assert get_quote(date) == expected


def test_main_prints_today_quote(capsys: mock.MagicMock):
    # Mock datetime.date.today() to a known date.
    fake_today = datetime.date(2023, 2, 1)  # 32nd day of year
    with mock.patch('datetime.date') as mock_date:
        mock_date.today.return_value = fake_today
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        main()
        captured = capsys.readouterr()
        # 32 % 5 = 2 -> third quote (zero‑based index 2)
        expected = "Simplicity is the ultimate sophistication.\n"
        assert captured.out == expected
