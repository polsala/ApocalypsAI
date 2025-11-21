import pytest

# Import the function from the utility package
from nightly_iso8601_duration_parser.src.parser import parse_iso8601_duration

# Test vectors: (input_string, expected_seconds)
TEST_CASES = [
    ("PT0S", 0),
    ("PT45S", 45),
    ("PT2M", 120),
    ("PT2M30S", 150),
    ("PT1H", 3600),
    ("PT1H15M", 4500),
    ("PT1H15M30S", 4530),
    ("P1D", 86_400),
    ("P2DT3H", 2 * 86_400 + 3 * 3_600),
    ("P3DT4H5M6S", 3 * 86_400 + 4 * 3_600 + 5 * 60 + 6),
]

@pytest.mark.parametrize("duration,expected", TEST_CASES)
def test_parse_iso8601_duration(duration, expected):
    assert parse_iso8601_duration(duration) == expected

def test_invalid_formats():
    # A collection of malformed strings that should raise ValueError
    invalid = [
        "",               # empty
        "P",              # period only, no component
        "PT",             # time designator only
        "1H30M",          # missing leading 'P'
        "P-1D",           # negative not supported
        "P1Y",            # years not supported in this subset
        "PT1H30M5",       # missing designator for seconds
    ]
    for bad in invalid:
        with pytest.raises(ValueError):
            parse_iso8601_duration(bad)
