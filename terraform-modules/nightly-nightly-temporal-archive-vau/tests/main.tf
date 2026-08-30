# Mock rationale: This test configuration uses a local backend and
# does not require AWS credentials for `terraform validate`. For `terraform plan`,
# it would typically require AWS credentials, but we are focusing on offline
# validation of the module's syntax and structure. The `aws` provider block is
# included for `terraform init` to download the provider, but actual API calls
# are not made during `validate`.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "local" { # Mock rationale: Using a local backend for offline testing.
    path = "terraform.tfstate"
  }
}

provider "aws" {
  region = "us-east-1" # Mock rationale: A default region is needed for provider configuration, but no actual API calls are made during `validate`.
  # access_key = "mock_access_key" # Mock rationale: Not needed for `terraform validate`
  # secret_key = "mock_secret_key" # Mock rationale: Not needed for `terraform validate`
}

module "test_archive_vault_basic" {
  source = "../src"

  bucket_name       = "apocalypsai-test-archive-basic-12345" # Unique name for testing
  enable_versioning = true
  enable_object_lock = false
}

module "test_archive_vault_immutable" {
  source = "../src"

  bucket_name         = "apocalypsai-test-archive-immutable-67890" # Unique name for testing
  enable_versioning   = true
  enable_object_lock  = true
  retention_mode      = "COMPLIANCE"
  retention_period_days = 7
}
