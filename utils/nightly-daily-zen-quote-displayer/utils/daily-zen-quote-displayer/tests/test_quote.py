import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

# Mock rationale: using a temporary quotes file to avoid filesystem dependency.

# Import the module under test. Adjust sys.path so that the src package is importable.
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import quote  # type: ignore


def write_temp_quotes(tmp_path, data):
    """Helper to write a temporary quotes.json file and monkey‑patch the module constant.
    """
    file_path = tmp_path / "quotes.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")
    # Monkey‑patch the internal path used by the module
    quote._QUOTE_FILE = file_path
    return file_path


def test_load_quotes(tmp_path):
    sample = [{"text": "Test quote", "author": "Tester"}]
    write_temp_quotes(tmp_path, sample)
    loaded = quote.load_quotes()
    assert loaded == sample


def test_pick_quote_deterministic(tmp_path):
    sample = [
        {"text": "First", "author": "A"},
        {"text": "Second", "author": "B"},
        {"text": "Third", "author": "C"},
    ]
    write_temp_quotes(tmp_path, sample)
    quotes = quote.load_quotes()
    # Seed 0 should always pick the same element
    chosen = quote.pick_quote(quotes, seed=0)
    assert chosen == {"text": "Second", "author": "B"}


def test_format_quote_with_author():
    q = {"text": "Stay hungry, stay foolish.", "author": "Steve Jobs"}
    formatted = quote.format_quote(q)
    assert formatted == "\"Stay hungry, stay foolish.\" — Steve Jobs"


def test_format_quote_without_author():
    q = {"text": "Just do it."}
    formatted = quote.format_quote(q)
    assert formatted == "\"Just do it.\""

def test_cli_output(capsys, tmp_path, monkeypatch):
    sample = [{"text": "CLI Test", "author": "CI"}]
    write_temp_quotes(tmp_path, sample)
    # Ensure the module sees the patched path
    monkeypatch.setattr(quote, "_QUOTE_FILE", tmp_path / "quotes.json")
    # Simulate CLI call with a fixed seed
    test_args = ["quote.py", "--seed", "123"]
    monkeypatch.setattr(sys, "argv", test_args)
    quote.main()
    captured = capsys.readouterr()
    assert "CLI Test" in captured.out
