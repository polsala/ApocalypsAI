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
  # In tests we use the "us-east-1" region with dummy credentials.
  region = var.aws_region
}

resource "random_pet" "bucket_name" {
  length    = 2
  separator = "-"
}

resource "aws_s3_bucket" "this" {
  bucket = "${var.bucket_prefix}-${random_pet.bucket_name.id}"
  tags   = var.tags

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
    id      = "expire-noncurrent"
    enabled = true

    noncurrent_version_expiration {
      days = 30
    }
  }
}
