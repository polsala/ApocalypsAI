import unittest
import sys
import os

# Mock rationale: We need to test the `suggest_emoji` function in isolation
# without actually running the script via `sys.argv` or printing to stdout.
# We directly import the function for unit testing.
# To ensure the test environment is clean, we temporarily modify sys.path
# to allow direct import from the 'src' directory.

# Add the src directory to the Python path for direct import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from emoji_suggester import suggest_emoji, EMOJI_MAP
sys.path.pop(0) # Clean up sys.path

class TestEmojiSuggester(unittest.TestCase):

    def test_feature_commit(self):
        self.assertEqual(suggest_emoji("feat: Add new user authentication"), "✨")
        self.assertEqual(suggest_emoji("feature: Implement dark mode"), "✨")
        self.assertEqual(suggest_emoji("add: Initial setup for database"), "✨")
        self.assertEqual(suggest_emoji("New component for dashboard"), "✨")

    def test_bug_fix_commit(self):
        self.assertEqual(suggest_emoji("fix: Resolve critical bug in payment processing"), "🐛")
        self.assertEqual(suggest_emoji("bug: UI glitch on mobile view"), "🐛")
        self.assertEqual(suggest_emoji("patch: Security vulnerability"), "🐛")

    def test_docs_commit(self):
        self.assertEqual(suggest_emoji("docs: Update README with new usage instructions"), "📚")
        self.assertEqual(suggest_emoji("doc: Add API documentation"), "📚")
        self.assertEqual(suggest_emoji("documentation: Fix typos"), "📚")

    def test_refactor_commit(self):
        self.assertEqual(suggest_emoji("refactor: Clean up old utility functions"), "♻️")
        self.assertEqual(suggest_emoji("Refactor: Improve code readability"), "♻️")

    def test_test_commit(self):
        self.assertEqual(suggest_emoji("test: Add unit tests for service layer"), "🧪")
        self.assertEqual(suggest_emoji("tests: Cover edge cases"), "🧪")

    def test_chore_commit(self):
        self.assertEqual(suggest_emoji("chore: Update dependencies"), "⚙️")
        self.assertEqual(suggest_emoji("config: Adjust CI/CD pipeline"), "⚙️")

    def test_style_commit(self):
        self.assertEqual(suggest_emoji("style: Format code with Black"), "🎨")
        self.assertEqual(suggest_emoji("format: Lint all Python files"), "🎨")

    def test_performance_commit(self):
        self.assertEqual(suggest_emoji("perf: Optimize database queries"), "⚡")
        self.assertEqual(suggest_emoji("performance: Reduce load times"), "⚡")

    def test_security_commit(self):
        self.assertEqual(suggest_emoji("security: Upgrade vulnerable package"), "🔒")

    def test_dependency_commit(self):
        self.assertEqual(suggest_emoji("dep: Update requests to latest version"), "📦")
        self.assertEqual(suggest_emoji("deps: Remove unused libraries"), "📦")

    def test_remove_commit(self):
        self.assertEqual(suggest_emoji("remove: Deprecated feature X"), "🗑️")
        self.assertEqual(suggest_emoji("delete: Old migration files"), "🗑️")

    def test_initial_commit(self):
        self.assertEqual(suggest_emoji("initial commit"), "🎉")
        self.assertEqual(suggest_emoji("init project"), "🎉")

    def test_release_commit(self):
        self.assertEqual(suggest_emoji("release: v1.0.0"), "🚀")
        self.assertEqual(suggest_emoji("deploy to production"), "🚀")

    def test_hotfix_commit(self):
        self.assertEqual(suggest_emoji("hotfix: Critical production issue"), "🚑")

    def test_merge_commit(self):
        self.assertEqual(suggest_emoji("Merge branch 'dev' into 'main'"), "🔀")

    def test_wip_commit(self):
        self.assertEqual(suggest_emoji("wip: Working on new feature"), "🚧")

    def test_breaking_commit(self):
        self.assertEqual(suggest_emoji("breaking change: API endpoint moved"), "💥")

    def test_data_commit(self):
        self.assertEqual(suggest_emoji("data: Update dataset for analysis"), "📊")

    def test_db_commit(self):
        self.assertEqual(suggest_emoji("db: Add new table for users"), "🗄️")

    def test_ux_commit(self):
        self.assertEqual(suggest_emoji("ux: Improve user onboarding flow"), "💡")
        self.assertEqual(suggest_emoji("ui: Redesign login page"), "💡")

    def test_accessibility_commit(self):
        self.assertEqual(suggest_emoji("accessibility: Add alt text to images"), "♿")
        self.assertEqual(suggest_emoji("a11y: Fix keyboard navigation"), "♿")

    def test_no_match(self):
        self.assertEqual(suggest_emoji("This is a generic commit message"), "")
        self.assertEqual(suggest_emoji("No keywords here"), "")
        self.assertEqual(suggest_emoji(""), "")

    def test_case_insensitivity(self):
        self.assertEqual(suggest_emoji("Feat: A new thing"), "✨")
        self.assertEqual(suggest_emoji("FIX: Another bug"), "🐛")
        self.assertEqual(suggest_emoji("Docs: Some updates"), "📚")

    def test_priority_of_prefix_match(self):
        # Ensure "fix:" takes precedence over "add" if both are present
        self.assertEqual(suggest_emoji("fix: Add a new feature and fix a bug"), "🐛")
        # Ensure "feat:" takes precedence over "fix" if it's the prefix
        self.assertEqual(suggest_emoji("feat: Fix a bug and add a feature"), "✨")
        # Test a case where a keyword is in the middle but a prefix exists
        self.assertEqual(suggest_emoji("chore: Update dependencies and fix a bug"), "⚙️")

    def test_multiple_keywords_in_message(self):
        # Should return the first one found based on the order in EMOJI_MAP
        # EMOJI_MAP is ordered, so 'feat' comes before 'test' in the map
        self.assertEqual(suggest_emoji("Add a new feature and test it"), "✨")
        # If 'test' comes before 'feat' in the message, but 'feat' is a prefix
        self.assertEqual(suggest_emoji("test: Add a new feature"), "🧪")
        # If 'feat' is a prefix, it should win
        self.assertEqual(suggest_emoji("feat: Add a new feature and test it"), "✨")
        # If no prefix, it should find the first keyword in the map (e.g., 'fix' before 'add')
        self.assertEqual(suggest_emoji("This commit fixes a bug and adds a feature"), "🐛")

    def test_emoji_map_completeness(self):
        # This is a meta-test to ensure the EMOJI_MAP is not empty and has a reasonable size.
        self.assertGreater(len(EMOJI_MAP), 5, "EMOJI_MAP should contain a good number of entries")

if __name__ == '__main__':
    unittest.main()
