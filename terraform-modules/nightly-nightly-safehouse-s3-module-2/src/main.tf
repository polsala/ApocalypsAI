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
  # Region is required for validation but no real credentials are needed.
  region = "us-east-1"
}

resource "aws_s3_bucket" "safehouse" {
  bucket        = var.bucket_name
  force_destroy = true

  versioning {
    enabled = var.versioning
  }

  lifecycle_rule {
    id      = "expire-old-objects"
    enabled = true

    expiration {
      days = var.expiration_days
    }
  }
}

resource "random_password" "vault_secret" {
  length  = 16
  special = true
}

output "bucket_id" {
  value = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  value = aws_s3_bucket.safehouse.arn
}

output "vault_password" {
  value     = random_password.vault_secret.result
  sensitive = true
}
