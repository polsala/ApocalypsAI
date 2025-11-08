# Mock rationale: All tests are pure Python, deterministic, and require no external resources.

import io
import sys
from contextlib import redirect_stdout

# Import the utility under test
from utils.text-similarity-cli.src.similarity import jaccard_similarity, main


def test_jaccard_basic_cases():
    # Identical texts → similarity 1.0
    assert jaccard_similarity("hello world", "hello world") == 1.0

    # Completely disjoint → similarity 0.0
    assert jaccard_similarity("apple", "banana") == 0.0

    # Partial overlap example from README
    a = "The quick brown fox"
    b = "the QUICK fox jumps"
    # Tokens: {the,quick,brown,fox} vs {the,quick,fox,jumps}
    # Intersection = 3, Union = 5 → 0.6
    assert abs(jaccard_similarity(a, b) - 0.6) < 1e-9

    # Both empty strings → defined as 1.0
    assert jaccard_similarity("", "") == 1.0


def test_cli_output_capture():
    # Capture stdout of the CLI entry point
    buf = io.StringIO()
    test_args = ["The quick brown fox", "the QUICK fox jumps"]
    with redirect_stdout(buf):
        exit_code = main(test_args)
    output = buf.getvalue().strip()
    # Expected similarity 0.6 formatted to 4 decimal places
    assert output == "0.6000"
    assert exit_code == 0
