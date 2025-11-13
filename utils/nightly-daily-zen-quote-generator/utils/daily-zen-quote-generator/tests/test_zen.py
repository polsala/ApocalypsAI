import sys
import pathlib
import pytest
from unittest import mock

# Ensure the src directory is on sys.path so we can import the module without package name issues.
src_dir = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_dir))

from zen import get_quote


def test_get_quote_no_theme():
    # Mock rationale: patch random.choice to always return the first element of the provided list.
    with mock.patch("random.choice", side_effect=lambda seq: seq[0]):
        quote = get_quote()
    assert quote == "The journey of a thousand miles begins with one step."


def test_get_quote_with_theme():
    with mock.patch("random.choice", side_effect=lambda seq: seq[0]):
        quote = get_quote(theme="nature")
    assert quote == "Nature does not hurry, yet everything is accomplished."


def test_get_quote_invalid_theme():
    with pytest.raises(ValueError) as excinfo:
        get_quote(theme="unknown")
    assert "No quotes found for theme 'unknown'" in str(excinfo.value)
