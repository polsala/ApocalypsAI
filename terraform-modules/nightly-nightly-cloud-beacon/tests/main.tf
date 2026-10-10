provider "aws" {
  region = "us-east-1" # Mock region, won't actually connect
  # Mock rationale: For offline validation and planning, AWS credentials are not strictly needed.
  # Terraform will parse the configuration and validate syntax. Providing mock credentials
  # satisfies the provider block's requirements without attempting a real connection.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_session_token"
}

module "test_beacon" {
  source = "../../src" # Relative path to the module source

  bucket_name_prefix = "test-apocalypsai-beacon"
  region             = "us-east-1"
  content_body       = "Test Beacon Activated! ApocalypsAI is online."
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI"
  }
}

output "test_s3_bucket_id" {
  value = module.test_beacon.s3_bucket_id
}

output "test_cloudfront_domain_name" {
  value = module.test_beacon.cloudfront_domain_name
}

output "test_cloudfront_distribution_id" {
  value = module.test_beacon.cloudfront_distribution_id
}
