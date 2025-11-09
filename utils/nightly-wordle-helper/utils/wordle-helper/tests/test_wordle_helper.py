import builtins
import io
import sys
from typing import List

# Mock rationale: we import the module under test.
from utils.wordle_helper.src.wordle_helper import (
    filter_by_pattern,
    filter_by_exclusions,
    parse_exclusions,
    main,
)


def test_parse_exclusions():
    assert parse_exclusions("") == set()
    assert parse_exclusions("a,b,c") == {"a", "b", "c"}
    assert parse_exclusions("  x , y ,z  ") == {"x", "y", "z"}
    assert parse_exclusions(",,a,,") == {"a"}


def test_filter_by_pattern():
    words = ["caper", "caste", "cater", "caves", "cello"]
    # Pattern with known first and fourth letters.
    result = filter_by_pattern(words, "c??e?")
    assert set(result) == {"caper", "caste", "cater", "caves"}
    # Exact match.
    assert filter_by_pattern(words, "cello") == ["cello"]
    # No matches.
    assert filter_by_pattern(words, "z????") == []


def test_filter_by_exclusions():
    words = ["caper", "caste", "cater", "caves"]
    # Exclude letters a and d.
    result = filter_by_exclusions(words, {"a", "d"})
    # All words contain 'a', so result should be empty.
    assert result == []
    # Exclude a letter not present.
    result = filter_by_exclusions(words, {"z"})
    assert set(result) == set(words)


def test_integration_via_main(capsys: any):
    # Simulate CLI call: pattern c??e?, exclude a,b,d
    # Expected: no matches because all candidate words contain 'a'.
    exit_code = main(["--pattern", "c??e?", "--exclude", "a,b,d"])
    captured = capsys.readouterr()
    assert exit_code == 0
    # No output lines (empty string after stripping).
    assert captured.out.strip() == ""


def test_integration_success_output(capsys: any):
    # Pattern c??e?, exclude only 'z' (which none of the words have).
    exit_code = main(["--pattern", "c??e?", "--exclude", "z"])
    captured = capsys.readouterr()
    assert exit_code == 0
    # Should list the matching words (order as in WORD_LIST).
    expected = "caper\ncaste\ncater\ncaves"
    assert captured.out.strip() == expected
