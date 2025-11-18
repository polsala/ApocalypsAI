import sys
import pathlib

# Add the src directory to sys.path so we can import the module directly.
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from duration_parser import parse_duration

import pytest

@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("10s", 10),
        ("5m", 300),
        ("2h", 7200),
        ("1d", 86400),
        ("1h30m", 5400),
        ("2d 3h 4m 5s", 2*86400 + 3*3600 + 4*60 + 5),
        ("0s", 0),
    ],
)
def test_parse_valid(input_str, expected):
    assert parse_duration(input_str) == expected

def test_invalid_unit():
    with pytest.raises(ValueError, match="Unsupported unit"):
        parse_duration("5x")

def test_malformed_string():
    with pytest.raises(ValueError, match="Unrecognized format"):
        parse_duration("5")
