terraform {
  required_version = ">= 1.3.0"

  required_providers {
    aws    = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }

  # Use a local backend for testing – no remote state required.
  backend "local" {}
}

provider "aws" {
  # In tests we rely on the AWS provider's validation only; region can be any valid value.
  region = "us-east-1"
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  force_destroy = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "expire-old-objects"
    enabled = true
    expiration {
      days = var.expiration_days
    }
  }

  tags = {
    Purpose = "Post‑Apocalyptic Safe‑House Data Storage"
  }
}

resource "aws_s3_bucket_logging" "log" {
  count = var.enable_logging ? 1 : 0

  bucket = aws_s3_bucket.safehouse.id
  target_bucket = "my‑safehouse‑logs"   # Placeholder – user must create this bucket separately.
  target_prefix = "log/"
}

resource "random_password" "access" {
  length  = 16
  special = false
}
