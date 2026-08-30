# Mock rationale: This provider block is for local testing only.
# It uses dummy credentials and region to allow `terraform plan`
# to run without requiring actual AWS authentication.
# For real deployments, configure your AWS provider with valid credentials.
provider "aws" {
  region     = "us-east-1"
  access_key = "mock_access_key" # Mock rationale: Dummy access key for offline plan validation.
  secret_key = "mock_secret_key" # Mock rationale: Dummy secret key for offline plan validation.
  token      = "mock_session_token" # Mock rationale: Dummy session token for offline plan validation.
}

# Mock rationale: The random_id resource is used to generate a unique suffix
# for the bucket name, ensuring deterministic behavior during testing
# by providing a consistent input for the module.
resource "random_id" "test_suffix" {
  byte_length = 8
  keepers = {
    # This keeper ensures the random_id is re-generated if the module's source changes,
    # which is useful for testing module updates.
    module_source_hash = filemd5("${path.module}/../src/main.tf")
  }
}

module "test_temporal_message_drop" {
  source = "../src" # Path to the module being tested

  bucket_name_prefix = "test-apocalypsai-messages-${random_id.test_suffix.hex}-"
  message_retention_days = 1 # Very short retention for test scenarios
  tags = {
    Environment = "Test"
    TestedBy    = "ApocalypsAI"
  }
}

output "test_bucket_name" {
  value = module.test_temporal_message_drop.bucket_name
}

output "test_bucket_arn" {
  value = module.test_temporal_message_drop.bucket_arn
}
