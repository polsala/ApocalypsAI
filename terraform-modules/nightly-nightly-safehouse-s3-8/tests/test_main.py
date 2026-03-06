import unittest
import re
import pathlib

class TestSafehouseS3Module(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load file contents once
        cls.main_tf = pathlib.Path('main.tf').read_text()
        cls.variables_tf = pathlib.Path('variables.tf').read_text()
        cls.outputs_tf = pathlib.Path('outputs.tf').read_text()

    def test_bucket_resource_exists(self):
        """Ensure aws_s3_bucket resource is defined with the correct bucket name variable."""
        pattern = r'resource\s+"aws_s3_bucket"\s+"safehouse"\s*{[^}]*bucket\s*=\s*var\.bucket_name'
        self.assertRegex(self.main_tf, pattern, "aws_s3_bucket resource with var.bucket_name not found")

    def test_versioning_enabled(self):
        """Check that versioning is enabled for the bucket."""
        pattern = r'resource\s+"aws_s3_bucket_versioning"\s+"safehouse_versioning"[\s\S]*status\s*=\s*"Enabled"'
        self.assertRegex(self.main_tf, pattern, "Bucket versioning not enabled")

    def test_encryption_aes256(self):
        """Verify server‑side encryption uses AES256."""
        pattern = r'sse_algorithm\s*=\s*"AES256"'
        self.assertRegex(self.main_tf, pattern, "AES256 encryption not configured")

    def test_lifecycle_expiration(self):
        """Confirm lifecycle rule uses the expiration_days variable."""
        pattern = r'expiration\s*{[^}]*days\s*=\s*var\.expiration_days'
        self.assertRegex(self.main_tf, pattern, "Lifecycle expiration does not reference var.expiration_days")

    def test_iam_policy_attached_to_role(self):
        """Ensure IAM policy attachment references the allowed_role_arn variable."""
        pattern = r'roles\s*=\s*\[var\.allowed_role_arn\]'
        self.assertRegex(self.main_tf, pattern, "IAM policy attachment does not use var.allowed_role_arn")

    def test_variables_defined(self):
        """Check that all required variables are declared in variables.tf."""
        for var in ["bucket_name", "allowed_role_arn", "expiration_days"]:
            self.assertIn(f'variable "{var}"', self.variables_tf, f"Variable {var} not defined")

    def test_outputs_defined(self):
        """Validate that outputs for bucket_arn and policy_arn exist."""
        for out in ["bucket_arn", "policy_arn"]:
            self.assertIn(f'output "{out}"', self.outputs_tf, f"Output {out} not defined")

if __name__ == '__main__':
    unittest.main()
