import pathlib
import sys

# Add the src directory to the import path.
BASE_DIR = pathlib.Path(__file__).resolve().parents[2] / "src"
sys.path.append(str(BASE_DIR))

from scrabble_finder import find_words


def test_find_words_basic():
    # Mock rationale: using a fixed small word list ensures deterministic results.
    letters = "aple"
    expected = [
        "pale",
        "plea",
        "leap",
        "ape",
        "pea",
        "pal",
        "lap",
        "ale",
        "lea",
    ]
    assert find_words(letters) == expected


def test_find_words_min_len():
    # Mock rationale: verify that the min_len filter works correctly.
    letters = "aple"
    # With min_len=4 we should only get the 4‑letter words.
    expected = ["pale", "plea", "leap"]
    assert find_words(letters, min_len=4) == expected
