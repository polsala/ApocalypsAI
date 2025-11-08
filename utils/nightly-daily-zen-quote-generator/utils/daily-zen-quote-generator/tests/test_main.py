import datetime
import sys
from pathlib import Path

# Mock rationale: Import the module from the utils folder without installing the package.
# This keeps the test offline and deterministic.
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from daily_zen_quote.main import _quote_for_date, main

def test_quote_determinism():
    # Known dates and their expected quotes based on the algorithm.
    test_cases = [
        (datetime.date(2025, 11, 8), "The river flows, but the stone remains."),
        (datetime.date(2025, 11, 9), "When the wind stops, the leaves still whisper."),
        (datetime.date(2025, 11, 10), "Silence is the loudest answer."),
        (datetime.date(2000, 1, 1), "The river flows, but the stone remains."),  # epoch start
        (datetime.date(2000, 1, 2), "When the wind stops, the leaves still whisper."),
    ]
    for dt, expected in test_cases:
        assert _quote_for_date(dt) == expected

def test_cli_success(capsys):
    # Mock rationale: Run main() with a valid date argument and capture stdout.
    exit_code = main(["2025-11-08"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "The river flows, but the stone remains."

def test_cli_invalid_date(capsys):
    exit_code = main(["2025-13-01"])  # invalid month
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Invalid date format" in captured.out

def test_cli_missing_argument(capsys):
    exit_code = main([])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Usage:" in captured.out
