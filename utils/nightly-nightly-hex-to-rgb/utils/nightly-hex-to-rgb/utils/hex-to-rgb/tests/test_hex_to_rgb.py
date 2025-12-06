import importlib.util
import pathlib
import pytest


def _load_module():
    """Load the hex_to_rgb module without requiring package imports.
    # Mock rationale: deterministic, offline loading of local source file.
    """
    module_path = pathlib.Path(__file__).resolve().parents[2] / "src" / "hex_to_rgb.py"
    spec = importlib.util.spec_from_file_location("hex_to_rgb", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

hex_mod = _load_module()
hex_to_rgb = hex_mod.hex_to_rgb
_clean_hex = hex_mod._clean_hex

@pytest.mark.parametrize(
    "hex_input,expected",
    [
        ("#ffffff", (255, 255, 255)),
        ("000000", (0, 0, 0)),
        ("#ff00aa", (255, 0, 170)),
        ("123abc", (18, 58, 188)),
    ],
)
def test_hex_to_rgb_valid(hex_input, expected):
    assert hex_to_rgb(hex_input) == expected

@pytest.mark.parametrize(
    "bad_input",
    [
        "#fff",      # too short
        "gggggg",    # non‑hex characters
        "#12345g",   # invalid character at end
        "",          # empty string
        "   ",       # whitespace only
    ],
)
def test_hex_to_rgb_invalid(bad_input):
    with pytest.raises(ValueError):
        hex_to_rgb(bad_input)

def test_clean_hex_strips_hash_and_whitespace():
    assert _clean_hex("  #AbCdEf  ") == "abcdef"
