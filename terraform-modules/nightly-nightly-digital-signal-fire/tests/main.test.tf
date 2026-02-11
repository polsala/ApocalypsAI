# Mock rationale: This test module uses a local backend and null resources
# to simulate a Terraform configuration without actually deploying to AWS.
# It focuses on validating the module's syntax and variable usage.
# The `terraform validate` command will check syntax, and `terraform plan -destroy`
# will ensure the module can be planned for destruction, indicating proper resource definition.

# Configure a local backend for testing
terraform {
  backend "local" {
    path = "terraform.tfstate.test"
  }
}

# Use the module with dummy values for validation
module "test_signal_fire" {
  source = "../src" # Path to the module being tested

  bucket_name_prefix = "test-apocalypsai-signal-fire"
  initial_message    = "Test beacon online. All systems nominal."
  aws_region         = "us-east-1"
}

# Output to ensure outputs are correctly defined
output "test_s3_bucket_id" {
  value = module.test_signal_fire.s3_bucket_id
}

output "test_cloudfront_domain_name" {
  value = module.test_signal_fire.cloudfront_domain_name
}
