# Mock rationale: This test configuration instantiates the module with dummy values
# and uses `terraform validate` and `terraform plan -destroy` to ensure the module's
# syntax and structure are correct without provisioning actual cloud resources.
# This is a standard offline testing approach for Terraform modules.

provider "aws" {
  region = "us-east-1" # Mock region for validation
  # No actual credentials needed for validate/plan -destroy
}

module "test_whispering_postbox" {
  source = "../src"

  bucket_name_prefix = "test-postbox-mock"
  allowed_ip_cidrs   = ["192.0.2.0/24"] # Example IP range for testing
  region             = "us-east-1"
}

output "test_bucket_id" {
  value = module.test_whispering_postbox.bucket_id
}

output "test_bucket_arn" {
  value = module.test_whispering_postbox.bucket_arn
}
