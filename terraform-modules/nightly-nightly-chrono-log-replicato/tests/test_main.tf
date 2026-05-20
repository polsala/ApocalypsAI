provider "aws" {
  region = "us-east-1" # Mock region for validation
  # Mock rationale: This test configuration is designed to be run with `terraform validate`
  # and `terraform plan -out=tfplan -no-color`. It does not require actual AWS credentials
  # to pass these checks, as it only verifies the syntax and structure of the Terraform
  # module. The `provider "aws"` block is included for `terraform validate` to understand
  # the resource types, but no actual API calls are made during validation or planning
  # without an `apply`.
}

module "test_chrono_log_replicator" {
  source = "../src" # Path to the module being tested

  bucket_name = "test-chrono-log-bucket-12345"
  environment = "test"
}
