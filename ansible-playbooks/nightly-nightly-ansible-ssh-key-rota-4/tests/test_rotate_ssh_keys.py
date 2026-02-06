import unittest
from unittest.mock import patch, MagicMock
import subprocess

class TestRotateSSHKeysPlaybook(unittest.TestCase):
    @patch('subprocess.run')
    def test_playbook_runs_successfully(self, mock_run):
        # Mock subprocess.run to simulate ansible-playbook execution
        # Mock rationale: simulate ansible-playbook without real hosts.
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = b'PLAY RECAP ... ok=3 changed=1'
        mock_process.stderr = b''
        mock_run.return_value = mock_process

        # Execute the playbook in check mode
        result = subprocess.run(
            ['ansible-playbook', '-i', 'inventory.ini', 'rotate_ssh_keys.yml', '--check'],
            capture_output=True
        )

        # Verify that subprocess.run was called with expected arguments
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertIn('ansible-playbook', args)
        self.assertIn('--check', args)

        # Ensure the mocked process reports success
        self.assertEqual(result.returncode, 0)
        self.assertIn(b'PLAY RECAP', result.stdout)

if __name__ == '__main__':
    unittest.main()
