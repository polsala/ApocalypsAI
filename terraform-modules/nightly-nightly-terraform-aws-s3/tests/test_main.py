import pathlib
import unittest

class TestTerraformModule(unittest.TestCase):
    def setUp(self):
        self.base = pathlib.Path(__file__).parent.parent / "src"

    def test_main_tf_exists(self):
        self.assertTrue((self.base / "main.tf").exists())

    def test_versioning_enabled(self):
        content = (self.base / "main.tf").read_text()
        self.assertIn('enabled = true', content)

    def test_lifecycle_rule_present(self):
        content = (self.base / "main.tf").read_text()
        self.assertIn('lifecycle_rule', content)
        self.assertIn('transition', content)
        self.assertIn('expiration', content)

    def test_variable_defined(self):
        content = (self.base / "variables.tf").read_text()
        self.assertIn('variable \"bucket_name\"', content)

    def test_output_bucket_arn(self):
        content = (self.base / "outputs.tf").read_text()
        self.assertIn('output \"bucket_arn\"', content)

if __name__ == "__main__":
    unittest.main()
