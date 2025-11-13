import sys
import pathlib
import json
from unittest import mock

# Ensure the src directory is on the import path
sys.path.append(str(pathlib.Path(__file__).parents[1] / "src"))

from src import quote_fetcher

# Mock rationale: we replace file reading and random.choice to make tests deterministic.

def test_load_quotes_mock():
    mock_data = [
        {"text": "Mock quote 1", "author": "Author A"},
        {"text": "Mock quote 2"}
    ]
    mock_json = json.dumps(mock_data)

    # Mock open to return our mock_json
    mock_open = mock.mock_open(read_data=mock_json)
    with mock.patch.object(quote_fetcher.pathlib.Path, "open", mock_open):
        quotes = quote_fetcher._load_quotes()
        assert quotes == mock_data


def test_get_random_quote_deterministic():
    mock_quotes = [{"text": "Deterministic quote", "author": "Tester"}]

    # Mock _load_quotes to return our list
    with mock.patch.object(quote_fetcher, "_load_quotes", return_value=mock_quotes):
        # Mock random.choice to always return the first element
        with mock.patch("random.choice", lambda seq: seq[0]):
            quote = quote_fetcher.get_random_quote()
            assert quote == mock_quotes[0]


def test_cli_output(capsys):
    mock_quote = {"text": "CLI test", "author": "CapSys"}
    with mock.patch.object(quote_fetcher, "get_random_quote", return_value=mock_quote):
        quote_fetcher.main()
        captured = capsys.readouterr()
        expected = "\"CLI test\" — CapSys\n"
        assert captured.out == expected
