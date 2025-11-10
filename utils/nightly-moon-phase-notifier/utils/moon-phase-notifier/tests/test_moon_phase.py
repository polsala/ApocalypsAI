import datetime

from src.moon_phase import get_moon_phase

# Mock rationale: deterministic mapping based on known lunar dates.
# The dates below are taken from public lunar calendars and correspond to
# the exact start of each primary phase. The algorithm used in the utility
# is deterministic and does not require any network access, making these
# tests fully offline.

def test_new_moon():
    date = datetime.date(2023, 1, 21)  # Known new moon
    phase, emoji = get_moon_phase(date)
    assert phase == "New Moon"
    assert emoji == "🌑"


def test_first_quarter():
    date = datetime.date(2023, 1, 28)  # Known first quarter
    phase, emoji = get_moon_phase(date)
    assert phase == "First Quarter"
    assert emoji == "🌓"


def test_full_moon():
    date = datetime.date(2023, 2, 5)  # Known full moon
    phase, emoji = get_moon_phase(date)
    assert phase == "Full Moon"
    assert emoji == "🌕"


def test_last_quarter():
    date = datetime.date(2023, 2, 13)  # Known last quarter
    phase, emoji = get_moon_phase(date)
    assert phase == "Last Quarter"
    assert emoji == "🌗"
