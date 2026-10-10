import unittest
import pathlib

class TestQuotePosterWorkflow(unittest.TestCase):
    def setUp(self):
        # Locate the workflow file relative to this test file
        self.path = pathlib.Path(__file__).parent.parent / "src" / "post-quote.yml"
        self.content = self.path.read_text()

    def test_contains_inputs(self):
        # Mock rationale: ensure the workflow defines required inputs
        self.assertIn("inputs:", self.content)
        self.assertIn("github_token:", self.content)
        self.assertIn("issue_number:", self.content)

    def test_contains_steps(self):
        # Mock rationale: ensure there are steps for picking a quote and posting it
        self.assertIn("Select random quote", self.content)
        self.assertIn("Post comment", self.content)

if __name__ == "__main__":
    unittest.main()
