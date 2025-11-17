import datetime

from src.forecast import get_forecast


def test_consistency():
    """# Mock rationale: The same date must always yield the same forecast.
    This ensures the hashing logic is deterministic and offline.
    """
    d = datetime.date(2023, 1, 1)
    first = get_forecast(d)
    second = get_forecast(d)
    assert first == second


def test_variation():
    """# Mock rationale: Different dates should produce different forecasts.
    Guarantees that the hash seed influences the output.
    """
    d1 = datetime.date(2023, 1, 1)
    d2 = datetime.date(2023, 1, 2)
    assert get_forecast(d1) != get_forecast(d2)
