import builtins
import io
import sys
from pathlib import Path

# Mock rationale: No external resources are accessed; we only need to import the module under test.
from utils.nightly_emoji_mood_analyzer.src.analyzer import analyze_mood, main


def test_analyze_happy():
    text = "Great job! 😊😊 😄"
    assert analyze_mood(text) == "happy"


def test_analyze_sad():
    text = "Feeling down 😢😞"
    assert analyze_mood(text) == "sad"


def test_analyze_angry():
    text = "That bug broke everything! 😡"
    assert analyze_mood(text) == "angry"


def test_analyze_neutral_no_emojis():
    text = "Just a plain sentence without any emojis."
    assert analyze_mood(text) == "neutral"


def test_analyze_neutral_tie():
    # Equal number of happy and sad emojis → ambiguous → neutral
    text = "Mixed feelings 😊 😢"
    assert analyze_mood(text) == "neutral"


def test_cli_direct_text(capsys):
    # Simulate CLI call with raw text (no file flag)
    test_argv = ["script_name", "I love this! 😄"]
    sys.argv = test_argv
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "happy"


def test_cli_file_input(tmp_path: Path, capsys):
    # Create a temporary file containing sad emojis
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Oops, something went wrong 😢", encoding="utf-8")
    test_argv = ["script_name", str(file_path), "--file"]
    sys.argv = test_argv
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "sad"
