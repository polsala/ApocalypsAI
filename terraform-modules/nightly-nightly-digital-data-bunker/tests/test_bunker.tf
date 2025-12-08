# This file is used by the test script to validate the module.
# It instantiates the module with default values.

# Mock rationale: For offline and deterministic testing of a Terraform module,
# we define a mock AWS provider configuration. This allows `terraform init`
# and `terraform validate` to succeed without requiring actual AWS credentials
# or network access, as it only checks syntax and local configuration.
provider "aws" {
  region = "us-east-1" # Mock region for validation
  # No actual credentials needed for `terraform validate`
}

module "test_data_bunker" {
  source = "./src" # Path to the module under test (relative to this file)

  # Override defaults if specific test cases are needed,
  # but for basic validation, defaults are fine.
  bunker_name_prefix = "test-apocalypsai-bunker"
  aws_region         = "us-east-1" # Pass region to module
  tags = {
    TestEnv = "True"
  }
}

# We don't need to define outputs here, as `terraform validate`
# primarily checks syntax and configuration correctness.
# The module's own outputs are implicitly validated by its structure.
