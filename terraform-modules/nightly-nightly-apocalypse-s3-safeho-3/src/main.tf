terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  # Mock provider configuration for testing; real users should configure region/credentials.
  # Mock rationale: In tests we use the "null" provider, so this block is ignored.
  region = var.aws_region
}

provider "random" {}

resource "random_pet" "bucket_suffix" {
  length = 2
}

resource "aws_s3_bucket" "safehouse" {
  bucket        = "${var.bucket_prefix}-${random_pet.bucket_suffix.id}"
  force_destroy = true

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  lifecycle_rule {
    id      = "expire-old-objects"
    enabled = true

    expiration {
      days = 365
    }
  }

  tags = var.tags
}
