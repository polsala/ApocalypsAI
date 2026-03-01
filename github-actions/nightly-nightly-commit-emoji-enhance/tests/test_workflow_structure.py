import unittest, yaml, os

class TestWorkflowStructure(unittest.TestCase):
    def setUp(self):
        # Load the workflow YAML file
        self.path = os.path.join(os.path.dirname(__file__), '..', 'src', 'workflow.yml')
        with open(self.path, 'r') as f:
            self.workflow = yaml.safe_load(f)

    def test_has_name(self):
        self.assertIn('name', self.workflow)
        self.assertEqual(self.workflow['name'], 'Nightly Commit Emoji Enhancer')

    def test_has_workflow_call(self):
        self.assertIn('on', self.workflow)
        self.assertIn('workflow_call', self.workflow['on'])
        inputs = self.workflow['on']['workflow_call']['inputs']
        self.assertIn('github-token', inputs)
        self.assertTrue(inputs['github-token']['required'])

    def test_has_add_emoji_job(self):
        self.assertIn('jobs', self.workflow)
        self.assertIn('add-emoji', self.workflow['jobs'])
        job = self.workflow['jobs']['add-emoji']
        self.assertEqual(job['runs-on'], 'ubuntu-latest')
        steps = job['steps']
        self.assertTrue(any(step.get('uses') == 'actions/github-script@v6' for step in steps))

if __name__ == '__main__':
    unittest.main()
