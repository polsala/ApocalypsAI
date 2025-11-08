import datetime
import sys
from pathlib import Path

# Ensure the src directory is on the import path.
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from main import get_zen_quote

def test_known_dates_return_expected_quotes():
    # These expectations were generated once and are now hard‑coded.
    cases = {
        "2025-01-01": "The river flows, but the stones remain.",
        "2025-06-15": "Patience is the art of quiet strength.",
        "2025-12-31": "A calm mind sees the path clearly.",
    }
    for date_str, expected in cases.items():
        assert get_zen_quote(date_str) == expected

def test_default_uses_today(monkeypatch):
    # Mock datetime.date.today() to a known value.
    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2025, 11, 8)  # Fixed date for test

    monkeypatch.setattr(datetime, "date", MockDate)
    # Expected quote for 2025‑11‑08 (pre‑computed).
    expected = "When the wind stops, the leaves still whisper."
    assert get_zen_quote() == expected

def test_invalid_date_raises():
    try:
        get_zen_quote("2025-13-01")
    except ValueError as e:
        assert "Invalid date format" in str(e)
    else:
        assert False, "ValueError not raised for invalid date"

# Mock rationale comments (no external network calls are performed).
# Mock rationale: All tests are deterministic and rely solely on the built‑in
# quote list and standard library functions.
