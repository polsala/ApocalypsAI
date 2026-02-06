# Mock rationale: This file acts as a test fixture, instantiating the module
# with specific inputs to allow for deterministic testing of its outputs and planned state.
# It does not provision real resources during 'terraform test plan'.
provider "aws" {
  region = "us-east-1"
  # Mock rationale: Using a dummy access key and secret key for offline validation.
  # Terraform test's 'plan' command does not require valid credentials for syntax/logic checks.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_session_token" # For temporary credentials
}

module "test_chronicle_archive" {
  source = "../" # Refers to the parent module directory

  bucket_name = "apocalypsai-test-chronicle-archive-12345"
  environment = "test"
  enable_lifecycle_rules = true
  noncurrent_version_transition_days = 30
  noncurrent_version_expiration_days = 180
}
