provider "aws" {
  region = "us-east-1"
  # Mock rationale: For testing, we don't actually want to hit AWS. We'll rely on
  # `terraform plan -json` to verify resource configuration without actual deployment.
  # The provider block is required for syntax validation, but credentials are mocked.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

resource "random_string" "test_suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
  # Mock rationale: This random_string is used to ensure the module can handle
  # dynamic bucket names. Its exact value is not asserted, only its presence
  # and the fact that it's computed during the plan.
}

module "test_beacon" {
  source = "../src"

  bucket_name_prefix = "test-apocalypsai-beacon"
  region             = "us-east-1"
  message_seed       = "Test message for the beacon."
}

output "test_website_endpoint" {
  value = module.test_beacon.website_endpoint
}

output "test_bucket_name" {
  value = module.test_beacon.bucket_name
}
