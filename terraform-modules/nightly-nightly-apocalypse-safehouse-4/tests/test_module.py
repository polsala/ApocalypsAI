import unittest
import pathlib
import re

class TestSafehouseModule(unittest.TestCase):
    def setUp(self):
        # The test file lives in <module_root>/tests/, so go up one level to the module root
        self.module_path = pathlib.Path(__file__).parent.parent
        self.main_tf = (self.module_path / "main.tf").read_text()
        self.variables_tf = (self.module_path / "variables.tf").read_text()
        self.outputs_tf = (self.module_path / "outputs.tf").read_text()

    def test_aws_s3_bucket_resource_exists(self):
        pattern = r'resource\s+"aws_s3_bucket"\s+"safehouse"'
        self.assertRegex(self.main_tf, pattern, "aws_s3_bucket resource not found")

    def test_versioning_enabled(self):
        pattern = r'resource\s+"aws_s3_bucket_versioning"\s+"safehouse_versioning".*status\s*=\s*"Enabled"'
        self.assertRegex(self.main_tf, pattern, "Versioning not enabled")

    def test_encryption_aes256(self):
        pattern = r'sse_algorithm\s*=\s*"AES256"'
        self.assertRegex(self.main_tf, pattern, "AES256 encryption not configured")

    def test_lifecycle_30_days(self):
        pattern = r'expiration\s*{[^}]*days\s*=\s*30'
        self.assertRegex(self.main_tf, pattern, "Lifecycle expiration not set to 30 days")

    def test_bucket_name_variable(self):
        self.assertIn('variable "bucket_name"', self.variables_tf)

    def test_outputs_defined(self):
        self.assertIn('output "bucket_id"', self.outputs_tf)
        self.assertIn('output "bucket_arn"', self.outputs_tf)

if __name__ == "__main__":
    unittest.main()
