import unittest
import re
import pathlib

class TestSafehouseS3Module(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the main.tf content once
        cls.tf_path = pathlib.Path(__file__).parents[2] / "src" / "main.tf"
        cls.tf_content = cls.tf_path.read_text()

    def test_aws_s3_bucket_resource_exists(self):
        pattern = r'resource\s+"aws_s3_bucket"\s+"safehouse"'
        self.assertRegex(self.tf_content, pattern, "aws_s3_bucket \"safehouse\" resource missing")

    def test_versioning_enabled(self):
        pattern = r'aws_s3_bucket_versioning"\s+"safehouse_versioning"[\s\S]*status\s*=\s*"Enabled"'
        self.assertRegex(self.tf_content, pattern, "S3 bucket versioning not enabled")

    def test_server_side_encryption(self):
        pattern = r'aws_s3_bucket_server_side_encryption_configuration"[\s\S]*sse_algorithm\s*=\s*"AES256"'
        self.assertRegex(self.tf_content, pattern, "Server‑side encryption AES256 not configured")

    def test_lifecycle_rule(self):
        pattern = r'aws_s3_bucket_lifecycle_configuration"[\s\S]*expiration[\s\S]*days\s*=\s*30'
        self.assertRegex(self.tf_content, pattern, "Lifecycle rule to expire objects after 30 days missing")

    def test_radiation_tag_generated(self):
        # Ensure the random_integer resource is present and its result is used in tags
        random_res = r'resource\s+"random_integer"\s+"radiation"'
        tag_use = r'"Radiation\\-Level"\s*=\s*random_integer\.radiation\.result'
        self.assertRegex(self.tf_content, random_res, "random_integer \"radiation\" resource missing")
        self.assertRegex(self.tf_content, tag_use, "Radiation‑Level tag not set from random integer")

if __name__ == "__main__":
    unittest.main()
