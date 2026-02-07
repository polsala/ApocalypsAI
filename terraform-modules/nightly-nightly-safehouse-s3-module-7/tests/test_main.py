import unittest
import pathlib
import re

class TestSafehouseS3Module(unittest.TestCase):
    """Tests for the nightly-safehouse-s3-module Terraform configuration.

    # Mock rationale: The tests operate purely on the static HCL file content, ensuring
    # they are deterministic and require no external Terraform binary or AWS credentials.
    """

    @classmethod
    def setUpClass(cls):
        cls.module_path = pathlib.Path(__file__).parents[1] / "src" / "main.tf"
        cls.content = cls.module_path.read_text()

    def assertPattern(self, pattern, msg=None):
        self.assertRegex(self.content, pattern, msg or f"Pattern not found: {pattern}")

    def test_provider_aws_present(self):
        self.assertPattern(r"provider \"aws\"", "AWS provider block missing")

    def test_s3_bucket_resource(self):
        self.assertPattern(r"resource \"aws_s3_bucket\" \"safehouse\"", "aws_s3_bucket \"safehouse\" resource missing")

    def test_versioning_enabled(self):
        self.assertPattern(r"versioning \{\s*enabled\s*=\s*true\s*\}", "Versioning block missing or disabled")

    def test_encryption_rule(self):
        self.assertPattern(r"server_side_encryption_configuration \{[\s\S]*sse_algorithm\s*=\s*\"AES256\"", "SSE‑S3 encryption configuration missing")

    def test_lifecycle_rule(self):
        self.assertPattern(r"lifecycle_rule \{[\s\S]*expiration \{[\s\S]*days\s*=\s*30", "Lifecycle rule to expire objects after 30 days missing")

    def test_public_access_block(self):
        self.assertPattern(r"resource \"aws_s3_bucket_public_access_block\" \"safehouse_block\"", "Public access block resource missing")

    def test_outputs(self):
        self.assertPattern(r"output \"bucket_id\"", "Output bucket_id missing")
        self.assertPattern(r"output \"bucket_arn\"", "Output bucket_arn missing")

if __name__ == "__main__":
    unittest.main()
