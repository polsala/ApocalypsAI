"""Tests for the mood‑emoji‑mapper utility.

All tests are deterministic and run offline.  No external services are
required.  The ``# Mock rationale:`` comments explain why no real network
interaction is needed.
"""

import sys
from pathlib import Path

# Ensure the src package is importable when running tests from the repository root.
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from src.mapper import map_mood_to_emoji


def test_happy_keywords():
    assert map_mood_to_emoji("I am so happy today!") == "😄"
    assert map_mood_to_emoji("Feeling joyful and bright") == "😂"  # 'joy' matches before 'happy'


def test_excited_and_love():
    assert map_mood_to_emoji("Excited about the launch 🚀") == "🚀"
    assert map_mood_to_emoji("I love this new feature") == "❤️"


def test_negative_moods():
    assert map_mood_to_emoji("I'm sad and tired") == "😢"  # 'sad' appears before 'tired'
    assert map_mood_to_emoji("Just a bit tired after the marathon") == "😴"


def test_no_match_returns_default():
    # No keyword from the map is present → default neutral face.
    assert map_mood_to_emoji("Just another day") == "😐"


def test_cli_output(capsys, monkeypatch):
    # Simulate command‑line execution of the module.
    test_args = ["prog", "I feel excited about the new release"]
    monkeypatch.setattr(sys, "argv", test_args)
    # Import the module as a script to trigger its __main__ block.
    # # Mock rationale: we are directly invoking main() without spawning a subprocess.
    from src import mapper as script
    script.main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "🚀"
