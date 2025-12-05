import builtins
import io
import sys
from src.leetify import leetify, main


def test_basic_mapping():
    assert leetify("abc") == "48("
    assert leetify("XYZ") == "><`/2"
    assert leetify("Hello World!") == "#3ll0 \\/\\/0r1d!"


def test_non_alpha_characters_preserved():
    assert leetify("123!@#") == "123!@#"
    assert leetify("ApocalypsAI is awesome!") == "4p4c4lyp5AI 15 4w350m3!"


def test_cli_argument(monkeypatch, capsys):
    # Simulate passing a CLI argument
    monkeypatch.setattr(sys, "argv", ["leetify", "Test"])
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "7e57"


def test_cli_stdin(monkeypatch, capsys):
    # Simulate no argument, reading from stdin
    monkeypatch.setattr(sys, "argv", ["leetify"])
    fake_stdin = io.StringIO("stdin input")
    monkeypatch.setattr(sys, "stdin", fake_stdin)
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "571n 1npu7"

# Mock rationale: No external services are used; all tests are deterministic and run offline.
