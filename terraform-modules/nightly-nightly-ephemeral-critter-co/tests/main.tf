# tests/main.tf - Configuration to test the ephemeral-critter-corral module

# Mock rationale: This test configuration uses the module with dummy values
# and relies on 'terraform validate' to check syntax and resource graph
# without actually provisioning AWS resources.

provider "aws" {
  region = "us-east-1"
  # Mock rationale: We don't need actual credentials for `terraform validate`.
  # The AWS provider is declared but its credentials are mocked to prevent
  # actual API calls during `validate`, ensuring the test remains offline.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_critter" {
  source = "../src"

  region        = "us-east-1"
  instance_type = "t2.nano"
  ami_id        = "ami-0abcdef1234567890" # A dummy AMI ID for validation
  name_prefix   = "test-apocalypsai"
  additional_tags = {
    "TestTag" = "true"
  }
}

output "test_instance_id" {
  value = module.test_critter.instance_id
}

output "test_public_ip" {
  value = module.test_critter.public_ip
}
