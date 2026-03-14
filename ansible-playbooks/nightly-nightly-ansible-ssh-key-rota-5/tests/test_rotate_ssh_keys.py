import unittest
import subprocess
import os

class TestRotateSSHKeysPlaybook(unittest.TestCase):
    def test_playbook_check_mode(self):
        """Run the playbook in check mode to ensure syntax and logic are valid."""
        playbook_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'rotate_ssh_keys.yml')
        inventory_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'inventory.ini')
        cmd = [
            'ansible-playbook',
            '-i', inventory_path,
            playbook_path,
            '--check',
            '-e', 'target_user=root'
        ]
        # Mock rationale: Running in check mode avoids side effects on the host.
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, msg=f"Playbook failed: {result.stderr}")

if __name__ == '__main__':
    unittest.main()
