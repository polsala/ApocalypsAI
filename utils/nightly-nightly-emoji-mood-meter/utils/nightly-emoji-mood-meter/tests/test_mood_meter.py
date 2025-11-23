import pytest
from datetime import date

# Import the utility under test
from utils.nightly-emoji-mood-meter.src.mood_meter import get_mood

# Fixed list of emojis must match the implementation's EMOJIS order
EXPECTED_EMOJIS = [
    "😀",
    "😐",
    "😢",
    "🤔",
    "🔥",
    "🌧️",
    "🌟",
    "🌀",
    "🦄",
    "🚀",
]

@pytest.mark.parametrize(
    "test_date,expected_idx",
    [
        (date(2025, 1, 1), 0),   # Determined via manual hash check
        (date(2025, 1, 2), 5),
        (date(2025, 12, 31), 6),
        (date(2000, 2, 29), 9),
    ],
)
def test_get_mood_deterministic(test_date, expected_idx):
    """Ensure that get_mood returns the expected emoji for known dates.

    The expected indices were pre‑computed using the same hashing algorithm.
    """
    assert get_mood(test_date) == EXPECTED_EMOJIS[expected_idx]

def test_get_mood_consistency(monkeypatch):
    """Mock the internal hash function to guarantee a specific output.

    # Mock rationale: we replace the private _hash_date to control the index without
    # relying on the actual SHA‑256 implementation, keeping the test deterministic.
    """
    from utils.nightly-emoji-mood-meter.src import mood_meter

    def mock_hash(_):
        return 42  # Arbitrary number; 42 % len(EMOJIS) == 2

    monkeypatch.setattr(mood_meter, "_hash_date", mock_hash)
    assert mood_meter.get_mood(date(1999, 12, 31)) == EXPECTED_EMOJIS[2]
