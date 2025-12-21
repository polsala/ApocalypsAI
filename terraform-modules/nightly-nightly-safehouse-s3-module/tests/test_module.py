import unittest
import pathlib
import re

class TestSafehouseS3Module(unittest.TestCase):
    def setUp(self):
        self.base_path = pathlib.Path(__file__).parent.parent

    def test_main_tf_contains_resources(self):
        main_tf = (self.base_path / "main.tf").read_text()
        # Check bucket resource
        self.assertRegex(main_tf, r'resource\s+"aws_s3_bucket"\s+"safehouse"')
        # Check versioning
        self.assertRegex(main_tf, r'resource\s+"aws_s3_bucket_versioning"\s+"safehouse_versioning"')
        # Check encryption
        self.assertRegex(main_tf, r'resource\s+"aws_s3_bucket_server_side_encryption_configuration"\s+"safehouse_encryption"')
        # Check lifecycle
        self.assertRegex(main_tf, r'resource\s+"aws_s3_bucket_lifecycle_configuration"\s+"safehouse_lifecycle"')

    def test_variables_have_defaults(self):
        vars_tf = (self.base_path / "variables.tf").read_text()
        # radiation_level should have default "moderate"
        match = re.search(r'variable\s+"radiation_level".*default\s*=\s*"([^\"]+)"', vars_tf, re.DOTALL)
        self.assertIsNotNone(match, "# Mock rationale: ensure default exists")
        self.assertEqual(match.group(1), "moderate")

    def test_outputs_reference_bucket(self):
        outputs_tf = (self.base_path / "outputs.tf").read_text()
        self.assertIn("aws_s3_bucket.safehouse.id", outputs_tf)
        self.assertIn("aws_s3_bucket.safehouse.arn", outputs_tf)

if __name__ == "__main__":
    unittest.main()
