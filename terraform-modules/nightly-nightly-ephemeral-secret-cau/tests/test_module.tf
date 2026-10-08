# Mock rationale: This test configuration uses the module with mock values
# to ensure the module's syntax is valid and it can be planned for destruction
# without actual AWS credentials. It verifies the module structure and variable
# definitions are correct for Terraform CLI operations.

provider "aws" {
  region = "us-east-1"
  # Mock rationale: No actual credentials are provided for offline testing.
  # The 'skip_credentials_validation' and 'skip_requesting_account_id'
  # are used to allow 'terraform plan -destroy' to run without AWS API calls.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_token"
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true
  s3_use_path_style           = true
  endpoints {
    s3 = "http://localhost:4566" # Mock S3 endpoint for localstack if needed, but not strictly for this test
  }
}

module "ephemeral_secret_test" {
  source = "../src" # Path to the module being tested

  secret_name             = "test-ephemeral-secret"
  secret_string           = "super-secret-test-value"
  description             = "Test secret for Nightly Ephemeral Secret Cauldron."
  recovery_window_in_days = 7
}

output "test_secret_arn" {
  value = module.ephemeral_secret_test.secret_arn
}

output "test_secret_name" {
  value = module.ephemeral_secret_test.secret_name
}
