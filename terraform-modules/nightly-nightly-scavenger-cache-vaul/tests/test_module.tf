# Mock rationale: This test file uses `terraform validate` and `terraform fmt --check`
# which are offline and deterministic. The AWS provider block is included to satisfy
# Terraform's parsing requirements for a valid configuration, but no actual API calls
# are made during validation. This ensures the module's syntax is correct without needing
# live AWS credentials or network access.

provider "aws" {
  region = "us-east-1" # Mock region for validation purposes
  # No credentials needed for `terraform validate`
}

module "test_scavenger_cache" {
  source = "../src" # Path to the module being tested

  bucket_name = "test-scavenger-cache-vault-12345" # Unique name for testing
  region      = "us-east-1"
  tags = {
    TestEnv = "True"
    Purpose = "Validation"
  }

  enable_versioning                       = true
  enable_encryption                       = true
  lifecycle_rule_days_to_expire           = 7
  lifecycle_rule_days_to_transition_to_glacier = 3
}

# To run these tests:
# 1. Navigate to the 'tests' directory.
# 2. Run `terraform init` (downloads provider, can be cached).
# 3. Run `terraform validate` to check configuration syntax and internal consistency.
# 4. Run `terraform fmt --check` to ensure proper formatting.
