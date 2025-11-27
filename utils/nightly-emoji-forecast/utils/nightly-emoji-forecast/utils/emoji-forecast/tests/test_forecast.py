import datetime
from src.forecast import get_forecast, EMOJIS


def test_forecast_structure():
    """# Mock rationale: Using a fixed date guarantees a deterministic output.
    We only assert structural properties – length and valid emojis – which are
    guaranteed by the deterministic algorithm.
    """
    d = datetime.date(2023, 1, 1)
    forecast = get_forecast(d)
    # The forecast should consist of exactly three emojis
    assert len(forecast) == 3
    # Each character must be one of the defined emojis
    for ch in forecast:
        assert ch in EMOJIS


def test_consistency_across_calls():
    d = datetime.date(2025, 12, 25)
    first = get_forecast(d)
    second = get_forecast(d)
    assert first == second
