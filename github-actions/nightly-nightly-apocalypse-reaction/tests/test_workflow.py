import unittest
import yaml
import os

class TestApocalypseReactionWorkflow(unittest.TestCase):
    def setUp(self):
        # Load the workflow YAML file
        workflow_path = os.path.join(os.path.dirname(__file__), '..', '..', '.github', 'workflows', 'apocalypse-reaction.yml')
        with open(workflow_path, 'r', encoding='utf-8') as f:
            self.workflow = yaml.safe_load(f)

    def test_trigger_is_issues_opened(self):
        # Mock rationale: ensure the workflow triggers on issue creation
        self.assertIn('issues', self.workflow.get('on', {}), "Workflow should have an 'issues' trigger")
        self.assertIn('opened', self.workflow['on']['issues'].get('types', []), "Trigger types should include 'opened'")

    def test_two_github_script_steps(self):
        # Mock rationale: verify both reaction and comment steps are present
        steps = self.workflow.get('jobs', {}).get('react', {}).get('steps', [])
        self.assertEqual(len(steps), 2, "There should be exactly two steps")
        for step in steps:
            self.assertEqual(step.get('uses'), 'actions/github-script@v6', "Each step must use actions/github-script@v6")
        # Verify the first step contains an emoji array
        first_script = steps[0]['with']['script']
        self.assertIn('const emojis =', first_script, "First script should define an 'emojis' array")
        # Verify the second step contains a messages array
        second_script = steps[1]['with']['script']
        self.assertIn('const messages =', second_script, "Second script should define a 'messages' array")

if __name__ == '__main__':
    unittest.main()
