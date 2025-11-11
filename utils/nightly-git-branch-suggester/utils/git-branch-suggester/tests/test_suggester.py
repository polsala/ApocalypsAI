import unittest
from git_branch_suggester import generate_branch


class TestGitBranchSuggester(unittest.TestCase):
    def test_basic_sanitization(self):
        self.assertEqual(
            generate_branch("Fix typo in README"),
            "fix-typo-in-readme",
        )

    def test_prefix_and_ticket(self):
        self.assertEqual(
            generate_branch(
                title="Add user avatars",
                prefix="feature",
                ticket="42",
            ),
            "feature-42-add-user-avatars",
        )

    def test_multiple_spaces_and_symbols(self):
        self.assertEqual(
            generate_branch("   Refactor   API!!   endpoints   "),
            "refactor-api-endpoints",
        )

    def test_non_ascii_characters(self):
        # Unicode letters are lower‑cased but non‑ASCII alphanumerics are stripped by the regex.
        self.assertEqual(
            generate_branch("Añadir función de búsqueda"),
            "a-adir-funci-n-de-busqueda",
        )

    def test_prefix_only(self):
        self.assertEqual(
            generate_branch("Update docs", prefix="docs"),
            "docs-update-docs",
        )

    def test_ticket_only(self):
        self.assertEqual(
            generate_branch("Hotfix crash", ticket=99),
            "99-hotfix-crash",
        )

    def test_all_none(self):
        # Title with only symbols should result in an empty string after sanitization.
        self.assertEqual(
            generate_branch("!!!"),
            "",
        )


if __name__ == "__main__":
    unittest.main()
