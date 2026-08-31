import os
import unittest

class TestCloudBeaconOfHope(unittest.TestCase):
    def setUp(self):
        self.main_tf_path = os.path.join(os.path.dirname(__file__), '../src/main.tf')
        self.variables_tf_path = os.path.join(os.path.dirname(__file__), '../src/variables.tf')
        self.outputs_tf_path = os.path.join(os.path.dirname(__file__), '../src/outputs.tf')

        with open(self.main_tf_path, 'r') as f:
            self.main_tf_content = f.read()
        with open(self.variables_tf_path, 'r') as f:
            self.variables_tf_content = f.read()
        with open(self.outputs_tf_path, 'r') as f:
            self.outputs_tf_content = f.read()

    def test_s3_bucket_resource_exists(self):
        # Mock rationale: Verifying the presence of core infrastructure components
        # by checking the Terraform configuration files directly. This avoids
        # actual AWS API calls, making the test offline and deterministic.
        self.assertIn('resource "aws_s3_bucket" "beacon_bucket"', self.main_tf_content)
        self.assertIn('bucket = "${var.project_name}-${var.env}-beacon-bucket"', self.main_tf_content)

    def test_s3_website_configuration_exists(self):
        # Mock rationale: Offline check for static website hosting configuration.
        self.assertIn('resource "aws_s3_bucket_website_configuration" "beacon_website_config"', self.main_tf_content)
        self.assertIn('index_document {', self.main_tf_content)
        self.assertIn('suffix = var.index_document', self.main_tf_content)

    def test_cloudfront_distribution_resource_exists(self):
        # Mock rationale: Offline check for CDN setup.
        self.assertIn('resource "aws_cloudfront_distribution" "beacon_cdn"', self.main_tf_content)
        self.assertIn('default_root_object = var.index_document', self.main_tf_content)
        self.assertIn('viewer_protocol_policy = "redirect-to-https"', self.main_tf_content)

    def test_cloudfront_oac_resource_exists(self):
        # Mock rationale: Offline check for CloudFront Origin Access Control.
        self.assertIn('resource "aws_cloudfront_origin_access_control" "beacon_oac"', self.main_tf_content)
        self.assertIn('origin_access_control_origin_type = "s3"', self.main_tf_content)

    def test_s3_bucket_policy_for_cloudfront_exists(self):
        # Mock rationale: Offline check for the S3 bucket policy allowing CloudFront access.
        self.assertIn('resource "aws_s3_bucket_policy" "beacon_bucket_policy"', self.main_tf_content)
        self.assertIn('data "aws_iam_policy_document" "s3_policy"', self.main_tf_content)
        self.assertIn('principals {\n      type        = "Service"\n      identifiers = ["cloudfront.amazonaws.com"]', self.main_tf_content)

    def test_variables_defined(self):
        # Mock rationale: Verifying that expected input variables are declared.
        self.assertIn('variable "project_name"', self.variables_tf_content)
        self.assertIn('variable "env"', self.variables_tf_content)
        self.assertIn('variable "index_document"', self.variables_tf_content)
        self.assertIn('variable "error_document"', self.variables_tf_content)

    def test_outputs_defined(self):
        # Mock rationale: Verifying that expected output variables are declared.
        self.assertIn('output "s3_bucket_name"', self.outputs_tf_content)
        self.assertIn('output "cloudfront_domain_name"', self.outputs_tf_content)
        self.assertIn('output "cloudfront_url"', self.outputs_tf_content)

if __name__ == '__main__':
    unittest.main()
