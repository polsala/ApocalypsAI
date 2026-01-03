terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  # Configuration is expected to be provided via environment variables or shared credentials.
  # No hard‑coded credentials.
}

resource "random_pet" "suffix" {
  length = 2
}

resource "aws_s3_bucket" "safehouse" {
  bucket = "${var.bucket_prefix}-${random_pet.suffix.id}"
  tags   = var.tags

  lifecycle_rule {
    id      = "glacier-transition"
    enabled = true

    transition {
      days          = 30
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }

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
}
