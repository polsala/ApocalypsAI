import datetime

# Mock rationale: No external services are called; we directly import the pure functions.
from utils.emoji-calendar.src.main import get_emoji_date, number_to_emoji


def test_number_to_emoji():
    assert number_to_emoji(1) == "1️⃣"
    assert number_to_emoji(12) == "1️⃣2️⃣"
    assert number_to_emoji(31) == "3️⃣1️⃣"


def test_get_emoji_date_known():
    # 2023-10-31 is a Tuesday.
    test_date = datetime.date(2023, 10, 31)
    result = get_emoji_date(test_date)
    # Expected mapping based on the constants in main.py
    expected = "🌜 🎃 3️⃣1️⃣"
    assert result == expected
