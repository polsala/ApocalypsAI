import pytest

# Mock rationale: we import the function directly from the utility's source.
from utils.nightly_hex_color_namer.src.color_namer import name_color, _clean_hex


def test_clean_hex_full_length():
    assert _clean_hex("#ff5733") == "ff5733"
    assert _clean_hex("ff5733") == "ff5733"


def test_clean_hex_short_form():
    assert _clean_hex("#abc") == "aabbcc"
    assert _clean_hex("abc") == "aabbcc"


def test_clean_hex_invalid():
    with pytest.raises(ValueError):
        _clean_hex("#12")  # too short
    with pytest.raises(ValueError):
        _clean_hex("#gggggg")  # invalid chars


def test_name_color_known_values():
    # Deterministic mapping based on the algorithm and word lists.
    assert name_color("#000000") == "mystic mist"  # int=0
    # 0xffffff = 16777215 -> adj index 0, noun index 3 (ember)
    assert name_color("#ffffff") == "mystic ember"
    # Random example: #ff5733 -> int=16734003
    # adj = 16734003 % 5 = 3 -> "golden"
    # noun = (16734003 // 5) % 5 = 3346800 % 5 = 0 -> "mist"
    assert name_color("#ff5733") == "golden mist"


def test_name_color_invalid_input():
    with pytest.raises(ValueError):
        name_color("not-a-hex")
    with pytest.raises(ValueError):
        name_color("#12345")  # wrong length
