import unittest
import pathlib
import re

class TestCrypticKeepModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Resolve the directory containing the module files
        cls.module_dir = pathlib.Path(__file__).parents[2] / "src"
        cls.main_tf = (cls.module_dir / "main.tf").read_text()
        cls.vars_tf = (cls.module_dir / "variables.tf").read_text()
        cls.outputs_tf = (cls.module_dir / "outputs.tf").read_text()

    def test_bucket_resource_present(self):
        """Ensure the S3 bucket resource is defined with versioning and encryption."""
        bucket_pattern = re.compile(r'resource\s+"aws_s3_bucket"\s+"secret_vault"', re.MULTILINE)
        self.assertRegex(self.main_tf, bucket_pattern)
        self.assertIn('versioning {', self.main_tf)
        self.assertIn('server_side_encryption_configuration {', self.main_tf)

    def test_public_access_block(self):
        """Check that public access is blocked for the bucket."""
        block_pattern = re.compile(r'resource\s+"aws_s3_bucket_public_access_block"\s+"block_public"', re.MULTILINE)
        self.assertRegex(self.main_tf, block_pattern)
        self.assertIn('block_public_acls   = true', self.main_tf)

    def test_secret_and_password(self):
        """Validate Secrets Manager resources and random password configuration."""
        secret_pattern = re.compile(r'resource\s+"aws_secretsmanager_secret"\s+"vault_password"', re.MULTILINE)
        self.assertRegex(self.main_tf, secret_pattern)
        self.assertIn('resource "random_password" "generated"', self.main_tf)

    def test_variable_defaults(self):
        """Confirm that password_length has a default of 16 and proper validation."""
        self.assertIn('default     = 16', self.vars_tf)
        self.assertIn('condition     = var.password_length >= 8 && var.password_length <= 64', self.vars_tf)

    def test_outputs_defined(self):
        """Check that both outputs are present and reference correct resources."""
        self.assertIn('output "bucket_arn"', self.outputs_tf)
        self.assertIn('aws_s3_bucket.secret_vault.arn', self.outputs_tf)
        self.assertIn('output "secret_arn"', self.outputs_tf)
        self.assertIn('aws_secretsmanager_secret.vault_password.arn', self.outputs_tf)

if __name__ == '__main__':
    unittest.main()
