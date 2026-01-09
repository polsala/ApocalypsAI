provider "aws" {
  region = "us-east-1" # Mock rationale: Use a fixed region for deterministic planning.
  # Mock rationale: No actual credentials needed for `terraform validate` or `terraform plan` without applying.
  # For `data "aws_caller_identity" "current" {}`, its `account_id` will be `(known after apply)` in the plan output,
  # which is acceptable for a plan-based test asserting resource existence and configuration.
}

module "temporal_echo_chamber" {
  source = "../"

  project_name = "test-apocalypsai"
  environment  = "test"
  region       = "us-east-1"
}
