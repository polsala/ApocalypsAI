import unittest
import tempfile
from pathlib import Path

# Import the module under test
from src.annotator import annotate_file, annotate_lines

class TestEmojiAnnotator(unittest.TestCase):
    def test_annotate_lines_basic(self):
        input_lines = [
            "Build started\n",
            "Compilation success\n",
            "Warning: deprecated API\n",
            "Tests failed\n",
            "All done"
        ]
        expected = [
            "Build started\n",
            "Compilation success 🎉\n",
            "Warning: deprecated API ⚠️\n",
            "Tests failed 😱\n",
            "All done"
        ]
        self.assertEqual(annotate_lines(input_lines), expected)

    def test_annotate_file_end_to_end(self):
        # Mock rationale: using temporary files ensures no filesystem side‑effects.
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.txt"
            output_path = Path(tmpdir) / "output.txt"
            input_content = "first line\nerror encountered\nsecond line\n"
            input_path.write_text(input_content, encoding="utf-8")

            # Run the annotator
            annotate_file(input_path, output_path)

            # Verify output
            expected_output = "first line\nerror encountered 😱\nsecond line\n"
            self.assertEqual(output_path.read_text(encoding="utf-8"), expected_output)

    def test_no_matching_keyword(self):
        self.assertEqual(annotate_lines(["Just a regular line\n"]), ["Just a regular line\n"])

    def test_case_insensitivity(self):
        self.assertEqual(
            annotate_lines(["WARNING: low disk space\n"]),
            ["WARNING: low disk space ⚠️\n"]
        )

if __name__ == "__main__":
    unittest.main()
