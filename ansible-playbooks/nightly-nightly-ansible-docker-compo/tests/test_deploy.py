import unittest
from unittest.mock import patch, MagicMock
import subprocess

class TestDeployPlaybook(unittest.TestCase):
    @patch('subprocess.run')
    def test_playbook_runs_successfully(self, mock_run):
        # Mock rationale: simulate successful ansible-playbook execution
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = b'PLAY RECAP ...'
        mock_run.return_value = mock_result

        result = subprocess.run(['ansible-playbook', '-i', 'inventory.ini', 'deploy.yml', '--check'],
                                capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn(b'PLAY RECAP', result.stdout)

if __name__ == '__main__':
    unittest.main()
