provider "aws" {
  region = "us-east-1"
}

module "temporal_echo_vault_test" {
  source = "../" # Path to the module under test

  bucket_name_prefix = "test-echo-vault"
  tags = {
    Environment = "Test"
    Owner       = "ApocalypsAI"
  }
}

output "test_bucket_id" {
  value = module.temporal_echo_vault_test.bucket_id
}

output "test_bucket_arn" {
  value = module.temporal_echo_vault_test.bucket_arn
}
