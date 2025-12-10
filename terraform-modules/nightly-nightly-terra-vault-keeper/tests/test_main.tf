# Mock rationale: This test uses a minimal set of Terraform resources to simulate
# the provisioning of a secrets manager vault and a secret. It does not require
# actual cloud provider credentials to run, as Terraform's plan/apply
# can be executed against a local state and mocked resources.

# For a more robust test, one would typically use a tool like Terratest
# to actually deploy to a test environment and then verify the state.
# However, for a self-contained utility, we'll simulate the core functionality.

provider "aws" {
  region = "us-east-1"
  # Mock credentials for local testing if not using actual AWS credentials
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "vault_keeper_test" {
  source = "../../terraform-modules/nightly-terra-vault-keeper"

  vault_name = "test-apoc-vault"
  region     = "us-east-1"

  rotation_enabled = true
  rotation_interval = "1h"

  secret_definitions = {
    "test_api_key" = {
      value = "test-secret-value-123"
    }
  }
}

# Assertions (conceptual - in a real test, you'd use terraform output and check values)
# For this example, we'll just ensure the module can be planned without errors.
# A full test would involve running `terraform plan` and inspecting the output.

output "test_vault_arn" {
  value = module.vault_keeper_test.vault_arn
}

output "test_secret_arns" {
  value = module.vault_keeper_test.secret_arns
}
