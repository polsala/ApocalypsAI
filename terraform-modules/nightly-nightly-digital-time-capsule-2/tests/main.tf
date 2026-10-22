provider "aws" {
  region = "us-east-1" # Mock rationale: A dummy region is required for Terraform validation, but no actual AWS API calls are made.
  # Mock rationale: No actual credentials are needed for terraform validate or plan with -backend=false.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_time_capsule" {
  source = "../src"

  bucket_name_prefix = "apocalypsai-test-capsule"
  tags = {
    Environment = "test"
    Project     = "ApocalypsAI"
  }
  enable_lifecycle_rules = true
  lifecycle_rule_days_to_glacier = 30
  lifecycle_rule_days_to_delete  = 90
}
