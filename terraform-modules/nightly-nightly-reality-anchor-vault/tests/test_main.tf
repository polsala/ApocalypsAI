# This file is used by the test script to validate the module.
# It provides a minimal, valid configuration to instantiate the module.

# Configure a dummy AWS provider.
# Mock rationale: This provider block is configured to allow `terraform init` and `terraform validate`
# to succeed without requiring actual AWS credentials. The `skip_credentials_validation`,
# `skip_requesting_account_id`, and `skip_metadata_api_check` flags tell the provider to bypass
# credential checks and API calls for local operations. This makes the test deterministic and offline.
provider "aws" {
  region                      = "us-east-1"
  access_key                  = "mock_access_key" # Mock rationale: Dummy value for offline validation.
  secret_key                  = "mock_secret_key" # Mock rationale: Dummy value for offline validation.
  token                       = "mock_token"      # Mock rationale: Dummy value for offline validation.
  skip_credentials_validation = true              # Mock rationale: Prevents actual credential validation.
  skip_requesting_account_id  = true              # Mock rationale: Prevents actual account ID lookup.
  skip_metadata_api_check     = true              # Mock rationale: Prevents metadata API calls.
  s3_use_path_style           = true              # Mock rationale: Can help with localstack/mocking if needed.
}

module "test_reality_anchor_vault" {
  source = "../" # Refers to the parent module directory

  bucket_name      = "test-apocalypsai-reality-anchor-vault-12345" # Mock rationale: A unique, dummy bucket name for testing.
  environment      = "test"                                       # Mock rationale: Dummy environment for testing.
  retention_days   = 7                                            # Mock rationale: Short retention for test purposes.
  tags = {
    TestTag = "True"
  }
}
