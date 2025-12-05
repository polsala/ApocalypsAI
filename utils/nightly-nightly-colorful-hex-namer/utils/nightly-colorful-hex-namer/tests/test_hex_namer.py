# Mock rationale: Tests are deterministic and use only the local implementation.

import sys
import pathlib

# Ensure the src directory is on the import path.
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import pytest
from src.hex_namer import name_from_hex, _hex_to_rgb


def test_hex_to_rgb():
    assert _hex_to_rgb("#ff0000") == (255, 0, 0)
    assert _hex_to_rgb("00ff00") == (0, 255, 0)
    assert _hex_to_rgb("0000ff") == (0, 0, 255)


def test_name_exact_matches():
    assert name_from_hex("#ff0000") == "Crimson Fury"
    assert name_from_hex("#00ff00") == "Emerald Whisper"
    assert name_from_hex("#0000ff") == "Sapphire Dream"


def test_name_nearest_match():
    # A tealish colour close to Teal Tide (0,128,128)
    assert name_from_hex("#006666") == "Teal Tide"
    # A warm orange close to Orange Ember (255,165,0)
    assert name_from_hex("#ff7f00") == "Orange Ember"


def test_invalid_hex():
    with pytest.raises(ValueError):
        name_from_hex("not-a-hex")
