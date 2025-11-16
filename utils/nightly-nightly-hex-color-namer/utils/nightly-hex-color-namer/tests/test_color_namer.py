import sys
from pathlib import Path

# Add the src directory to the import path so we can import ``color_namer`` directly.
src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

from color_namer import hex_to_name


def test_known_colors():
    assert hex_to_name("#ff0000") == "red"
    assert hex_to_name("#00ff00") == "lime"
    assert hex_to_name("#0000ff") == "blue"
    assert hex_to_name("#ffff00") == "yellow"
    assert hex_to_name("#ffffff") == "white"
    assert hex_to_name("#000000") == "black"


def test_nearest_match():
    # Slightly off pure red should still map to red
    assert hex_to_name("#fe0100") == "red"


def test_invalid_input():
    assert hex_to_name("not-a-color") == "unknown"
    assert hex_to_name("#123abz") == "unknown"
    assert hex_to_name("#123") == "unknown"
