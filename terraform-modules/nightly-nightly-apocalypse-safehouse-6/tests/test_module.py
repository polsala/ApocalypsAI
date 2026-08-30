import unittest
import pathlib
import re

class TestSafehouseS3Module(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load file contents once
        base_path = pathlib.Path(__file__).parents[1]
        cls.main_tf = (base_path / "main.tf").read_text()
        cls.variables_tf = (base_path / "variables.tf").read_text()
        cls.outputs_tf = (base_path / "outputs.tf").read_text()

    def test_bucket_name_variable_exists(self):
        self.assertIn('variable "bucket_name"', self.variables_tf)

    def test_versioning_enabled(self):
        # Look for versioning block with enabled = true
        pattern = r"versioning\s*{[^}]*enabled\s*=\s*true"
        self.assertRegex(self.main_tf, pattern, "Versioning block with enabled = true not found")

    def test_server_side_encryption(self):
        self.assertIn('sse_algorithm = "AES256"', self.main_tf)

    def test_lifecycle_expiration_30_days(self):
        # Ensure lifecycle rule expires after 30 days
        pattern = r"expiration\s*{[^}]*days\s*=\s*30"
        self.assertRegex(self.main_tf, pattern, "Lifecycle expiration of 30 days not found")

    def test_outputs_defined(self):
        self.assertIn('output "bucket_id"', self.outputs_tf)
        self.assertIn('output "bucket_arn"', self.outputs_tf)

if __name__ == "__main__":
    unittest.main()
