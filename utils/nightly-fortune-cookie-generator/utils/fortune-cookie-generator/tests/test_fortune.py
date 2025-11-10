"""
Tests for the Fortune Cookie Generator.
"""

import sys
from unittest import mock

# Mock rationale: Ensure deterministic output by mocking random.choice
# to return a known string, making the test offline and repeatable.

def test_get_fortune_mocked_choice():
    with mock.patch('random.choice', return_value="Mocked fortune"):
        # Import inside the mock context to ensure the patched function is used
        from src.fortune import get_fortune
        assert get_fortune() == "Mocked fortune"


def test_cli_output(capsys):
    # Mock random.choice to return a known string for CLI output
    with mock.patch('random.choice', return_value="CLI fortune"):
        from src.fortune import main
        main()
        captured = capsys.readouterr()
        assert captured.out.strip() == "CLI fortune"
