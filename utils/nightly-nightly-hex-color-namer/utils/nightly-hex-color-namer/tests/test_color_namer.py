import pytest

# Import the function from the utility package. The relative import works because the tests are run
# with the repository root on ``sys.path``.
from utils.nightly-hex-color-namer.src.color_namer import name_color, _normalize_hex


def test_normalize_hex_valid_cases():
    assert _normalize_hex("#FF4500") == "ff4500"
    assert _normalize_hex("ff4500") == "ff4500"
    assert _normalize_hex("  #AaBbCc  ") == "aabbcc"


def test_normalize_hex_invalid_cases():
    # Mock rationale: we deliberately test a handful of malformed inputs to ensure deterministic validation.
    with pytest.raises(ValueError):
        _normalize_hex("#123")  # Too short
    with pytest.raises(ValueError):
        _normalize_hex("GGHHII")  # Non‑hex characters
    with pytest.raises(ValueError):
        _normalize_hex("#1234567")  # Too long
    with pytest.raises(ValueError):
        _normalize_hex("")  # Empty string


def test_known_color_mapping():
    # Known mapping should return the exact whimsical name.
    assert name_color("#ff4500") == "Molten Ember"
    assert name_color("ff0000") == "Crimson Cataclysm"
    assert name_color("#00FF00") == "Toxic Verdure"


def test_unknown_color_fallback():
    # Any hex not present in the map should fall back to the default name.
    assert name_color("#123456") == "Mysterious Void"
    assert name_color("abcdef") == "Mysterious Void"


def test_case_insensitivity_and_whitespace():
    # The function should be robust to case and surrounding whitespace.
    assert name_color("  #FF4500  ") == "Molten Ember"
    assert name_color("ff4500") == "Molten Ember"
    assert name_color("FF4500") == "Molten Ember"
