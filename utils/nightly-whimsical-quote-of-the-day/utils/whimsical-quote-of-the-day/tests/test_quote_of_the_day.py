import datetime
from unittest import mock

# Mock rationale: we replace datetime.date.today() to make the test deterministic without network.

from utils.whimsical-quote-of-the-day.src.quote_of_the_day import get_quote_of_the_day, QUOTES


def test_quote_determinism_fixed_date():
    # Choose a known date: 2023-03-15 (day 74 of the year, non‑leap year)
    fixed_date = datetime.date(2023, 3, 15)
    expected_index = (fixed_date.timetuple().tm_yday - 1) % len(QUOTES)
    expected_quote = QUOTES[expected_index]
    assert get_quote_of_the_day(fixed_date) == expected_quote


def test_today_mocked():
    # Mock datetime.date.today() to return 2024-12-31 (day 366, leap year)
    mock_today = datetime.date(2024, 12, 31)
    with mock.patch('utils.whimsical-quote-of-the-day.src.quote_of_the_day.datetime.date') as mock_date_class:
        mock_date_class.today.return_value = mock_today
        # Ensure that other date constructors still work (e.g., .fromtimestamp)
        mock_date_class.side_effect = lambda *args, **kwargs: datetime.date(*args, **kwargs)
        result = get_quote_of_the_day()
        expected_index = (mock_today.timetuple().tm_yday - 1) % len(QUOTES)
        assert result == QUOTES[expected_index]
