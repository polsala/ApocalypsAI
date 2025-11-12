import unittest
import importlib.util
import pathlib
import sys
from unittest import mock


def load_analyzer_module():
    """Load the analyzer module from the source file without relying on package imports.
    This keeps the test self‑contained and works even though the utility folder name contains a hyphen.
    """
    base_dir = pathlib.Path(__file__).resolve().parents[2]
    file_path = base_dir / "src" / "analyzer.py"
    spec = importlib.util.spec_from_file_location("analyzer", file_path)
    module = importlib.util.module_from_spec(spec)
    # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return module


class TestEmojiMoodAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.analyzer = load_analyzer_module()
        cls.analyze_mood = cls.analyzer.analyze_mood

    def test_positive(self):
        self.assertEqual(self.analyze_mood("I love sunny days and great coffee!"), "😊")

    def test_negative(self):
        self.assertEqual(self.analyze_mood("I hate rainy mornings, they are terrible."), "😞")

    def test_neutral_equal(self):
        self.assertEqual(self.analyze_mood("I love and hate this."), "😐")

    def test_neutral_word(self):
        self.assertEqual(self.analyze_mood("It was okay, just fine."), "😐")

    def test_unknown(self):
        self.assertEqual(self.analyze_mood("xyzzy plugh"), "🤔")

    def test_cli(self):
        # Mock sys.argv and capture print output for the CLI entry point.
        with mock.patch.object(sys, "argv", ["analyzer.py", "I am happy"]):
            with mock.patch("builtins.print") as mock_print:
                self.analyzer._cli()
                mock_print.assert_called_once_with("😊")
        # Mock rationale: we replace sys.argv and capture print to avoid real I/O.

if __name__ == "__main__":
    unittest.main()
