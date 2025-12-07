provider "aws" {
  region = "us-east-1" # Mock region for testing
  # Mock rationale: For terraform plan, AWS credentials are not strictly needed
  # if the provider block is present. Terraform will simulate the plan.
  # If actual credentials were required, this test would not be offline.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_token"
}

module "test_cache_keeper" {
  source = "../src"

  bucket_name                = "apocalypsai-test-cache-001"
  enable_versioning          = true
  transition_to_glacier_days = 60
  expire_after_days          = 730
  environment                = "test"
  tags = {
    Project = "ApocalypsAI"
    Owner   = "IntegratorAgent"
  }
}

output "test_bucket_id" {
  value = module.test_cache_keeper.bucket_id
}
