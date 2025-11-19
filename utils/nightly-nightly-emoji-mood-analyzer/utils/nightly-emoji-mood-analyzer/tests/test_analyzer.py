import json
from pathlib import Path

# Mock rationale: All tests use in‑memory strings; no file I/O beyond temporary fixtures.
# This guarantees deterministic, offline execution.

from utils.nightly_emoji_mood_analyzer.src.analyzer import extract_emojis, most_common_emojis


def test_extract_emojis_simple():
    text = "I love pizza 🍕! It's great 😊😊."
    emojis = extract_emojis(text)
    assert emojis == ["🍕", "😊", "😊"]


def test_most_common_single_winner():
    text = "Happy day 😊😊😊! Pizza 🍕🍕 is good."
    most, counts = most_common_emojis(text)
    assert most == ["😊"]
    assert counts == {"😊": 3}


def test_most_common_tie():
    text = "Thumbs up 👍👍 and thumbs down 👎👎."
    most, counts = most_common_emojis(text)
    # Order is not guaranteed; sort for comparison.
    assert sorted(most) == sorted(["👍", "👎"])
    assert counts == {"👍": 2, "👎": 2}


def test_cli_output(tmp_path: Path, capsys):
    # Create a temporary file with known content.
    sample = "Good morning 🌞! Have a nice day 🌞🌞."
    file_path = tmp_path / "sample.txt"
    file_path.write_text(sample, encoding="utf-8")

    # Import the CLI runner function directly.
    from utils.nightly_emoji_mood_analyzer.src.analyzer import _run_cli

    # Monkey‑patch sys.argv to simulate command‑line invocation.
    import sys
    original_argv = sys.argv
    sys.argv = ["analyzer.py", str(file_path)]
    try:
        _run_cli()
    finally:
        sys.argv = original_argv

    captured = capsys.readouterr().out.strip()
    result = json.loads(captured)
    assert result["most_common"] == ["🌞"]
    assert result["counts"] == {"🌞": 3}
