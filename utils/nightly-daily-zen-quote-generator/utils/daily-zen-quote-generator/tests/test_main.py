import builtins
import sys
from datetime import date
from unittest import mock

# Mock rationale: Ensure deterministic behavior without relying on actual current date.

# Import the module under test
from src.main import get_quote, deterministic_index, load_quotes

def test_load_quotes():
    quotes = load_quotes()
    assert isinstance(quotes, list)
    assert len(quotes) >= 1
    assert all(isinstance(q, str) for q in quotes)

def test_deterministic_index_consistency():
    quotes = ['a', 'b', 'c']
    d = date(2023, 1, 1)
    idx1 = deterministic_index(quotes, d)
    idx2 = deterministic_index(quotes, d)
    assert idx1 == idx2
    # Different date should likely give different index (not guaranteed but we test inequality for two far apart dates)
    d2 = date(2025, 12, 31)
    idx3 = deterministic_index(quotes, d2)
    assert idx1 != idx3 or len(quotes) == 1

def test_get_quote_fixed_date():
    # Mock today to a known date and verify the returned quote matches expected index.
    fixed_date = date(2022, 5, 17)
    with mock.patch('src.main.date') as mock_date:
        mock_date.today.return_value = fixed_date
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        quote = get_quote()
        # Compute expected index manually
        quotes = load_quotes()
        expected_idx = deterministic_index(quotes, fixed_date)
        assert quote == quotes[expected_idx]

def test_main_prints_quote(capsys):
    # Run the script's main function and capture stdout.
    from src.main import main
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() != ''
    # Ensure it matches one of the quotes.
    quotes = load_quotes()
    assert captured.out.strip() in quotes
