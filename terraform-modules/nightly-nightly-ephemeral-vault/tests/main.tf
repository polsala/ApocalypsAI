# Mock rationale: This configuration uses the module with dummy values
# to allow 'terraform validate' to check syntax and variable usage
# without requiring actual AWS credentials or resource provisioning.
# The 'null_resource' is a placeholder to ensure a resource is present
# for validation, though not strictly necessary for module validation.

provider "aws" {
  region = "us-east-1" # Mock region for validation
  # No actual credentials needed for 'terraform validate'
}

module "test_ephemeral_vault" {
  source = "../src" # Path to the module under test
  
  bucket_name_prefix = "test-ephemeral-data"
  retention_days     = 1
  tags = {
    Test = "True"
  }
}

# A null resource to ensure a resource is present in the configuration
# for terraform to process, though not strictly required for module validation.
resource "null_resource" "dummy_resource" {
  triggers = {
    bucket_id = module.test_ephemeral_vault.bucket_id
  }
}
