# Mock rationale: This file is for testing the module's syntax and plan generation offline.
# It uses dummy values for variables and does not require actual AWS credentials or resources.
# The 'aws' provider block is included for Terraform to recognize the resource types,
# but its configuration is minimal and doesn't point to a real account.

provider "aws" {
  region = "us-east-1" # Mock region
  # access_key = "mock_access_key" # Mock rationale: Not needed for terraform validate/plan with -destroy
  # secret_key = "mock_secret_key" # Mock rationale: Not needed for terraform validate/plan with -destroy
  skip_credentials_validation = true # Mock rationale: Skip actual credential checks
  skip_requesting_account_id = true # Mock rationale: Skip actual account ID checks
  skip_metadata_api_check = true # Mock rationale: Skip metadata API checks
  skip_region_validation = true # Mock rationale: Skip region validation
  # endpoint = "http://localhost:4566" # Mock rationale: Could use LocalStack for more advanced local testing, but not required for basic plan validation.
}

module "test_beacon" {
  source = "../src"

  bucket_name = "apocalypsai-test-beacon-12345" # Mock rationale: A unique, dummy bucket name for testing.
  aws_region  = "us-east-1"                    # Mock rationale: A dummy region for testing.
  tags = {                                     # Mock rationale: Dummy tags for testing.
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}

output "test_website_endpoint" {
  value = module.test_beacon.website_endpoint
}
