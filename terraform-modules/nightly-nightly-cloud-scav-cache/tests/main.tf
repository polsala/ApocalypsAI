# Mock rationale: This file is part of the test setup, not the module itself.
# It simulates how a user would consume the module.
provider "aws" {
  region = "us-east-1"
  # Mock rationale: Region is required for provider configuration, but no actual AWS calls are made during `terraform validate`.
  # This is a mock provider configuration for local validation.
  access_key = "mock_access_key" # Mock rationale: Placeholder for validation, not used in offline tests.
  secret_key = "mock_secret_key" # Mock rationale: Placeholder for validation, not used in offline tests.
}

module "test_scavenger_cache" {
  source = "../src"

  bucket_name_prefix = "test-apocalypsai-cache"
  tags = {
    Environment = "test"
    Owner       = "ApocalypsAI-Test"
  }
}
