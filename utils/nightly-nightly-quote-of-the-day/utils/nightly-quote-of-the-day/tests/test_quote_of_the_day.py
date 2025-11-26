import datetime
import builtins
from unittest import mock

# Mock rationale: we replace datetime.date.today to a fixed date so the test is deterministic and offline.

def test_get_quote_for_known_date():
    from src.quote_of_the_day import get_quote_for_date, _QUOTES

    # January 1st should map to the first quote (index 0)
    fixed_date = datetime.date(2023, 1, 1)
    expected = _QUOTES[0]
    assert get_quote_for_date(fixed_date) == expected

    # February 15th (day 46) should map to index (46-1) % len(_QUOTES)
    fixed_date = datetime.date(2023, 2, 15)
    index = (46 - 1) % len(_QUOTES)
    expected = _QUOTES[index]
    assert get_quote_for_date(fixed_date) == expected

def test_cli_outputs_correct_quote():
    from src import quote_of_the_day
    import sys

    # Patch datetime.date.today to a known date and capture stdout.
    with mock.patch.object(datetime.date, "today", return_value=datetime.date(2023, 3, 3)):
        with mock.patch.object(sys, "stdout") as mock_stdout:
            # Mock stdout.write to capture printed text.
            mock_stdout.write = mock.Mock()
            quote_of_the_day.main()
            # The CLI prints the quote followed by a newline via print().
            # Retrieve the first call argument.
            printed = mock_stdout.write.call_args[0][0]
            # The printed string includes the newline; strip it for comparison.
            printed = printed.strip()
            expected = quote_of_the_day.get_quote_for_date(datetime.date(2023, 3, 3))
            assert printed == expected
