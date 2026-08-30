provider "aws" {
  region = "us-east-1"
  # Mock rationale: We are not performing actual AWS API calls.
  # This provider block is for Terraform's syntax validation and plan generation.
  # Credentials are not required for `terraform validate` or `terraform plan`
  # when only checking module syntax and local configuration.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_token"
}

resource "random_id" "test_suffix" {
  byte_length = 4
}

module "test_time_capsule" {
  source             = "../src"
  bucket_name_prefix = "test-apocalypsai-capsule-${random_id.test_suffix.hex}"
  retention_years    = 1 # Use a shorter period for testing, though default is 100
  tags = {
    Environment = "Test"
    ManagedBy   = "ApocalypsAI"
  }
}

output "test_bucket_name" {
  value = module.test_time_capsule.bucket_name
}

output "test_bucket_arn" {
  value = module.test_time_capsule.bucket_arn
}
