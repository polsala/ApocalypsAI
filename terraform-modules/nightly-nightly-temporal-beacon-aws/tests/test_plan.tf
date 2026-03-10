# Mock rationale: This configuration is used for offline testing with terraform plan.
# It defines a minimal AWS provider configuration and calls the module under test.
# No actual AWS credentials are required for 'terraform plan' to validate the module.

provider "aws" {
  region = "us-east-1" # Hardcoded for deterministic testing
  # No access_key or secret_key needed for plan-only operations
}

module "test_temporal_beacon" {
  source = "../src" # Path to the module being tested

  bucket_name_prefix = "test-apocalypsai-beacon"
  environment        = "test"
  aws_region         = "us-east-1"
}
