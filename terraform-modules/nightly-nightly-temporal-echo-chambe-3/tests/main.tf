provider "aws" {
  region = "us-east-1" # Mock rationale: Required for Terraform to parse AWS resources, but no actual API calls are made during `terraform validate` or `terraform plan` without `apply`. No actual credentials are needed for these offline checks.
}

module "test_echo_chamber" {
  source = "../src"

  prefix         = "test-apocalypsai-echo-chamber"
  retention_days = 3 # Short retention for testing purposes
  aws_region     = "us-east-1"
}

output "test_bucket_id" {
  value = module.test_echo_chamber.bucket_id
}

output "test_bucket_arn" {
  value = module.test_echo_chamber.bucket_arn
}
