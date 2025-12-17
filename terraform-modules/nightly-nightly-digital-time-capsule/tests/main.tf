provider "aws" {
  region = "us-east-1"
  # Mock rationale: We are not actually applying this configuration to AWS.
  # The provider block is required for `terraform init` and `terraform validate`
  # to correctly parse the module and its AWS-specific resources. Credentials
  # will not be used for `terraform validate` or `terraform plan -destroy`.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_time_capsule" {
  source = "../" # Reference the module in the parent directory

  bucket_name = "apocalypsai-test-time-capsule-12345"
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}
