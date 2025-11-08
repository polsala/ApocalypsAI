import pytest

# Mock rationale: No external dependencies are used; the tests are fully deterministic.

from utils.emoji-date-formatter.src.emoji_date import format_date

@pytest.mark.parametrize(
    "input_date,expected",
    [
        ("2024-01-01", "2️⃣0️⃣2️⃣4🌸-0️⃣1️⃣"),
        ("1999-12-31", "1️⃣9️⃣9️⃣9🌾-3️⃣1️⃣"),
        ("0001-07-04", "0️⃣0️⃣0️⃣1🌱-0️⃣4️⃣"),
        ("2023-10-05", "2️⃣0️⃣2️⃣3🌴-0️⃣5️⃣"),
    ],
)
def test_format_date_success(input_date, expected):
    assert format_date(input_date) == expected


def test_format_date_invalid():
    with pytest.raises(ValueError) as excinfo:
        format_date("2023-02-30")  # Invalid day for February
    assert "Invalid ISO date" in str(excinfo.value)
