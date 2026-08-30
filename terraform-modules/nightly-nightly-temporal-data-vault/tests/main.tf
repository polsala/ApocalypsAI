# This is a test configuration to ensure the module can be instantiated
# and its outputs are correctly exposed.
# It does not provision actual resources during offline testing.

module "temporal_vault_test" {
  source = "../src"

  bucket_name = "test-apocalypsai-temporal-data-vault"
  tags = {
    Environment = "Test"
    Owner       = "ApocalypsAI"
  }
  region = "us-east-1" # Specify a region for the test
}

output "test_bucket_id" {
  value = module.temporal_vault_test.bucket_id
}

output "test_bucket_arn" {
  value = module.temporal_vault_test.bucket_arn
}

output "test_bucket_name" {
  value = module.temporal_vault_test.bucket_name
}
