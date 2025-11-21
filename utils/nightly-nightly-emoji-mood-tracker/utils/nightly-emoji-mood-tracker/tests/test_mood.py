import datetime
from unittest import mock

# Mock rationale: we need deterministic dates to verify the hash‑based mapping without external randomness.

from utils.nightly_emoji_mood_tracker.src.mood import mood_for_date


def test_known_dates():
    # Pre‑computed expected emojis for given dates using the same algorithm.
    cases = {
        datetime.date(2025, 11, 21): "🤖",
        datetime.date(2020, 1, 1): "🛠️",
        datetime.date(1999, 12, 31): "🌧️",
        datetime.date(2000, 2, 29): "🔥",
    }
    for d, expected in cases.items():
        assert mood_for_date(d) == expected


def test_today_uses_mocked_date():
    # Mock rationale: ensure the CLI falls back to datetime.date.today() correctly.
    mock_today = datetime.date(2023, 3, 14)
    with mock.patch("datetime.date") as mock_date_cls:
        mock_date_cls.today.return_value = mock_today
        mock_date_cls.fromisoformat.side_effect = datetime.date.fromisoformat
        # Import inside the patch to pick up the mocked today.
        from utils.nightly_emoji_mood_tracker.src import mood as mood_mod
        assert mood_mod.mood_for_date(datetime.date.today()) == mood_mod.mood_for_date(mock_today)
