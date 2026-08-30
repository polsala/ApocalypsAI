import unittest, re, pathlib

class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.path = pathlib.Path(__file__).resolve().parents[1] / 'src' / 'workflow.yml'
        self.content = self.path.read_text()
    def test_on_workflow_call(self):
        self.assertIn('workflow_call', self.content)
    def test_has_emoji_input(self):
        self.assertRegex(self.content, r'emoji_list.*default')
    def test_has_git_amend_step(self):
        self.assertIn('git commit --amend', self.content)

if __name__ == '__main__':
    unittest.main()
