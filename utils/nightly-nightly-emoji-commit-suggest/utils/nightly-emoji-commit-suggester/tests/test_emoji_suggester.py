import unittest
import sys
import os

# Add the src directory to the Python path for importing the module
# Mock rationale: This setup allows the test to import the module as if it were installed,
# without needing to modify sys.path globally or install the package. It's self-contained
# and deterministic for the test environment.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import constants and function from the module
from emoji_suggester import (
    suggest_emoji,
    EMOJI_SPARKLES, EMOJI_BUG, EMOJI_BOOKS, EMOJI_ART, EMOJI_RECYCLE,
    EMOJI_LIGHTNING, EMOJI_TEST_TUBE, EMOJI_ROCKET, EMOJI_BROOM, EMOJI_LOCK,
    EMOJI_PACKAGE, EMOJI_REWIND, EMOJI_PARTY_POPPER
)

class TestEmojiSuggester(unittest.TestCase):

    def test_feature_commit(self):
        self.assertEqual(suggest_emoji("feat: Add new user authentication"), [EMOJI_SPARKLES])
        self.assertEqual(suggest_emoji("feature: Implement dark mode"), [EMOJI_SPARKLES])
        self.assertEqual(suggest_emoji("Add: Introduce caching layer"), [EMOJI_SPARKLES])
        self.assertEqual(suggest_emoji("add new feature"), [EMOJI_SPARKLES])

    def test_bug_fix_commit(self):
        self.assertEqual(suggest_emoji("fix(auth): Resolve critical bug"), [EMOJI_BUG])
        self.assertEqual(suggest_emoji("BUG: Fix typo in README"), [EMOJI_BUG])
        self.assertEqual(suggest_emoji("Error: Handle edge case in parser"), [EMOJI_BUG])

    def test_docs_commit(self):
        self.assertEqual(suggest_emoji("docs: Update API documentation"), [EMOJI_BOOKS])
        self.assertEqual(suggest_emoji("Documentation: Add usage examples"), [EMOJI_BOOKS])

    def test_style_commit(self):
        self.assertEqual(suggest_emoji("style: Format code with Black"), [EMOJI_ART])
        self.assertEqual(suggest_emoji("Format: Lint all Python files"), [EMOJI_ART])

    def test_refactor_commit(self):
        self.assertEqual(suggest_emoji("refactor: Extract helper function"), [EMOJI_RECYCLE])
        self.assertEqual(suggest_emoji("Restructure: Move files to new directory"), [EMOJI_RECYCLE])

    def test_performance_commit(self):
        self.assertEqual(suggest_emoji("perf: Optimize database query"), [EMOJI_LIGHTNING])
        self.assertEqual(suggest_emoji("Performance: Improve startup time"), [EMOJI_LIGHTNING])

    def test_test_commit(self):
        self.assertEqual(suggest_emoji("test: Add unit tests for new feature"), [EMOJI_TEST_TUBE])
        self.assertEqual(suggest_emoji("Tests: Cover edge cases"), [EMOJI_TEST_TUBE])

    def test_build_ci_commit(self):
        self.assertEqual(suggest_emoji("build: Update CI configuration"), [EMOJI_ROCKET])
        self.assertEqual(suggest_emoji("CI: Fix broken workflow"), [EMOJI_ROCKET])
        self.assertEqual(suggest_emoji("Workflow: Add new GitHub Action"), [EMOJI_ROCKET])

    def test_chore_misc_commit(self):
        self.assertEqual(suggest_emoji("chore: Clean up temporary files"), [EMOJI_BROOM])
        self.assertEqual(suggest_emoji("Misc: Update .gitignore"), [EMOJI_BROOM])

    def test_security_commit(self):
        self.assertEqual(suggest_emoji("security: Patch XSS vulnerability"), [EMOJI_LOCK])

    def test_dependency_commit(self):
        self.assertEqual(suggest_emoji("dep: Upgrade requests library"), [EMOJI_PACKAGE])
        self.assertEqual(suggest_emoji("Dependencies: Update all packages"), [EMOJI_PACKAGE])

    def test_revert_commit(self):
        self.assertEqual(suggest_emoji("revert: Revert previous commit"), [EMOJI_REWIND])

    def test_initial_commit(self):
        self.assertEqual(suggest_emoji("Initial commit"), [EMOJI_PARTY_POPPER])
        self.assertEqual(suggest_emoji("initial commit for project"), [EMOJI_PARTY_POPPER])

    def test_multiple_matches(self):
        # Order should be deterministic (sorted list of emojis)
        expected_emojis = sorted([EMOJI_BROOM, EMOJI_PACKAGE])
        self.assertEqual(suggest_emoji("chore: Update dependencies and clean up"), expected_emojis)

        expected_emojis_2 = sorted([EMOJI_SPARKLES, EMOJI_TEST_TUBE])
        self.assertEqual(suggest_emoji("feat: Add new feature with tests"), expected_emojis_2)

    def test_no_match(self):
        self.assertEqual(suggest_emoji("Just a random commit message"), [])
        self.assertEqual(suggest_emoji(""), [])
        self.assertEqual(suggest_emoji("Hello world"), [])

    def test_case_insensitivity(self):
        self.assertEqual(suggest_emoji("FEAT: Add something"), [EMOJI_SPARKLES])
        self.assertEqual(suggest_emoji("Fix: A small issue"), [EMOJI_BUG])
        self.assertEqual(suggest_emoji("Docs: Readme update"), [EMOJI_BOOKS])

    def test_keyword_as_substring_no_false_positive(self):
        # With regex word boundaries, 'add' should not match 'ladder' or 'additional'
        self.assertEqual(suggest_emoji("ladder update"), [])
        self.assertEqual(suggest_emoji("additional changes"), [])
        self.assertEqual(suggest_emoji("defeat the purpose"), [])
        self.assertEqual(suggest_emoji("news update"), [])
