import sys
import tempfile
from pathlib import Path
from unittest import mock

# Mock rationale: we replace sys.argv to simulate CLI invocation without spawning a subprocess.

from utils.daily_emoji_mood_tracker.src.mood_tracker import main


def write_sample_log(content: str) -> Path:
    tmp = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")
    tmp.write(content)
    tmp.flush()
    tmp.close()
    return Path(tmp.name)


def test_full_flow_success(capfd):
    sample = """
    2025-11-01: happy
    2025-11-02: sad
    2025-11-03: excited
    2025-11-04: happy
    2025-11-05: love
    2025-11-06: happy
    """
    log_path = write_sample_log(sample)
    test_argv = ["prog", str(log_path)]
    with mock.patch.object(sys, "argv", test_argv):
        exit_code = main()
    captured = capfd.readouterr()
    # Expected histogram order: happy (3), excited (1), love (1), sad (1)
    assert exit_code == 0
    assert "😄 3" in captured.out
    assert "🤩 1" in captured.out
    assert "❤️ 1" in captured.out
    assert "😢 1" in captured.out


def test_no_moods_found(capfd):
    sample = """
    2025-11-01: unknownmood
    just some random text
    """
    log_path = write_sample_log(sample)
    test_argv = ["prog", str(log_path)]
    with mock.patch.object(sys, "argv", test_argv):
        exit_code = main()
    captured = capfd.readouterr()
    assert exit_code == 0
    assert "No recognizable moods found" in captured.out


def test_file_not_found(capfd):
    test_argv = ["prog", "nonexistent.txt"]
    with mock.patch.object(sys, "argv", test_argv):
        exit_code = main()
    captured = capfd.readouterr()
    assert exit_code == 1
    assert "Error: file not found" in captured.err
