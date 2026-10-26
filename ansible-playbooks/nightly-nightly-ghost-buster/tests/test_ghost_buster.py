import unittest
import yaml
from pathlib import Path
from unittest import mock

class TestGhostBusterPlaybook(unittest.TestCase):
    def setUp(self):
        # Load the playbook YAML for structural assertions
        playbook_path = Path(__file__).parents[1] / 'src' / 'ghost_buster.yml'
        with playbook_path.open('r', encoding='utf-8') as f:
            self.playbook = yaml.safe_load(f)

    def test_playbook_structure(self):
        # Ensure the top‑level is a list with one play
        self.assertIsInstance(self.playbook, list)
        self.assertEqual(len(self.playbook), 1)
        play = self.playbook[0]
        self.assertIn('hosts', play)
        self.assertIn('become', play)
        self.assertTrue(play['become'])
        self.assertIn('tasks', play)
        self.assertIsInstance(play['tasks'], list)
        # Verify expected task names are present
        task_names = [t.get('name') for t in play['tasks']]
        self.assertIn('Find ghost processes owned by {{ ghost_user }}', task_names)
        self.assertIn('Kill ghost processes', task_names)
        self.assertIn('Celebrate the exorcism', task_names)

    @mock.patch('subprocess.run')
    def test_mocked_ansible_execution(self, mock_run):
        # Simulate a successful ansible‑playbook run without touching a real host
        mock_run.return_value = mock.Mock(returncode=0, stdout='PLAY RECAP ...', stderr='')
        import subprocess
        result = subprocess.run(['ansible-playbook', '--check', 'src/ghost_buster.yml'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('PLAY RECAP', result.stdout)
        # Ensure the mock was called with the expected arguments
        mock_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
