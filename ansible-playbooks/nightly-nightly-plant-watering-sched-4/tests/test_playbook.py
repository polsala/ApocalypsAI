import unittest
import yaml
import os

class TestPlantWateringPlaybook(unittest.TestCase):
    def setUp(self):
        playbook_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'playbook.yml')
        with open(playbook_path, 'r') as f:
            self.playbook = yaml.safe_load(f)

    def test_playbook_structure(self):
        # Ensure top-level is a list with at least one dict
        self.assertIsInstance(self.playbook, list)
        self.assertGreaterEqual(len(self.playbook), 1)
        first = self.playbook[0]
        self.assertIn('tasks', first)
        tasks = first['tasks']
        # Check that there is a cron task
        cron_tasks = [t for t in tasks if 'cron' in t]
        self.assertTrue(any(cron_tasks), "Cron task not defined")
        cron_task = cron_tasks[0]['cron']
        self.assertEqual(cron_task['name'], "Plant watering via smart plug")
        self.assertIn('job', cron_task)

if __name__ == '__main__':
    unittest.main()
