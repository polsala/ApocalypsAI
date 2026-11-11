provider "aws" {
  region = "us-east-1"
  # Mock rationale: These credentials are dummy and will not be used by `terraform plan`.
  # The plan command only evaluates the configuration, it does not interact with AWS API.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

provider "random" {
  # Mock rationale: The random_string resource is used in the module to ensure unique bucket names.
  # For testing, we need to ensure the provider for random is available, but its actual output
  # is not critical for plan validation, only its presence in the graph. No credentials needed.
}

module "test_beacon" {
  source = "../src"

  beacon_message     = "Test Beacon Message for ApocalypsAI"
  bucket_name_prefix = "test-apocalypsai-beacon"
  aws_region         = "us-east-1"
}

output "test_cloudfront_domain_name" {
  value = module.test_beacon.cloudfront_domain_name
}

output "test_s3_bucket_name" {
  value = module.test_beacon.s3_bucket_name
}
