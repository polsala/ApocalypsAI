provider "aws" {
  region = var.aws_region
  # Mock rationale: For `terraform validate` and `terraform plan`, the provider block is needed.
  # We provide dummy credentials to satisfy syntax checks, but no actual AWS API calls are made.
  # The test relies on `terraform plan -detailed-exitcode` to verify the module's structure and expected changes.
  access_key = "mock_access_key" 
  secret_key = "mock_secret_key" 
  token      = "mock_session_token" # Mock rationale: Include token for assumed roles scenarios.
}

variable "aws_region" {
  description = "The AWS region for testing."
  type        = string
  default     = "us-east-1"
}

module "ephemeral_beacon_test" {
  source = "../src"

  bucket_prefix   = "test-beacon"
  expiration_days = 1
  aws_region      = var.aws_region
}

output "test_bucket_id" {
  value = module.ephemeral_beacon_test.bucket_id
}

output "test_bucket_arn" {
  value = module.ephemeral_beacon_test.bucket_arn
}
