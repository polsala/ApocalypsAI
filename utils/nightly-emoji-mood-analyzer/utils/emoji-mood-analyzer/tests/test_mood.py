# Mock rationale: All tests are deterministic and run offline.
# They import the module directly from the sibling ``src`` directory.

import sys
from pathlib import Path

# Add the ``src`` directory to ``sys.path`` so ``import mood`` works.
src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_path))

from mood import analyze_mood, main


def test_analyze_mood_cases():
    """Validate that known keywords map to the correct emojis.

    The first matching keyword wins; if none match, the neutral face is
    returned. This test covers happy, sad, angry, excited, love, neutral, and
    a multi‑keyword sentence where the earlier keyword should be chosen.
    """
    cases = [
        ("I am happy", "😊"),
        ("Feeling sad about the news", "😢"),
        ("He was angry and mad", "😠"),
        ("What a thrilling adventure!", "🤩"),
        ("I love this!", "❤️"),
        ("Just a regular day", "😐"),
        ("Confused and bored", "🤔"),  # first match is "confused"
    ]
    for text, expected in cases:
        assert analyze_mood(text) == expected


def test_cli(monkeypatch, capsys):
    """Run the CLI ``main`` function with mocked ``sys.argv``.

    The test ensures the script exits with code ``0`` and prints the expected
    emoji to stdout. No external processes are spawned – everything stays in‑
    process.
    """
    # Mock command‑line arguments: script name + words
    monkeypatch.setattr(sys, "argv", ["mood.py", "I", "am", "excited"])
    exit_code = main()
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "🤩"
