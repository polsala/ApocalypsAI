import unittest, pathlib, re

class TestTerraformModule(unittest.TestCase):
    def setUp(self):
        self.tf_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "main.tf"
        self.content = self.tf_path.read_text()

    def test_s3_bucket_resource_present(self):
        self.assertIn('resource "aws_s3_bucket" "static_site"', self.content)

    def test_cloudfront_conditional(self):
        # Ensure the CloudFront resource uses count based on enable_cdn
        pattern = r'resource "aws_cloudfront_distribution" "cdn" {\s*count = var\.enable_cdn \? 1 : 0'
        self.assertRegex(self.content, pattern, "CloudFront count conditional missing")

if __name__ == "__main__":
    unittest.main()
