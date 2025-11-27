import os
import sys

# Ensure the src package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

import pytest
from namer import get_color_name, _parse_hex


def test_parse_hex_valid():
    assert _parse_hex("#ff0000") == (255, 0, 0)
    assert _parse_hex("00ff00") == (0, 255, 0)
    assert _parse_hex("0000ff") == (0, 0, 255)


def test_parse_hex_invalid():
    with pytest.raises(ValueError):
        _parse_hex("gggggg")  # invalid characters
    with pytest.raises(ValueError):
        _parse_hex("#123")   # too short


@pytest.mark.parametrize(
    "hex_code,expected",
    [
        ("#ff0000", "red"),
        ("#00ff00", "lime"),
        ("#0000ff", "blue"),
        ("#ffff00", "yellow"),
        ("#123456", "navy"),  # nearest among palette
    ],
)
def test_get_color_name(hex_code, expected):
    assert get_color_name(hex_code) == expected
