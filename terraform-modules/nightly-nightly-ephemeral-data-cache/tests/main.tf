# Mock rationale: For offline testing, we define a local provider configuration
# that doesn't require actual AWS credentials. Terraform plan will still
# generate a valid plan based on the module's resource definitions.
# We're testing the module's configuration, not its deployment.
provider "aws" {
  region = "us-east-1"
  # Mock rationale: Using dummy credentials for offline plan generation.
  # These are not used for actual deployment.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_ephemeral_cache" {
  source = "../src"

  bucket_name_prefix = "test-apocalypsai-cache"
  expiration_days    = 3
}

output "bucket_id" {
  value = module.test_ephemeral_cache.s3_bucket_id
}

output "bucket_arn" {
  value = module.test_ephemeral_cache.s3_bucket_arn
}
