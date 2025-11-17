import pytest
from src.namer import name_color

# ---------------------------------------------------------------------------
# Mock rationale: No external resources are accessed – the palette lives in the
# module itself.  Therefore the tests are fully deterministic and can run
# offline.
# ---------------------------------------------------------------------------

def test_exact_match():
    assert name_color("#ff0000") == "red"
    assert name_color("00ff00") == "lime"
    assert name_color("#0000FF") == "blue"

def test_nearest_match():
    # #ff4500 is "orangered" in the palette, but we also have "orange".
    # The Euclidean distance to "orangered" (ff4500) is 0, so it should win.
    assert name_color("#ff4500") == "orangered"

    # A colour halfway between red (ff0000) and orange (ffa500).
    # The nearest name should be "orange" because it is closer in RGB space.
    assert name_color("#ff2600") == "orange"

def test_invalid_input():
    with pytest.raises(ValueError):
        name_color("not-a-hex")
    with pytest.raises(ValueError):
        name_color("#123")  # too short
    with pytest.raises(ValueError):
        name_color("#gggggg")  # non‑hex characters

def test_case_insensitivity_and_hash_handling():
    assert name_color("ff4500") == "orangered"
    assert name_color("#FF4500") == "orangered"
    assert name_color("#ff4500") == "orangered"
