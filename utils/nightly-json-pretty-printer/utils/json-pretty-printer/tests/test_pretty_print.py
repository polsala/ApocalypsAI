import io
import sys
from pathlib import Path
from unittest import mock

# Mock rationale: we avoid real file I/O and network; all data is in‑memory.

# Import the module under test
from utils.json_pretty_printer.src.pretty_print import _format_json, _load_json, main


def test_format_json_without_color():
    data = {"b": 2, "a": [1, 2, 3], "c": {"z": None, "y": True}}
    expected = (
        "{\n"
        "  \"a\": [\n"
        "    1,\n"
        "    2,\n"
        "    3\n"
        "  ],\n"
        "  \"b\": 2,\n"
        "  \"c\": {\n"
        "    \"y\": true,\n"
        "    \"z\": null\n"
        "  }\n"
        "}"
    )
    assert _format_json(data, indent=2, color=False) == expected


def test_format_json_with_color(monkeypatch):
    # The exact ANSI codes are part of the implementation; we verify that they appear.
    data = {"key": "value", "num": 42, "flag": False, "none": None}
    result = _format_json(data, indent=2, color=True)
    assert "\033[94m\"key\"\033[0m" in result  # colored key
    assert "\033[92m\"value\"\033[0m" in result  # colored string
    assert "\033[93m42\033[0m" in result  # colored number
    assert "\033[95mFalse\033[0m" in result  # colored bool
    assert "\033[90mnull\033[0m" in result  # colored null


def test_load_json_from_file(tmp_path: Path):
    json_content = "{\"hello\": \"world\"}"
    file = tmp_path / "sample.json"
    file.write_text(json_content, encoding="utf-8")
    result = _load_json(str(file))
    assert result == {"hello": "world"}


def test_load_json_from_stdin(monkeypatch):
    json_content = "[1, 2, 3]"
    mock_stdin = io.StringIO(json_content)
    monkeypatch.setattr(sys, "stdin", mock_stdin)
    result = _load_json("-")
    assert result == [1, 2, 3]


def test_main_successful_print(monkeypatch, capsys):
    # Prepare a temporary JSON file
    json_data = "{\"z\": 0, \"a\": 1}"
    mock_file = mock.mock_open(read_data=json_data)
    monkeypatch.setattr('builtins.open', mock_file)
    # Mock sys.argv
    monkeypatch.setattr(sys, "argv", ["pretty_print.py", "dummy.json"])
    # Run main
    main()
    captured = capsys.readouterr()
    # Expected pretty output (sorted keys a, z)
    expected_output = "{\n  \"a\": 1,\n  \"z\": 0\n}\n"
    assert captured.out == expected_output


def test_main_invalid_json(monkeypatch, capsys):
    mock_file = mock.mock_open(read_data="{invalid json}")
    monkeypatch.setattr('builtins.open', mock_file)
    monkeypatch.setattr(sys, "argv", ["pretty_print.py", "bad.json"])
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Invalid JSON" in captured.err
