import sys
import pathlib

# Add the src directory to sys.path so the module can be imported
src_path = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

from emoji_clock import time_to_emoji

def test_midnight():
    assert time_to_emoji(0, 0) == "🕛"

def test_noon():
    assert time_to_emoji(12, 0) == "🕛"

def test_afternoon():
    assert time_to_emoji(13, 0) == "🕐"

def test_evening_half():
    assert time_to_emoji(23, 45) == "🕦"

def test_exact_half():
    assert time_to_emoji(9, 30) == "🕤"

def test_round_down():
    assert time_to_emoji(15, 29) == "🕒"

def test_round_up():
    assert time_to_emoji(15, 30) == "🕞"
