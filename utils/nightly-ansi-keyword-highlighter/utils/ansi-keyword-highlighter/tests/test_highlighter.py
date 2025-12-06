import pytest
from src.highlighter import highlight


def test_highlight_basic():
    input_text = "Error: file missing. Warning: low memory. Info: all good."
    expected = (
        "\x1b[31mError\x1b[0m: file missing. "
        "\x1b[33mWarning\x1b[0m: low memory. "
        "\x1b[32mInfo\x1b[0m: all good."
    )
    assert highlight(input_text) == expected


def test_highlight_case_insensitivity():
    input_text = "error ERROR ErRoR warning WARNING info INFO"
    expected = (
        "\x1b[31merror\x1b[0m \x1b[31mERROR\x1b[0m \x1b[31mErRoR\x1b[0m "
        "\x1b[33mwarning\x1b[0m \x1b[33mWARNING\x1b[0m "
        "\x1b[32minfo\x1b[0m \x1b[32mINFO\x1b[0m"
    )
    assert highlight(input_text) == expected


def test_highlight_no_keywords():
    # Mock rationale: ensure unchanged text passes through unchanged.
    input_text = "All systems operational."
    assert highlight(input_text) == input_text
