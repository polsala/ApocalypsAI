import builtins
import sys
from unittest import mock

# Mock rationale: Ensure deterministic output by forcing random.choice to return the first compliment.
# This avoids flaky tests and keeps them offline.

def test_cli_output(monkeypatch, capsys):
    # Patch random.choice to always return the first element
    with mock.patch('random.choice', lambda seq: seq[0]):
        # Import the CLI entrypoint lazily to apply the mock before execution
        from random_compliment.cli import main
        exit_code = main([])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "You are a coding wizard!"
