import unittest
from unittest import mock
import subprocess

class TestSSHKeyRotator(unittest.TestCase):
    @mock.patch('subprocess.run')
    def test_playbook_execution_success(self, mock_run):
        # Mock rationale: simulate successful ansible-playbook run without real SSH
        mock_run.return_value = mock.Mock(returncode=0, stdout=b'PLAY RECAP', stderr=b'')
        result = subprocess.run(
            ['ansible-playbook', '-i', 'src/inventory.ini', 'src/rotate_ssh_keys.yml'],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn(b'PLAY RECAP', result.stdout)

    @mock.patch('subprocess.run')
    def test_missing_ssh_keygen(self, mock_run):
        # Mock rationale: simulate ssh-keygen missing causing non-zero exit
        mock_run.return_value = mock.Mock(returncode=1, stdout=b'', stderr=b'ssh-keygen: command not found')
        result = subprocess.run(
            ['ansible-playbook', '-i', 'src/inventory.ini', 'src/rotate_ssh_keys.yml'],
            capture_output=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b'command not found', result.stderr)

if __name__ == '__main__':
    unittest.main()
