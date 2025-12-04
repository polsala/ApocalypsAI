# Mock rationale: No external dependencies, deterministic logic.

import os
import sys
import unittest

# Add the src directory to sys.path so we can import emoji_adder
src_dir = os.path.join(os.path.dirname(__file__), "..", "..", "src")
sys.path.append(src_dir)

from emoji_adder import add_emoji

class TestEmojiAdder(unittest.TestCase):
    def test_feat_prefix(self):
        self.assertEqual(add_emoji("feat: add new API"), "🚀 feat: add new API")

    def test_fix_prefix_case_insensitive(self):
        self.assertEqual(add_emoji("FiX: bug fix"), "🐛 FiX: bug fix")

    def test_docs_prefix(self):
        self.assertEqual(add_emoji("docs: update README"), "📚 docs: update README")

    def test_style_prefix(self):
        self.assertEqual(add_emoji("style: format code"), "🎨 style: format code")

    def test_refactor_prefix(self):
        self.assertEqual(add_emoji("refactor: improve performance"), "🔧 refactor: improve performance")

    def test_test_prefix(self):
        self.assertEqual(add_emoji("test: add unit tests"), "🧪 test: add unit tests")

    def test_no_prefix(self):
        self.assertEqual(add_emoji("improve documentation"), "❓ improve documentation")

    def test_leading_trailing_whitespace(self):
        self.assertEqual(add_emoji("   feat: trim spaces   "), "🚀 feat: trim spaces")

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            add_emoji(123)

if __name__ == "__main__":
    unittest.main()
