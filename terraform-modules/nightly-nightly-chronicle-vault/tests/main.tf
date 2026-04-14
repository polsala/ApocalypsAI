# Mock rationale: This file serves as a test harness for the module.
# It instantiates the module with specific inputs to allow 'terraform plan'
# to generate an execution plan that can be inspected by the test script.
# No actual AWS resources are provisioned during this test.

provider "aws" {
  region = "us-east-1"
  # Mock rationale: Dummy credentials for terraform plan, no actual auth needed for plan.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_chronicle_vault" {
  source = "../src"

  bucket_name_prefix         = "test-apocalypsai-vault"
  glacier_transition_days    = 90
  multipart_upload_expiration_days = 3

  tags = {
    TestEnv = "True"
    Module  = "ChronicleVault"
  }
}

output "test_bucket_id" {
  value = module.test_chronicle_vault.bucket_id
}

output "test_bucket_arn" {
  value = module.test_chronicle_vault.bucket_arn
}
