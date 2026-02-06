provider "aws" {
  region = "us-east-1"
  # Mock rationale: Terraform tests run in a plan-only mode by default for assertions.
  # No actual AWS resources are provisioned during `terraform test` unless explicitly configured
  # for integration tests. The provider block is necessary for schema validation.
  # For offline testing, we rely on Terraform's ability to validate configuration against the provider schema.
}

resource "random_id" "test_suffix" {
  byte_length = 8
}

module "test_cosmic_dust_collector" {
  source = "../"

  bucket_name_prefix    = "test-dust-collector"
  environment           = "test"
  retention_days        = 10
  transition_days_to_ia = 3
}
