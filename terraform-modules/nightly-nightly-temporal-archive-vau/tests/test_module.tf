# This is a test configuration to validate the module.
# It does not require AWS credentials for `terraform plan` assertions.

provider "aws" {
  region = "us-east-1" # Mock region, not actually used for plan
  # Mock rationale: For `terraform plan` validation, the provider block is needed
  # but actual credentials are not required if we only assert on the plan output.
  # This allows offline testing of the module's structure and variable interpolation.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "temporal_archive_test" {
  source = "./modules/nightly-temporal-archive-vault"

  bucket_name = "apocalypsai-test-archive-vault-12345"
  region      = "us-east-1"
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
  glacier_ir_transition_days = 60
  deep_archive_transition_days = 180
  expiration_days = 365
}

module "temporal_archive_no_expiration_test" {
  source = "./modules/nightly-temporal-archive-vault"

  bucket_name = "apocalypsai-test-archive-vault-no-expire-67890"
  region      = "us-east-1"
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
  glacier_ir_transition_days = 30
  deep_archive_transition_days = 90
  expiration_days = null # Test null expiration
}
