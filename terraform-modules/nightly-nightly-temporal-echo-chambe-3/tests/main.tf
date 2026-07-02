# Mock rationale: This configuration is for testing the module's plan output
# without requiring actual AWS credentials or resource provisioning.
# The random_string resource ensures a unique bucket name for plan validation.

resource "random_string" "test_suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

module "test_echo_chamber" {
  source = "../src" # Path to the module being tested

  bucket_name_prefix = "test-echo-chamber-${random_string.test_suffix.result}"
  retention_days     = 14
  environment        = "test"
}

output "test_bucket_id" {
  value = module.test_echo_chamber.bucket_id
}

output "test_bucket_arn" {
  value = module.test_echo_chamber.bucket_arn
}

output "test_bucket_regional_domain_name" {
  value = module.test_echo_chamber.bucket_regional_domain_name
}
