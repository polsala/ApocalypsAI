terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

provider "aws" {
  # In tests we rely on the default (mock) provider configuration.
  # Users should configure region and credentials as needed.
  region = "us-east-1"
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "safehouse" {
  bucket = "${var.bucket_name_prefix}-${random_id.bucket_suffix.hex}"
  force_destroy = true

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  versioning {
    enabled = var.versioning_enabled
  }

  lifecycle_rule {
    id      = "expire-noncurrent"
    enabled = true
    noncurrent_version_expiration {
      days = var.lifecycle_days
    }
  }
}

output "bucket_id" {
  description = "The name of the created bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the created bucket"
  value       = aws_s3_bucket.safehouse.arn
}
