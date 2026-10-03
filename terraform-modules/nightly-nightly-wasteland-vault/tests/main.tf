# Mock rationale: This provider block is required for terraform init/validate/plan
# to function, even if no actual AWS resources are provisioned during testing.
# The 'skip_credentials_validation' and 'skip_requesting_account_id' are used
# to allow the provider to initialize without valid AWS credentials, making the
# test truly offline and deterministic.
provider "aws" {
  region                        = "us-east-1"
  access_key                    = "mock_access_key" # Mock rationale: Dummy value for offline validation
  secret_key                    = "mock_secret_key" # Mock rationale: Dummy value for offline validation
  skip_credentials_validation   = true # Mock rationale: Prevent actual AWS credential check
  skip_requesting_account_id    = true # Mock rationale: Prevent actual AWS account ID request
  skip_metadata_api_check       = true # Mock rationale: Prevent metadata API calls
  s3_use_path_style             = true # Mock rationale: Avoid DNS resolution for S3
  endpoints {
    s3 = "http://localhost:4566" # Mock rationale: Point to a dummy endpoint if needed, or just rely on skip flags
  }
}

# Mock rationale: The random provider is used by the module to generate a unique suffix.
# It does not require external API calls and is deterministic for testing purposes.
provider "random" {}

module "test_wasteland_vault" {
  source = "../src" # Path to the module under test

  bucket_name_prefix = "test-apocalypsai-vault"
  environment        = "test"
  tags = {
    TestTag = "true"
  }
}

output "test_bucket_id" {
  value = module.test_wasteland_vault.bucket_id
}

output "test_bucket_arn" {
  value = module.test_wasteland_vault.bucket_arn
}
