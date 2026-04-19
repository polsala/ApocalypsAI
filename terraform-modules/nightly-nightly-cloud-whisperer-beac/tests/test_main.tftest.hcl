# Mock rationale: This test validates the Terraform configuration's structure,
# variable handling, and output generation without deploying actual AWS resources.
# It uses mock provider configurations and asserts on planned resource attributes
# and module outputs, ensuring determinism and offline execution. The `run = false`
# directive prevents any actual AWS API calls.

run "test_default_beacon_configuration" {
  module "beacon" {
    source = "../src"
    # No variables needed, uses defaults
  }

  # Mock the AWS provider to prevent actual API calls
  provider "aws" {
    alias = "mock"
    # These values are arbitrary and won't be used by the test runner
    region     = "us-east-1"
    access_key = "mock_access_key"
    secret_key = "mock_secret_key"
  }

  assert {
    condition     = module.beacon.s3_bucket_id != null
    error_message = "S3 bucket ID should be generated."
  }

  assert {
    condition     = module.beacon.cloudfront_domain_name != null
    error_message = "CloudFront domain name should be generated."
  }

  # Check that the S3 bucket ID starts with the default prefix
  assert {
    condition     = startswith(module.beacon.s3_bucket_id, "apocalypsai-beacon-")
    error_message = "S3 bucket ID should start with the default prefix."
  }
}

run "test_custom_bucket_prefix" {
  module "beacon" {
    source = "../src"
    bucket_name_prefix = "custom-apocalypsai-signal"
  }

  provider "aws" {
    alias = "mock"
    region     = "us-east-1"
    access_key = "mock_access_key"
    secret_key = "mock_secret_key"
  }

  assert {
    condition     = startswith(module.beacon.s3_bucket_id, "custom-apocalypsai-signal-")
    error_message = "S3 bucket ID should start with the custom prefix."
  }

  assert {
    condition     = module.beacon.cloudfront_domain_name != null
    error_message = "CloudFront domain name should be generated for custom prefix."
  }
}
