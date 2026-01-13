import sys, pathlib

# Add src directory to import path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from app import compute_rations

def test_compute_rations_basic():
    data = {
        "days": 5,
        "items": [
            {"name": "canned beans", "quantity": 20},
            {"name": "water bottles", "quantity": 15}
        ]
    }
    expected = {
        "days": 5,
        "daily_rations": [
            {"name": "canned beans", "per_day": 4.0},
            {"name": "water bottles", "per_day": 3.0}
        ]
    }
    assert compute_rations(data) == expected

def test_invalid_days():
    data = {"days": 0, "items": []}
    try:
        compute_rations(data)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert "days must be a positive integer" in str(e)

# Mock rationale: No external resources are accessed; tests are deterministic.
