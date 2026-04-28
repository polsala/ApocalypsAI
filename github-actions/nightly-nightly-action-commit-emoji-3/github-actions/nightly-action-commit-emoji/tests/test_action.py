import unittest, pathlib, os

class TestCommitEmojiAction(unittest.TestCase):
    def test_action_yaml_contains_required_fields(self):
        # Locate the action.yml relative to this test file
        action_path = pathlib.Path(__file__).resolve().parents[1] / "action.yml"
        content = action_path.read_text()
        self.assertIn("name: Commit Emoji Reactor", content)
        self.assertIn("runs:", content)
        self.assertIn("steps:", content)

if __name__ == "__main__":
    unittest.main()
