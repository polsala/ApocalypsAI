provider "aws" {
  region = "us-east-1" # Mock region for validation
  # No actual credentials needed for `terraform validate` and `terraform plan -backend=false`
}

module "test_vault" {
  source = "../src"

  bucket_name = "apocalypsai-test-temporal-data-vault-12345"
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}

module "test_vault_no_lifecycle" {
  source = "../src"

  bucket_name            = "apocalypsai-test-temporal-data-vault-no-lifecycle"
  enable_lifecycle_rules = false
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}

module "test_vault_custom_lifecycle" {
  source = "../src"

  bucket_name                        = "apocalypsai-test-temporal-data-vault-custom-lifecycle"
  noncurrent_version_expiration_days = 120
  transition_current_to_ia_days      = 45
  transition_noncurrent_to_ia_days   = 75
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}
