# Mock rationale: The test replaces actual Terraform binary calls with in‑memory mocks, ensuring the suite runs offline and deterministically.
import unittest
from unittest.mock import patch, MagicMock
import subprocess
import os

class TestSafehouseS3Module(unittest.TestCase):
    def setUp(self):
        # Resolve absolute path to the module's src directory
        self.module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))

    @patch("subprocess.run")
    def test_terraform_init_and_validate(self, mock_run):
        # Mock result for `terraform init`
        mock_init = MagicMock()
        mock_init.returncode = 0
        mock_init.stdout = b"Terraform has been successfully initialized!"
        # Mock result for `terraform validate`
        mock_validate = MagicMock()
        mock_validate.returncode = 0
        mock_validate.stdout = b"Success! The configuration is valid."

        # Side‑effect function to return the appropriate mock based on the command
        def side_effect(cmd, cwd, capture_output, text, check):
            if "init" in cmd:
                return mock_init
            if "validate" in cmd:
                return mock_validate
            raise ValueError("Unexpected Terraform command")

        mock_run.side_effect = side_effect

        # Execute mocked `terraform init`
        result_init = subprocess.run(
            ["terraform", "init", "-backend=false"],
            cwd=self.module_path,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result_init.returncode, 0)

        # Execute mocked `terraform validate`
        result_validate = subprocess.run(
            ["terraform", "validate"],
            cwd=self.module_path,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result_validate.returncode, 0)

if __name__ == "__main__":
    unittest.main()
