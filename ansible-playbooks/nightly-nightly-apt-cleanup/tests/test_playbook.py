import subprocess
import unittest
from unittest.mock import patch, MagicMock

def run_playbook():
    """Execute the apt cleanup playbook."""
    result = subprocess.run(
        ["ansible-playbook", "-i", "src/inventory.ini", "src/playbook.yml"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout

class TestAptCleanupPlaybook(unittest.TestCase):
    @patch("subprocess.run")
    def test_playbook_runs_successfully(self, mock_run):
        # Mock rationale: simulate successful ansible-playbook execution without touching the system
        mock_process = MagicMock()
        mock_process.stdout = "PLAY RECAP ... success"
        mock_process.returncode = 0
        mock_run.return_value = mock_process

        output = run_playbook()
        mock_run.assert_called_once_with(
            ["ansible-playbook", "-i", "src/inventory.ini", "src/playbook.yml"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("success", output)

if __name__ == "__main__":
    unittest.main()
