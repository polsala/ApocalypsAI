provider "aws" {
  region = "us-east-1"
  # Mock rationale: For `terraform validate` and `terraform plan`,
  # a valid region is required, but actual credentials are not needed
  # as no resources are provisioned or API calls made during these phases.
  # This allows for offline syntax and configuration validation.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_session_token"
}
