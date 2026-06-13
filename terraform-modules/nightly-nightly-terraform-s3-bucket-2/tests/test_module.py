import unittest
import pathlib

class TestTerraformS3Module(unittest.TestCase):
    def setUp(self):
        # Path to the src directory relative to this test file
        self.module_path = pathlib.Path(__file__).parent.parent / "src"

    def test_main_contains_s3_bucket(self):
        content = (self.module_path / "main.tf").read_text()
        self.assertIn('resource "aws_s3_bucket" "this"', content)

    def test_versioning_logic(self):
        content = (self.module_path / "main.tf").read_text()
        self.assertIn('status = var.versioning ? "Enabled" : "Suspended"', content)

    def test_outputs_defined(self):
        outputs = (self.module_path / "outputs.tf").read_text()
        self.assertIn('output "bucket_id"', outputs)
        self.assertIn('output "bucket_arn"', outputs)

if __name__ == "__main__":
    unittest.main()
