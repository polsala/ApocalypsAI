# Mock rationale: This test configuration uses the module with dummy values
# to ensure it can be initialized, validated, and a plan can be generated
# without actual AWS credentials or resource creation.
# It simulates a user consuming the module.

provider "aws" {
  region = "us-east-1"
  # Mock rationale: Dummy credentials for offline validation.
  # Terraform validate and plan do not require valid credentials for syntax checks.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  skip_credentials_validation = true # Mock rationale: Prevents AWS provider from trying to validate dummy credentials.
  skip_requesting_account_id = true  # Mock rationale: Prevents AWS provider from trying to fetch account ID.
  skip_metadata_api_check = true     # Mock rationale: Prevents AWS provider from trying to check metadata API.
  s3_use_path_style = true           # Mock rationale: For localstack/mocking compatibility, though not strictly needed for offline plan.
}

module "test_whisperwind_relay" {
  source = "../src"

  queue_name = "test-whisperwind-queue"
  topic_name = "test-whisperwind-topic"
  tags = {
    Environment = "test"
    Project     = "ApocalypsAI"
  }
}
