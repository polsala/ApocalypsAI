provider "aws" {
  region = "us-east-1" # Mock region for plan/validate. No actual credentials needed.
  # Mock rationale: For `terraform validate` and `terraform plan`, AWS credentials are not strictly required
  # if no actual API calls are made. The provider block is needed for syntax validation and schema loading.
  # The region is specified to satisfy provider configuration requirements.
}

module "test_echo_vault" {
  source = "../src"

  bucket_name_prefix = "test-echo-vault-prefix"
  region             = "us-east-1"
  decay_period_days  = 1 # Test with a short decay period
}

output "test_bucket_id" {
  value = module.test_echo_vault.bucket_id
}

output "test_bucket_arn" {
  value = module.test_echo_vault.bucket_arn
}
