import unittest
import pathlib
import re

class TestSafehouseTerraform(unittest.TestCase):
    def setUp(self):
        # Load the main.tf content
        self.tf_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "main.tf"
        self.content = self.tf_path.read_text()

    def test_random_pet_resource(self):
        self.assertRegex(self.content, r"resource \"random_pet\" \"bucket_name\"")

    def test_s3_bucket_resource(self):
        self.assertRegex(self.content, r"resource \"aws_s3_bucket\" \"safehouse\"")
        # Ensure bucket name uses the random pet
        self.assertIn("bucket = \"safehouse-${random_pet.bucket_name.id}\"", self.content)

    def test_versioning_enabled(self):
        self.assertRegex(self.content, r"resource \"aws_s3_bucket_versioning\" \"safehouse_versioning\"")
        self.assertIn("status = \"Enabled\"", self.content)

    def test_encryption_aes256(self):
        self.assertRegex(self.content, r"sse_algorithm = \"AES256\"")

    def test_lifecycle_30_days(self):
        self.assertRegex(self.content, r"days = 30")

if __name__ == "__main__":
    unittest.main()
