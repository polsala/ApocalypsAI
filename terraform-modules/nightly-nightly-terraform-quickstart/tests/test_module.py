import unittest
import re
import os

class TestTerraformModule(unittest.TestCase):
    def read_file(self, filename):
        with open(os.path.join(os.path.dirname(__file__), '..', filename), 'r') as f:
            return f.read()

    def test_main_tf_contains_s3_bucket(self):
        content = self.read_file('main.tf')
        self.assertRegex(content, r'resource\s+"aws_s3_bucket"\s+"this"')
        self.assertRegex(content, r'versioning\s*{[^}]*enabled\s*=\s*true')
        self.assertRegex(content, r'lifecycle\s*{[^}]*prevent_destroy\s*=\s*true')
        self.assertRegex(content, r'aws_s3_bucket_lifecycle_configuration')

    def test_variables_tf(self):
        content = self.read_file('variables.tf')
        self.assertRegex(content, r'variable\s+"bucket_name"')

    def test_outputs_tf(self):
        content = self.read_file('outputs.tf')
        self.assertRegex(content, r'output\s+"bucket_id"')

if __name__ == "__main__":
    unittest.main()
