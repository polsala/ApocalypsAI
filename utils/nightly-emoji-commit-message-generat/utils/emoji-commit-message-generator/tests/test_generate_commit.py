import unittest
import importlib.util
import pathlib

def load_module():
    # Resolve the path to the generate_commit.py file relative to this test file.
    file_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "generate_commit.py"
    spec = importlib.util.spec_from_file_location("generate_commit", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    return module

module = load_module()
generate_commit_message = module.generate_commit_message
_find_emoji = module._find_emoji

class TestEmojiCommitMessageGenerator(unittest.TestCase):
    def test_known_keyword(self):
        self.assertEqual(generate_commit_message("add new feature"), "✨ add new feature")
        self.assertEqual(generate_commit_message("Fix critical bug"), "🐛 Fix critical bug")
        self.assertEqual(generate_commit_message("Update documentation"), "📝 Update documentation")
        self.assertEqual(generate_commit_message("security patch applied"), "🔐 security patch applied")

    def test_multiple_keywords_first_match(self):
        # 'refactor' appears before 'test' in the description; should pick refactor's emoji.
        self.assertEqual(generate_commit_message("refactor and test utils"), "🔧 refactor and test utils")

    def test_no_keyword_defaults(self):
        self.assertEqual(generate_commit_message("miscellaneous changes"), "💡 miscellaneous changes")

    def test_find_emoji_direct(self):
        self.assertEqual(_find_emoji("remove obsolete files"), "🗑️")
        self.assertEqual(_find_emoji("unknown words here"), "💡")

if __name__ == "__main__":
    unittest.main()
