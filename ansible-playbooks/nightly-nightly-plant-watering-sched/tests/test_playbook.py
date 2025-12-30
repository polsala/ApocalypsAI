import unittest
from unittest import mock
import subprocess

class TestPlaybook(unittest.TestCase):
    @mock.patch('subprocess.run')
    def test_syntax_check(self, mock_run):
        # Mock rationale: simulate successful ansible-playbook syntax check
        mock_run.return_value = mock.Mock(returncode=0, stdout=b'Syntax OK', stderr=b'')
        result = subprocess.run(['ansible-playbook', '--syntax-check', 'playbook.yml'], capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn(b'Syntax OK', result.stdout)

    @mock.patch('subprocess.run')
    def test_check_mode(self, mock_run):
        # Mock rationale: simulate successful dry-run execution
        mock_run.return_value = mock.Mock(returncode=0, stdout=b'PLAY RECAP', stderr=b'')
        result = subprocess.run(['ansible-playbook', '-i', 'inventory.ini', 'playbook.yml', '--check'], capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn(b'PLAY RECAP', result.stdout)

if __name__ == '__main__':
    unittest.main()
