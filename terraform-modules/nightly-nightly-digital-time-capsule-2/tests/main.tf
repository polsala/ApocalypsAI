provider "aws" {
  region = "us-east-1" # Mock region for plan
  # Mock rationale: No actual AWS credentials are needed for `terraform plan`
  # as we are only inspecting the generated plan, not applying it.
  # The provider block is required for Terraform to parse the configuration.
}

module "test_time_capsule" {
  source = "../src"

  bucket_name           = "test-apocalypsai-time-capsule-12345"
  object_lock_mode      = "COMPLIANCE"
  object_lock_days      = 365
  archive_transition_days = 30
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}

output "test_bucket_id" {
  value = module.test_time_capsule.bucket_id
}
