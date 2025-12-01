import unittest
import pathlib
import sys

# Adjust sys.path so the src module can be imported without installing the package.
# Mock rationale: this manipulation is deterministic and offline.
CURRENT_DIR = pathlib.Path(__file__).resolve().parent
SRC_DIR = CURRENT_DIR.parent / "src"
sys.path.append(str(SRC_DIR))

from annotator import annotate

class TestEmojiAnnotator(unittest.TestCase):
    def test_single_happy(self):
        self.assertEqual(annotate("I am happy"), "I am happy 😊")

    def test_multiple_sentiments(self):
        self.assertEqual(
            annotate("happy sad angry"),
            "happy 😊 sad 😢 angry 😠",
        )

    def test_no_sentiment(self):
        self.assertEqual(
            annotate("just a neutral sentence"),
            "just a neutral sentence",
        )

    def test_case_insensitivity(self):
        self.assertEqual(
            annotate("I feel HAPPY and SAD"),
            "I feel HAPPY 😊 and SAD 😢",
        )

    def test_preserve_whitespace(self):
        self.assertEqual(
            annotate("happy   sad"),
            "happy 😊   sad 😢",
        )

if __name__ == "__main__":
    unittest.main()
