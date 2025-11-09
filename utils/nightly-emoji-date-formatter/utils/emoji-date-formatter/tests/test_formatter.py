import pytest
from src.formatter import date_to_emoji


def test_date_to_emoji_known():
    # Mock rationale: deterministic mapping, no network.
    result = date_to_emoji("2023-12-05")
    assert result == "2️⃣0️⃣2️⃣3️⃣ 🎄 0️⃣5️⃣"


def test_invalid_format_raises():
    with pytest.raises(ValueError):
        date_to_emoji("2023/12/05")
