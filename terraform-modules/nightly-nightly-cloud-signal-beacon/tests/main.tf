provider "aws" {
  region = "us-east-1"
  # Mock rationale: No actual AWS credentials are required for `terraform validate`.
  # This block is present to satisfy the provider requirement of the module.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_beacon" {
  source = "../src" # Relative path to the module under test

  region             = "us-east-1"
  bucket_name_prefix = "apocalypsai-test-beacon"
  signal_message     = "Test signal: All systems nominal, for now."
}
