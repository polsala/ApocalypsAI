provider "aws" {
  region = "us-east-1"
  # Mock rationale: For offline testing, we don't need actual AWS credentials.
  # Terraform plan will still generate a valid plan based on the configuration.
  # The test script will parse the plan output, not execute it.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_chrono_vault" {
  source = "../src"

  bucket_name = "test-chrono-vault-12345"
  region      = "us-east-1"
  enable_access_logging = true
  log_bucket_name = "test-log-bucket-67890"
  transition_days_standard_ia = 45
  transition_days_glacier = 120
  expiration_days_noncurrent_versions = 90
}

module "test_chrono_vault_no_logging" {
  source = "../src"

  bucket_name = "test-chrono-vault-no-log-abcde"
  region      = "us-east-1"
  enable_access_logging = false
  transition_days_standard_ia = 30
  transition_days_glacier = 90
  expiration_days_noncurrent_versions = 60
}

output "test_bucket_id" {
  value = module.test_chrono_vault.bucket_id
}

output "test_bucket_arn" {
  value = module.test_chrono_vault.bucket_arn
}

output "test_bucket_domain_name" {
  value = module.test_chrono_vault.bucket_domain_name
}
