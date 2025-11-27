import unittest
from pathlib import Path
from io import StringIO

# Mock rationale: we import the module directly; no external resources are needed.
from utils.emoji_annotator.src.annotator import annotate_line, process_file

class TestAnnotateLine(unittest.TestCase):
    def test_happy_keyword(self):
        self.assertEqual(annotate_line("I am very happy today\n"), "I am very happy today 😊\n")

    def test_sad_keyword(self):
        self.assertEqual(annotate_line("It is a sad story"), "It is a sad story 😢")

    def test_multiple_keywords_first_match(self):
        # "love" appears before "happy" in the mapping, so love wins.
        self.assertEqual(annotate_line("I love happy moments"), "I love happy moments ❤️")

    def test_no_match(self):
        self.assertEqual(annotate_line("Just a neutral line"), "Just a neutral line 🤔")

class TestProcessFile(unittest.TestCase):
    def setUp(self):
        # Create temporary input file
        self.input_path = Path("temp_input.txt")
        self.output_path = Path("temp_output.txt")
        self.input_path.write_text(
            "I am happy\n"
            "Feeling sad today\n"
            "Nothing special\n",
            encoding="utf-8",
        )

    def tearDown(self):
        # Clean up temporary files
        for p in (self.input_path, self.output_path):
            if p.exists():
                p.unlink()

    def test_process_file(self):
        process_file(str(self.input_path), str(self.output_path))
        expected = (
            "I am happy 😊\n"
            "Feeling sad today 😢\n"
            "Nothing special 🤔\n"
        )
        actual = self.output_path.read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

    def test_missing_input_raises(self):
        missing = Path("does_not_exist.txt")
        with self.assertRaises(FileNotFoundError):
            process_file(str(missing), str(self.output_path))

if __name__ == "__main__":
    unittest.main()
