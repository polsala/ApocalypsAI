import pytest

# Mock rationale: No external resources are needed; all tests are pure function calls.

from utils.human-duration-parser.src.parser import parse_duration

@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("1s", 1),
        ("45s", 45),
        ("2m", 120),
        ("2m30s", 150),
        ("1h", 3600),
        ("1h15m", 4500),
        ("1h15m30s", 4530),
        ("2d", 172800),
        ("1d2h3m4s", 93784),
        (" 1d 2h 3m 4s ", 93784),  # whitespace tolerance
        ("3h2d", 183600),  # order‑agnostic
    ],
)
def test_parse_valid(input_str, expected):
    assert parse_duration(input_str) == expected

@pytest.mark.parametrize(
    "bad_input",
    [
        "",  # empty
        "abc",  # no numbers
        "10x",  # unsupported unit
        "5",  # missing unit
        "2h30",  # missing unit for minutes
        "2h30m5",  # trailing number without unit
    ],
)
def test_parse_invalid(bad_input):
    with pytest.raises(ValueError):
        parse_duration(bad_input)
