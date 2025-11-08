import builtins
import sys
from pathlib import Path

# Mock rationale: we import the module directly from its relative path to avoid package installation.
# This keeps the test self‑contained and offline.

UTILS_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(UTILS_ROOT / "src"))

from convert import convert_time, main


def test_basic_conversion():
    # Convert New York 2025-12-31 23:30 to Tokyo (should be 2025-01-01 13:30)
    result = convert_time("2025-12-31 23:30", "America/New_York", "Asia/Tokyo")
    assert result == "2025-01-01 13:30 (Asia/Tokyo)"


def test_invalid_time_format():
    try:
        convert_time("31-12-2025 23:30", "America/New_York", "Asia/Tokyo")
    except ValueError as e:
        assert "Invalid time format" in str(e)
    else:
        assert False, "Expected ValueError for bad time format"


def test_unknown_timezone():
    try:
        convert_time("2025-12-31 23:30", "Mars/Phobos", "Asia/Tokyo")
    except ValueError as e:
        assert "Unknown source time‑zone" in str(e)
    else:
        assert False, "Expected ValueError for unknown source tz"


def test_cli_success(monkeypatch, capsys):
    # Simulate CLI arguments
    test_args = [
        "--from",
        "America/New_York",
        "--to",
        "Asia/Tokyo",
        "--time",
        "2025-12-31 23:30",
    ]
    monkeypatch.setattr(sys, "argv", ["convert.py"] + test_args)
    exit_code = main()
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "2025-01-01 13:30 (Asia/Tokyo)"


def test_cli_error(monkeypatch, capsys):
    # Missing required argument triggers argparse error (exit code 2)
    monkeypatch.setattr(sys, "argv", ["convert.py", "--from", "America/New_York"])
    try:
        main()
    except SystemExit as e:
        # argparse calls sys.exit with code 2 on error
        assert e.code == 2
    else:
        assert False, "Expected SystemExit from argparse"
