import unittest
from src.branch_namer import suggest_branch_name

class TestBranchNamer(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(
            suggest_branch_name("Add user login feature"),
            "add-user-login-feature"
        )

    def test_stopwords_and_punctuation(self):
        self.assertEqual(
            suggest_branch_name("Fix the bug, and improve UI!"),
            "fix-bug-improve-ui"
        )

    def test_long_title_truncation(self):
        long_title = "Implement a very long feature name that exceeds the typical fifty character limit for branch names"
        result = suggest_branch_name(long_title)
        # Ensure length <= 50 and no trailing hyphen
        self.assertTrue(len(result) <= 50)
        self.assertFalse(result.endswith("-"))
        # Expected prefix (first part of the slug before truncation)
        self.assertTrue(result.startswith("implement-very-long-feature-name-that-exceeds"))

    def test_non_ascii(self):
        # Non‑ASCII characters are stripped out by the regex
        self.assertEqual(
            suggest_branch_name("Añadir función de búsqueda"),
            "adir-funcion-de-busqueda"
        )

if __name__ == "__main__":
    unittest.main()
