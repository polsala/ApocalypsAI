# This file is used to test the module locally.
# It instantiates the module with example values.

# Configure the AWS provider (required for terraform validate, but not for static checks in test.sh)
# Mock rationale: For offline validation, the provider block is needed for HCL syntax checks,
# but no actual AWS credentials or network access are used by test.sh.
provider "aws" {
  region = "us-east-1"
  # access_key = "mock_access_key" # Not actually used by test.sh
  # secret_key = "mock_secret_key" # Not actually used by test.sh
  # skip_credentials_validation = true # Helps with offline validation
  # skip_requesting_account_id = true
  # skip_metadata_api_check = true
  # skip_region_validation = true
  # skip_get_ec2_platforms = true
}

# Mock rationale: The random provider is used by the module to generate a unique suffix.
# It needs to be declared here for `terraform validate` to pass, even though no actual
# random ID is generated during the static analysis in test.sh.
provider "random" {
  # No configuration needed for offline validation
}

module "echo_vault_test" {
  source = "../src"

  bucket_name_prefix = "test-echo-vault"
  region             = "us-east-1"
  echo_chamber_retention_days = 30
  echo_chamber_glacier_days   = 90
  echo_chamber_decay_days     = 365
  enable_versioning           = true
}

output "bucket_id" {
  value = module.echo_vault_test.bucket_id
}
output "bucket_arn" {
  value = module.echo_vault_test.bucket_arn
}
