provider "aws" {
  region = "us-east-1"
}

module "test_vault" {
  source = "../"

  name        = "test-vault-guard"
  description = "A test secret vault"
  tags = {
    TestEnv = "true"
  }
}

# Mock rationale: We are using Terraform's built-in testing capabilities and not external mocks.
# The 'provider "aws"' block configures the AWS provider, and the module block
# instantiates the module under test. Terraform's plan/apply process will
# validate the syntax and resource definitions. For actual state validation,
# one would typically run `terraform plan` and inspect the output or use
# a testing framework like Terratest.

# For the purpose of this self-contained utility, we'll define a simple test
# that would pass if `terraform plan` succeeds without syntax errors.
# A more comprehensive test would involve `terraform apply` and then using
# AWS SDKs or CLI to verify the created resources.

output "test_secret_arn" {
  value = module.test_vault.secret_arn
}

output "test_secret_name" {
  value = module.test_vault.secret_name
}

output "test_secret_version_id" {
  value = module.test_vault.secret_version_id
}
