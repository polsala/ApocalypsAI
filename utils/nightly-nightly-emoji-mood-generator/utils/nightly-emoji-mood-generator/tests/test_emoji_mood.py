import datetime
from src.emoji_mood import get_mood, main


def test_get_mood_index(monkeypatch):
    # Mock rationale: ensure deterministic index selection.
    def fake_hash(_):
        return 7  # selects EMOJIS[7] = "😡"
    monkeypatch.setattr('src.emoji_mood._hash_date', fake_hash)
    assert get_mood(datetime.date(2022, 1, 1)) == "😡"


def test_cli_invalid_date(capsys):
    # Mock rationale: verify error handling for bad date format.
    exit_code = main(["not-a-date"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error: date must be in YYYY-MM-DD format" in captured.err
