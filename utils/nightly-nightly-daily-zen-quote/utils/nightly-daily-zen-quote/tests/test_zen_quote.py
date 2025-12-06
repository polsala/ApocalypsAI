import sys
import pathlib
import datetime

# Mock rationale: add the src directory to sys.path so we can import the module directly.
src_path = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

from zen_quote import get_zen_quote


def test_known_dates():
    """Validate that specific dates map to the expected deterministic quotes."""
    cases = [
        (datetime.date(2023, 1, 1), "Be present, not perfect."),
        (datetime.date(2023, 1, 2), "All we have is now."),
        (datetime.date(2023, 1, 10), "The obstacle is the path."),
        (datetime.date(2025, 12, 31), "The journey of a thousand miles begins with one step."),
    ]
    for d, expected in cases:
        assert get_zen_quote(d) == expected
