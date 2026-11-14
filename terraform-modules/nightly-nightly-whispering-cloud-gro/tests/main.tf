# Mock rationale: This test configuration uses the module with mock inputs
# to ensure it can be initialized and planned without syntax errors.
# It does not provision actual AWS resources.

provider "aws" {
  region = "us-east-1" # Mock region for validation
  # Mock rationale: No actual credentials needed for `terraform validate` or `terraform plan`.
  # We are only checking the module's syntax and variable/output definitions.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_grove" {
  source = "../src" # Path to the module being tested

  bucket_name_prefix   = "test-grove-prefix"
  enable_s3_versioning = true
  index_document       = "test-index.html"
  error_document       = "test-error.html"
}

output "test_s3_bucket_id" {
  value = module.test_grove.s3_bucket_id
}

output "test_cloudfront_domain_name" {
  value = module.test_grove.cloudfront_domain_name
}
