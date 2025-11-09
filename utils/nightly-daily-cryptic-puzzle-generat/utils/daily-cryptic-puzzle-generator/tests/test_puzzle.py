import importlib.util
import pathlib
from unittest import mock

# Mock rationale: Ensure deterministic selection of the first puzzle.

def _load_module():
    """Load the puzzle module from its source file without importing as a package."""
    module_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "puzzle.py"
    spec = importlib.util.spec_from_file_location("puzzle", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

def test_generate_puzzle_deterministic():
    with mock.patch('random.choice', side_effect=lambda seq: seq[0]):
        puzzle = _load_module()
        clue, answer = puzzle.generate_puzzle()
        assert clue == "Day star (3)"
        assert answer == "SUN"

def test_main_output(capsys):
    with mock.patch('random.choice', side_effect=lambda seq: seq[0]):
        puzzle = _load_module()
        puzzle.main()
        captured = capsys.readouterr()
        expected = "Clue: Day star (3)\nAnswer: SUN\n"
        assert captured.out == expected
