import json
import os
import tempfile
from pathlib import Path

# Mock rationale: The tests operate entirely on temporary files and in‑memory data, ensuring
# they are deterministic, offline, and have no external side‑effects.

from env_var_validator import validator


def write_env(content: str) -> str:
    """Create a temporary .env file with the given content and return its path."""
    fd, path = tempfile.mkstemp(text=True)
    os.write(fd, content.encode())
    os.close(fd)
    return path


def test_validate_all_present():
    env_content = """
    # Sample .env
    DATABASE_URL=postgres://localhost/db
    API_KEY=secret123
    DEBUG=True
    """
    env_path = write_env(env_content)
    required = ["DATABASE_URL", "API_KEY", "DEBUG"]
    missing = validator.validate(env_path, required)
    assert missing == []
    os.remove(env_path)


def test_validate_some_missing():
    env_content = """
    DATABASE_URL=postgres://localhost/db
    DEBUG=False
    """
    env_path = write_env(env_content)
    required = ["DATABASE_URL", "API_KEY", "DEBUG"]
    missing = validator.validate(env_path, required)
    assert missing == ["API_KEY"]
    os.remove(env_path)


def test_cli_success(monkeypatch, capsys):
    env_content = """
    FOO=bar
    BAZ=qux
    """
    env_path = write_env(env_content)
    # Simulate command‑line arguments
    monkeypatch.setattr('sys.argv', [
        'validator.py',
        '--env-file', env_path,
        '--required', 'FOO,BAZ'
    ])
    exit_code = validator.main()
    captured = capsys.readouterr()
    assert exit_code == 0
    result = json.loads(captured.out.strip())
    assert result == {"missing": []}
    os.remove(env_path)


def test_cli_missing(monkeypatch, capsys):
    env_content = """
    FOO=bar
    """
    env_path = write_env(env_content)
    monkeypatch.setattr('sys.argv', [
        'validator.py',
        '--env-file', env_path,
        '--required', 'FOO,BAZ'
    ])
    exit_code = validator.main()
    captured = capsys.readouterr()
    assert exit_code == 1
    result = json.loads(captured.out.strip())
    assert result == {"missing": ["BAZ"]}
    os.remove(env_path)


def test_cli_file_not_found(monkeypatch, capsys):
    # Provide a non‑existent path
    monkeypatch.setattr('sys.argv', [
        'validator.py',
        '--env-file', '/nonexistent/.env',
        '--required', 'FOO'
    ])
    exit_code = validator.main()
    captured = capsys.readouterr()
    assert exit_code == 2
    assert "Env file not found" in captured.err
