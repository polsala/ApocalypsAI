# Mock rationale: This block defines a null provider, which doesn't interact
# with any external services. It allows Terraform to initialize and plan
# the module without requiring actual AWS credentials or network access,
# making the tests deterministic and offline. The module itself doesn't
# create AWS resources directly, only generates names and tags, so a null
# provider is sufficient for testing its logic.
provider "null" {
  # No configuration needed for a null provider
}

# Mock rationale: Although the module specifies an AWS provider requirement
# in versions.tf, for offline testing of the module's *logic* (name/tag generation),
# we don't need to actually interact with AWS. Terraform will still validate
# the provider block, but since the module only computes strings, this provider
# block is effectively a no-op for the purpose of these tests. Dummy values
# are provided to satisfy Terraform's validation without requiring real credentials.
provider "aws" {
  region     = "us-east-1"
  access_key = "mock_access_key" # Mock rationale: Dummy value for offline validation
  secret_key = "mock_secret_key" # Mock rationale: Dummy value for offline validation
  token      = "mock_token"      # Mock rationale: Dummy value for offline validation
  skip_credentials_validation = true # Mock rationale: Skip actual credential check
  skip_requesting_account_id  = true # Mock rationale: Skip actual account ID check
  skip_metadata_api_check     = true # Mock rationale: Skip actual metadata API check
  skip_region_validation      = true # Mock rationale: Skip actual region validation
}
