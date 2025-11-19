import sys
import pathlib

# Mock rationale: extend sys.path so the src module can be imported without installing a package.
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import pytest
from src.convert import convert_time


def test_new_york_to_tokyo():
    """2025‑11‑19 15:30 in New York (EST, UTC‑5) → Tokyo (JST, UTC+9)."""
    result = convert_time("2025-11-19 15:30", "America/New_York", "Asia/Tokyo")
    assert result == "2025-11-20T05:30:00+09:00"


def test_london_to_sydney():
    """2025‑06‑01 12:00 in London (BST, UTC+1) → Sydney (AEST, UTC+10)."""
    result = convert_time("2025-06-01 12:00", "Europe/London", "Australia/Sydney")
    assert result == "2025-06-01T21:00:00+10:00"


def test_invalid_timezone():
    """Ensure an unknown zone raises an exception (mock rationale: deterministic error path)."""
    with pytest.raises(Exception):
        convert_time("2025-01-01 00:00", "Invalid/Zone", "UTC")
