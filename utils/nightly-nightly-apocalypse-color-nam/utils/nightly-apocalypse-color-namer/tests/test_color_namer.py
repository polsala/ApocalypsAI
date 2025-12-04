import pytest

# Import the function from the utility package.
from utils.nightly_apocalypse_color_namer.src.color_namer import name_color

# ---------------------------------------------------------------------------
# Mock rationale: The tests are fully deterministic and do not require any
# external resources. They simply verify that the deterministic algorithm
# produces the expected output for known inputs.
# ---------------------------------------------------------------------------

def test_known_hex_values():
    # "ff0000" -> Radiant Wasteland (see algorithm explanation)
    assert name_color("#ff0000") == "Radiant Wasteland"
    # "123abc" -> Toxic Ruin (computed manually)
    assert name_color("#123abc") == "Toxic Ruin"
    # Upper‑case input should be handled correctly.
    assert name_color("FF5733") == "Radiant Wasteland"


def test_invalid_hex_raises():
    with pytest.raises(ValueError):
        name_color("#gggggg")  # Invalid hex characters
    with pytest.raises(ValueError):
        name_color("12345")    # Too short
    with pytest.raises(ValueError):
        name_color("#1234567")  # Too long
    with pytest.raises(ValueError):
        name_color(123)  # Not a string
