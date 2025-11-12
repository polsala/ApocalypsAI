import os
import sys
from unittest import mock

# Mock rationale: Ensure deterministic output by mocking random.choice.

def _add_src_to_path():
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    return src_path

def _remove_src_from_path(src_path):
    if src_path in sys.path:
        sys.path.remove(src_path)

def test_get_fortune_deterministic():
    src_path = _add_src_to_path()
    import fortune
    with mock.patch('random.choice', lambda seq: seq[0]):
        assert fortune.get_fortune() == "You will find great success in unexpected places."
    _remove_src_from_path(src_path)

def test_main_prints_fortune(capsys):
    src_path = _add_src_to_path()
    import fortune
    with mock.patch('random.choice', lambda seq: seq[2]):
        fortune.main()
        captured = capsys.readouterr()
        assert captured.out.strip() == "Patience is a virtue; good things come to those who wait."
    _remove_src_from_path(src_path)
