# Mock rationale: We cannot interact with a real AWS API for offline tests.
# The mock provider allows us to simulate resource creation and check outputs
# without actual cloud provisioning, ensuring deterministic and fast tests.

provider "aws" {
  region = "us-east-1" # Required for AWS provider, but mocked
}

provider "random" {}

run "bucket_creation_and_tags" {
  variables {
    bucket_name_prefix = "test-prefix"
    common_tags = {
      "Environment" = "Test"
    }
  }

  # Mock the AWS provider to simulate resource creation
  mock_provider "aws" {
    resource "aws_s3_bucket" "hide_and_seek_bucket" {
      id     = "mock-test-prefix-12345678"
      arn    = "arn:aws:s3:::mock-test-prefix-12345678"
      bucket = "mock-test-prefix-12345678"
      acl    = "private"
      tags = {
        "Game"        = "CloudHideAndSeek"
        "WhimsyLevel" = "High"
        "Ephemeral"   = "True"
        "CreatedBy"   = "ApocalypsAI"
        "Environment" = "Test"
      }
    }
  }

  # Mock the random provider to ensure deterministic string generation
  mock_provider "random" {
    resource "random_string" "suffix" {
      id     = "12345678"
      result = "12345678"
    }
  }

  assert {
    condition     = output.bucket_id.value == "mock-test-prefix-12345678"
    error_message = "Bucket ID should match the mocked value"
  }

  assert {
    condition     = output.bucket_arn.value == "arn:aws:s3:::mock-test-prefix-12345678"
    error_message = "Bucket ARN should match the mocked value"
  }
}

run "default_bucket_name" {
  variables {
    # bucket_name_prefix is default ""
    common_tags = {}
  }

  # Mock the AWS provider to simulate resource creation with default prefix
  mock_provider "aws" {
    resource "aws_s3_bucket" "hide_and_seek_bucket" {
      id     = "mock-hide-seek-abcdefgh"
      arn    = "arn:aws:s3:::mock-hide-seek-abcdefgh"
      bucket = "mock-hide-seek-abcdefgh"
      acl    = "private"
      tags = {
        "Game"        = "CloudHideAndSeek"
        "WhimsyLevel" = "High"
        "Ephemeral"   = "True"
        "CreatedBy"   = "ApocalypsAI"
      }
    }
  }

  # Mock the random provider to ensure deterministic string generation
  mock_provider "random" {
    resource "random_string" "suffix" {
      id     = "abcdefgh"
      result = "abcdefgh"
    }
  }

  assert {
    condition     = output.bucket_id.value == "mock-hide-seek-abcdefgh"
    error_message = "Bucket ID should match the mocked default value"
  }

  assert {
    condition     = output.bucket_arn.value == "arn:aws:s3:::mock-hide-seek-abcdefgh"
    error_message = "Bucket ARN should match the mocked default value"
  }
}
