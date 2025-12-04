import sys
from pathlib import Path

# Add the src directory to sys.path so we can import sanitizer directly
src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

from sanitizer import sanitize_branch

import pytest

@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("My Feature #1!", "my-feature-1"),
        ("  leading and trailing  ", "leading-and-trailing"),
        ("Multiple   Spaces___and---dashes", "multiple-spaces-and-dashes"),
        ("UPPER_case-MIX", "upper-case-mix"),
        ("---already--clean---", "already-clean"),
        ("", ""),
        ("!!!", ""),
    ],
)
def test_sanitize_branch(input_str, expected):
    assert sanitize_branch(input_str) == expected
