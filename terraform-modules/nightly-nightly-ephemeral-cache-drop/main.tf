terraform {
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
  region = "us-east-1" # Default region, can be overridden by user
}

resource "random_id" "suffix" {
  byte_length = 8
}

resource "aws_s3_bucket" "ephemeral_cache" {
  bucket = "${var.bucket_name_prefix}-${random_id.suffix.hex}"
  tags   = var.tags
}

resource "aws_s3_bucket_public_access_block" "ephemeral_cache_public_access_block" {
  bucket = aws_s3_bucket.ephemeral_cache.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "ephemeral_cache_versioning" {
  bucket = aws_s3_bucket.ephemeral_cache.id
  versioning_configuration {
    status = "Disabled" # For ephemeral, we don't need versioning
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "ephemeral_cache_encryption" {
  bucket = aws_s3_bucket.ephemeral_cache.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "ephemeral_cache_lifecycle" {
  bucket = aws_s3_bucket.ephemeral_cache.id

  rule {
    id     = "expire-objects"
    status = "Enabled"

    expiration {
      days = var.expiration_days
    }
  }
}
