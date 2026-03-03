import unittest
import re
from pathlib import Path

class TestTerraformS3WebsiteModule(unittest.TestCase):
    def setUp(self):
        # Load the Terraform file
        self.tf_path = Path(__file__).resolve().parents[1] / "src" / "main.tf"
        self.tf_content = self.tf_path.read_text()

    def test_contains_aws_s3_bucket_resource(self):
        # Mock rationale: ensure the module defines an aws_s3_bucket resource
        self.assertRegex(self.tf_content, r'resource\s+"aws_s3_bucket"\s+"this"')

    def test_website_block_has_index_and_error(self):
        # Mock rationale: verify website configuration uses variables
        pattern = r'website\s*{[^}]*index_document\s*=\s*var\.index_document[^}]*error_document\s*=\s*var\.error_document'
        self.assertRegex(self.tf_content, pattern, msg="Website block should reference index_document and error_document variables")

    def test_versioning_block_uses_variable(self):
        pattern = r'versioning\s*{[^}]*enabled\s*=\s*var\.versioning'
        self.assertRegex(self.tf_content, pattern, msg="Versioning block should reference versioning variable")

if __name__ == "__main__":
    unittest.main()
