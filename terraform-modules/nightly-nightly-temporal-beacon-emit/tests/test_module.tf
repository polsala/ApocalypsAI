provider "aws" {
  region = "us-east-1"
  # Mock rationale: For offline validation and plan generation, AWS credentials
  # are not strictly required if the provider is configured. The actual deployment
  # would require valid credentials, but these tests focus on HCL syntax and structure.
  # We use a dummy access key and secret for provider configuration to allow `terraform init`
  # and `terraform plan` to proceed without failing on missing credentials, while still
  # being deterministic and not connecting to a real AWS account.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "temporal_beacon_test" {
  source = "../src"

  bucket_name_prefix = "test-apocalypsai-beacon"
  region             = "us-east-1"
  environment        = "test"
}
