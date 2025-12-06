import unittest
from utils.nightly_branch_name_suggester.src.suggester import suggest_branch_name

class TestBranchNameSuggester(unittest.TestCase):
    def test_basic_conversion(self):
        self.assertEqual(
            suggest_branch_name("Add user login"),
            "feat/add-user-login",
        )

    def test_custom_prefix(self):
        self.assertEqual(
            suggest_branch_name("Fix crash on start", prefix="fix"),
            "fix/fix-crash-on-start",
        )

    def test_punctuation_and_spaces(self):
        self.assertEqual(
            suggest_branch_name("Refactor: API, v2!"),
            "feat/refactor-api-v2",
        )

    def test_truncation(self):
        long_title = "A" * 100  # 100 characters, no hyphens
        result = suggest_branch_name(long_title)
        # Should be truncated to MAX_SLUG_LENGTH (50) characters after the prefix and slash
        prefix_len = len("feat/")
        self.assertTrue(len(result) <= prefix_len + 50)
        # Ensure we don't cut in the middle of a hyphen‑separated word when possible
        # Since the slug contains only 'a's, we expect a simple cut
        expected_slug = "a" * 50
        self.assertEqual(result, f"feat/{expected_slug}")

    def test_empty_title_raises(self):
        with self.assertRaises(ValueError):
            suggest_branch_name("")

if __name__ == "__main__":
    unittest.main()
