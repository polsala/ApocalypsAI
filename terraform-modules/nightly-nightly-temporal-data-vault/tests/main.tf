# Mock rationale: This configuration is used for offline validation and planning.
# It does not provision actual AWS resources.
# The 'bucket_name' is set to a placeholder as it's required by the module,
# but its uniqueness is not checked during 'terraform validate' or 'terraform plan'
# without actual AWS API calls.
# The 'logging_bucket_name' is also a placeholder.

provider "aws" {
  region = "us-east-1" # Mock rationale: A region is required by the provider, but no actual API calls are made.
}

module "temporal_data_vault_test" {
  source = "../src"

  bucket_name          = "test-temporal-data-vault-12345" # Mock rationale: Placeholder name for validation.
  environment          = "test"
  project              = "ApocalypsAI-Test"
  retention_days_to_glacier = 1
  expiration_days_noncurrent = 2
  enable_access_logging = true
  logging_bucket_name   = "test-s3-access-logs-bucket-12345" # Mock rationale: Placeholder name for validation.
}
