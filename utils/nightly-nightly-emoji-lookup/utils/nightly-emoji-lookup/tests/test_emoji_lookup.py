import sys
from pathlib import Path

# Ensure the src directory is on the import path
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from src.emoji_lookup import search, main


def test_search_basic_match():
    result = search("smile")
    assert result == ["😄", "😊", "😁"]


def test_search_substring_match():
    # "cat" should also match "cat" keyword, but "at" is a substring of "cat"
    result = search("at")
    assert "🐱" in result  # cat emojis should appear
    assert "🐶" not in result


def test_search_case_insensitivity():
    assert search("HeArT") == ["❤️", "💖", "💘"]


def test_search_no_match_returns_empty():
    assert search("nonexistent") == []


def test_cli_with_argument(monkeypatch, capsys):
    # Simulate calling the CLI with a keyword argument
    monkeypatch.setattr(sys, "argv", ["emoji_lookup", "fire"])
    exit_code = main()
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "🔥 ♨️"


def test_cli_without_argument_reads_stdin(monkeypatch, capsys):
    # Simulate stdin containing two lines
    stdin_data = "party\ncoffee\n"
    monkeypatch.setattr(sys, "stdin", io.StringIO(stdin_data))
    monkeypatch.setattr(sys, "argv", ["emoji_lookup"])
    exit_code = main()
    captured = capsys.readouterr()
    assert exit_code == 0
    # Order is preserved: first party emojis then coffee emojis
    expected = "🥳 🎉 🎊 ☕ 🧋"
    assert captured.out.strip() == expected


def test_cli_no_matches_exits_with_1(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["emoji_lookup", "unknown"])
    exit_code = main()
    assert exit_code == 1

# Mock rationale comments (no external network calls are performed)
# Mock rationale: All tests operate on the in‑memory EMOJI_DB; no I/O or network.
