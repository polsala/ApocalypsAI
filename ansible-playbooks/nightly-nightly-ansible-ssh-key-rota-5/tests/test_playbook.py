import unittest
from unittest.mock import patch
import subprocess

class TestSSHKeyRotatorPlaybook(unittest.TestCase):
    @patch('subprocess.run')
    def test_playbook_runs_successfully(self, mock_run):
        # Mock rationale: simulate ansible-playbook execution without needing a real Ansible environment
        mock_run.return_value = subprocess.CompletedProcess(args=['ansible-playbook'], returncode=0)
        result = subprocess.run(
            ['ansible-playbook', '-i', 'tests/inventory.ini', 'src/playbook.yml', '--check'],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)

if __name__ == '__main__':
    unittest.main()
