# Mock rationale: This test configuration uses the module with dummy values.
# It does not interact with actual AWS resources, ensuring determinism and offline execution.
# The 'aws' provider is configured with a dummy region, and the module is sourced locally.
# 'terraform plan -destroy' will validate the module's syntax and resource definitions.

provider "aws" {
  region = "us-east-1" # Dummy region for validation
  # Mock rationale: No actual AWS credentials are needed for `terraform validate` or `terraform plan -destroy`.
  # The provider block is present for syntax validation.
}

module "test_slumber_sentinel" {
  source = "../src" # Relative path to the module

  aws_region          = "us-east-1"
  instance_tags       = {
    "TestEnv" = "true",
    "Service" = "DummyApp"
  }
  stop_cron_schedule  = "cron(0 23 * * ? *)"
  start_cron_schedule = "cron(0 6 * * ? *)"
  lambda_memory_size  = 256
  lambda_timeout      = 120
}
