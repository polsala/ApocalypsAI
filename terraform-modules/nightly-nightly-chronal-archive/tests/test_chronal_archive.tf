# Mock rationale: This test configuration uses the module with dummy values.
# The 'terraform validate' command, which is run offline, will check the
# module's syntax, variable definitions, and output references without
# requiring actual AWS credentials or network access. It effectively
# verifies the module's internal consistency and adherence to Terraform HCL syntax.

# Configure the AWS provider with dummy values for offline validation.
# This block is purely for satisfying 'terraform init' and 'terraform validate'
# without needing actual credentials.
provider "aws" {
  region                      = "us-east-1"
  access_key                  = "mock_access_key" # Mock rationale: Dummy value for offline validation
  secret_key                  = "mock_secret_key" # Mock rationale: Dummy value for offline validation
  skip_credentials_validation = true              # Mock rationale: Skip actual credential validation
  skip_requesting_account_id  = true              # Mock rationale: Skip actual account ID request
  skip_metadata_api_check     = true              # Mock rationale: Skip metadata API check
  s3_use_path_style           = true              # Mock rationale: Use path style for S3 for local/mock
  endpoints {
    s3 = "http://localhost:4566" # Mock rationale: Point to a localstack-like endpoint for offline init/validate
  }
}

module "test_chronal_archive_instance" {
  source = "../src" # Path to the module being tested

  bucket_name_prefix = "test-temporal-echo"
  environment        = "test-timeline"
  versioning_enabled = true
  tags = {
    TestTag = "Validation"
  }
}

output "test_bucket_id" {
  value = module.test_chronal_archive_instance.bucket_id
}

output "test_bucket_arn" {
  value = module.test_chronal_archive_instance.bucket_arn
}
