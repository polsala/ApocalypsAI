provider "aws" {
  region = var.aws_region
  # Mock rationale: For offline testing, the provider block is needed for syntax validation,
  # but no actual AWS credentials are required for `terraform validate` or `terraform plan`
  # when not applying. We're not performing actual API calls.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "temporal_echo_chamber_test" {
  source = "../src"

  bucket_name    = "apocalypsai-test-echo-chamber"
  aws_region     = "us-east-1"
  retention_days = 7
}

variable "aws_region" {
  description = "AWS region for testing."
  type        = string
  default     = "us-east-1"
}
