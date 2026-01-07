terraform {
  required_version = ">= 1.3.0"

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
  # In real usage, configure region and credentials via environment variables or shared config.
  # Mock rationale: tests run with a local backend and no real AWS calls.
  region = "us-east-1"
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  tags   = var.tags
}

resource "aws_s3_bucket_versioning" "safehouse_versioning" {
  bucket = aws_s3_bucket.safehouse.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "safehouse_encryption" {
  bucket = aws_s3_bucket.safehouse.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "safehouse_lifecycle" {
  bucket = aws_s3_bucket.safehouse.id
  rule {
    id     = "glacier-transition"
    status = "Enabled"
    filter {}
    transition {
      days          = var.lifecycle_days
      storage_class = "GLACIER"
    }
    expiration {
      days = var.lifecycle_days + 365
    }
  }
}

resource "random_password" "access_token" {
  length  = var.password_length
  special = false
  upper   = true
  lower   = true
  number  = true
}
