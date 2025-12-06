import datetime

from src.moon_phase import get_moon_phase

# Mock rationale: These dates are well‑known lunar phases (UTC) and provide a deterministic test suite.

def test_new_moon():
    # 2023‑01‑21 was a New Moon
    date = datetime.date(2023, 1, 21)
    assert get_moon_phase(date) == "New Moon"


def test_first_quarter():
    # 2023‑01‑28 was a First Quarter
    date = datetime.date(2023, 1, 28)
    assert get_moon_phase(date) == "First Quarter"


def test_full_moon():
    # 2023‑02‑05 was a Full Moon
    date = datetime.date(2023, 2, 5)
    assert get_moon_phase(date) == "Full Moon"


def test_last_quarter():
    # 2023‑02‑13 was a Last Quarter
    date = datetime.date(2023, 2, 13)
    assert get_moon_phase(date) == "Last Quarter"
