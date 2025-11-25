import unittest
from nightly_emoji_annotator import annotate


class TestEmojiAnnotator(unittest.TestCase):
    def test_single_keyword(self):
        self.assertEqual(annotate("I am happy"), "I am happy 😊")
        self.assertEqual(annotate("Fire!"), "Fire! 🔥")

    def test_multiple_keywords(self):
        text = "The build succeeded but there is a warning"
        expected = "The build succeeded ✅ but there is a warning ⚠️"
        self.assertEqual(annotate(text), expected)

    def test_case_insensitivity(self) -> None:
        self.assertEqual(annotate("I love LOVE LoVe"), "I love ❤️ LOVE ❤️ LoVe ❤️")

    def test_no_keywords(self) -> None:
        self.assertEqual(annotate("Just a plain sentence."), "Just a plain sentence.")

    def test_overlapping_keywords(self) -> None:
        # "bug" should be annotated, but "debug" contains the substring "bug" –
        # our regex matches whole words only, so only "bug" gets an emoji.
        self.assertEqual(annotate("debug bug"), "debug bug 🐛")

    # Mock rationale: No external services are used, so we don't need network mocks.
    # The tests are fully deterministic and run offline.


if __name__ == "__main__":
    unittest.main()
