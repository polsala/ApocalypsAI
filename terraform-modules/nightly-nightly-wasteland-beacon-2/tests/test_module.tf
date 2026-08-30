# This file instantiates the module for testing purposes.
# It does not deploy actual resources but allows `terraform validate` and `terraform plan`
# to check the module's syntax and expected resource creation.

module "test_beacon" {
  source = "../src" # Path to the module under test

  beacon_name         = "test-wasteland-beacon"
  schedule_expression = "rate(1 hour)"
  aws_region          = "us-east-1" # Mock rationale: Required by AWS provider, but no actual deployment.
}

# Output to verify if needed in a more advanced test script
output "test_lambda_name" {
  value = module.test_beacon.beacon_lambda_name
}

output "test_log_group_name" {
  value = module.test_beacon.beacon_log_group_name
}
