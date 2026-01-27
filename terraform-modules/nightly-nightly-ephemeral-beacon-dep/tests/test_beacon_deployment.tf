# Mock rationale: This test fixture uses the module with dummy inputs
# to allow for offline validation and plan generation, simulating a deployment
# without actually provisioning cloud resources.
# Terraform's `validate` and `plan` commands act as a form of "mocking"
# the cloud provider by checking the configuration's correctness and
# predicting changes without making them.

provider "aws" {
  region = "us-east-1" # Mock region for validation
  # No actual credentials needed for `terraform validate` or `terraform plan`
  # when testing module syntax and structure.
  # Mock rationale: Provider configuration is minimal for offline validation.
}

module "ephemeral_beacon_test" {
  source = "../../" # Path to the module being tested (relative to tests/)

  bucket_name     = "test-apocalypsai-beacon-12345" # Mock bucket name, must be unique for validation
  whisper_content = "Testing the beacon's whisper! This is a mock message."
  aws_region      = "us-east-1" # Mock region
}

output "test_bucket_name" {
  value = module.ephemeral_beacon_test.beacon_bucket_name
}

output "test_whisper_url" {
  value = module.ephemeral_beacon_test.beacon_whisper_url
}
