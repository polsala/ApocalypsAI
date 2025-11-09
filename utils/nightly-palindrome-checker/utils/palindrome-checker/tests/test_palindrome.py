import os
import sys
import pytest

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from palindrome import is_palindrome

@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("racecar", True),
        ("RaceCar", True),
        ("A man, a plan, a canal: Panama", True),
        ("No lemon, no melon", True),
        ("Hello, World!", False),
        ("", True),
    ],
)
def test_is_palindrome(input_str, expected):
    assert is_palindrome(input_str) == expected
