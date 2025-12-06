import pytest
from human_delta import diff

# Mock rationale: All timestamps are hard‑coded ISO strings; no external I/O.

@pytest.mark.parametrize(
    "start,end,expected",
    [
        ("2023-01-01T00:00:00", "2023-01-01T00:00:00", "0 seconds"),
        ("2023-01-01T00:00:00", "2023-01-01T00:00:05", "5 seconds"),
        ("2023-01-01T00:00:00", "2023-01-01T01:02:03", "1 hour, 2 minutes, 3 seconds"),
        ("2023-01-01T12:00:00", "2023-01-03T15:30:45", "2 days, 3 hours, 30 minutes, 45 seconds"),
        # Reverse order – function should auto‑swap
        ("2023-01-03T15:30:45", "2023-01-01T12:00:00", "2 days, 3 hours, 30 minutes, 45 seconds"),
    ],
)
def test_diff(start, end, expected):
    assert diff(start, end) == expected
