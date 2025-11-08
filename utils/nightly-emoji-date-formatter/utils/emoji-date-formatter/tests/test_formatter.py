import pytest

# Mock rationale: No external services are called; all logic is pure Python.
# The tests are deterministic and run offline.

from utils.emoji_date_formatter.src.formatter import format_date

@pytest.mark.parametrize(
    "input_date,expected",
    [
        ("2025-12-31", "🎄 2️⃣2️⃣❄️"),
        ("1999-01-01", "🌱 1️⃣9️⃣9️⃣0️⃣1️⃣"),
        ("2000-07-04", "🏖️ 2️⃣0️⃣0️⃣00️⃣4️⃣"),
        ("2023-10-31", "🎃 2️⃣0️⃣2️⃣33️⃣1️⃣"),
    ],
)
def test_format_date(input_date, expected):
    assert format_date(input_date) == expected

def test_invalid_format():
    with pytest.raises(ValueError):
        format_date("2025/12/31")  # wrong separator
    with pytest.raises(ValueError):
        format_date("20251231")   # missing dashes
    with pytest.raises(ValueError):
        format_date("2025-13-01")  # month out of range – still passes mapping fallback, but format is syntactically correct; we only validate structure, not range.
