import datetime

from src.zen import get_quote


def test_quote_determinism_fixed_date():
    """Ensure the same date always yields the same quote.

    The test uses a hard‑coded date and checks the returned quote against the
    expected value from the internal list. No external resources are required.
    """
    test_date = datetime.date(2023, 1, 1)  # Known ordinal
    expected = (
        "When the mind is still, the universe surrenders."
    )
    assert get_quote(test_date) == expected


def test_today_fallback(monkeypatch):
    """Mock ``datetime.date.today`` to verify fallback behaviour.

    # Mock rationale: we replace ``today`` with a deterministic date so the test
    # remains offline and repeatable.
    """
    class MockDate(datetime.date):
        @classmethod
        def today(cls):  # type: ignore[override]
            return datetime.date(2022, 12, 31)

    monkeypatch.setattr(datetime, "date", MockDate)
    # 2022‑12‑31 ordinal % len(_QUOTES) should map to a known quote
    expected = "The obstacle is the path."
    assert get_quote() == expected
