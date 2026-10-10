# Mock rationale: Using a mock provider to test Terraform module structure and resource creation without actual cloud deployment.

terraform {
  required_providers {
    # Mock provider for testing purposes
    mock = {
      source = "hashicorp/mock"
      version = "0.1.0"
    }
  }
}

provider "mock" {
  # Mock provider configuration
}

module "test_infra" {
  source = ".."

  vpc_cidr_block    = "192.168.0.0/24"
  subnet_cidr_block = "192.168.1.0/28"
  region            = "eu-west-1"
}

output "test_vpc_id" {
  value = module.test_infra.vpc_id
}

output "test_subnet_id" {
  value = module.test_infra.subnet_id
}

# This test assumes the mock provider will return dummy values for outputs.
# In a real scenario, you'd use a testing framework like Terratest or a more sophisticated mock setup.
# For this example, we're just ensuring the structure is valid and outputs are defined.

# Example of how you might assert outputs if a more advanced mock was used:
# assert {
#   condition     = module.test_infra.vpc_id == "mock-vpc-id"
#   error_message = "VPC ID mismatch."
# }
