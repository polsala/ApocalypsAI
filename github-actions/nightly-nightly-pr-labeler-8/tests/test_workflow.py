import unittest
import yaml
import os

class TestPRLabelerWorkflow(unittest.TestCase):
    def setUp(self):
        # Locate the workflow file relative to this test file
        self.workflow_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'workflow.yml'))
        with open(self.workflow_path, 'r', encoding='utf-8') as f:
            self.workflow = yaml.safe_load(f)

    def test_trigger_is_workflow_call(selfn        self.assertIn('on', self.workflow)
        self.assertIn('workflow_call', self.workflow['on'])
        inputs = self.workflow['on']['workflow_call'].get('inputs', {})
        self.assertIn('label_map', inputs)
        self.assertTrue(inputs['label_map'].get('required', False))

    def test_job_structure(self):
        self.assertIn('jobs', self.workflow)
        self.assertIn('labeler', self.workflow['jobs'])
        job = self.workflow['jobs']['labeler']
        self.assertEqual(job.get('runs-on'), 'ubuntu-latest')
        steps = job.get('steps', [])
        step_names = [step.get('name') for step in steps]
        self.assertIn('Checkout PR', step_names)
        self.assertIn('Determine changed files', step_names)
        self.assertIn('Compute labels', step_names)
        self.assertIn('Add labels via GitHub API', step_names)

    def test_permissions(self):
        job = self.workflow['jobs']['labeler']
        perms = job.get('permissions', {})
        self.assertEqual(perms.get('contents'), 'read')
        self.assertEqual(perms.get('pull-requests'), 'write')

if __name__ == '__main__':
    unittest.main()
