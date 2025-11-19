import pytest
from utils.nightly_emoji_calendar.src.calendar import render_month


def test_render_january_2023():
    expected = (
        "   January 2023\n"
        "Mo Tu We Th Fr Sa Su\n"
        "            🌞 🌜\n"
        " 3  4  5  6  7 🌞 🌜\n"
        "10 11 12 13 14 🌞 🌜\n"
        "17 18 19 20 21 🌞 🌜\n"
        "24 25 26 27 28 🌞 🌜\n"
        "31"
    )
    result = render_month(2023, 1)
    assert result == expected
