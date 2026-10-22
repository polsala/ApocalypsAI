# This is a test configuration to instantiate the module.
# It should not be run directly for deployment.

provider "aws" {
  region = "us-east-1" # Mock region for plan generation
  # Mock rationale: No actual AWS credentials are needed for `terraform plan`
  # when testing module structure and resource generation.
  # The provider block is required by Terraform even for plan-only operations.
}

module "test_bottle_post_private" {
  source = "../src"

  bucket_name_prefix = "test-private-bottle"
  message_retention_days = 14
  enable_public_read = false
  tags = {
    Environment = "Test"
    Purpose     = "PrivateBottle"
  }
}

module "test_bottle_post_public" {
  source = "../src"

  bucket_name_prefix = "test-public-bottle"
  message_retention_days = 7
  enable_public_read = true
  tags = {
    Environment = "Test"
    Purpose     = "PublicBottle"
  }
}

module "test_bottle_post_no_versioning" {
  source = "../src"

  bucket_name_prefix = "test-no-versioning"
  message_retention_days = 1
  enable_public_read = false
  versioning_enabled = false
  tags = {
    Environment = "Test"
    Purpose     = "NoVersioning"
  }
}
