provider "aws" {
  region = "us-east-1"
  # Mock rationale: In a real test, this would be configured via environment variables
  # or a test-specific AWS profile. For offline testing, we just need a valid provider block.
  # No actual AWS calls will be made by `terraform plan -json`.
}

module "test_relay" {
  source = "../src"

  relay_name                = "test-whisperwind-relay-alpha"
  visibility_timeout_seconds = 60
  message_retention_seconds  = 86400
  delay_seconds             = 5
}
