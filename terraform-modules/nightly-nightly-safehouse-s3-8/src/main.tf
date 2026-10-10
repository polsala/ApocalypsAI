terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  # In test environments we rely on the AWS_DEFAULT_REGION env var.
  # No credentials are needed for local validation.
  region = var.aws_region
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  force_destroy = true

  tags = {
    Purpose = "PostApocalypticSafeHouse"
  }
}

resource "aws_s3_bucket_versioning" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id

  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls  = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id

  rule {
    id     = "expire-old-supplies"
    status = "Enabled"

    expiration {
      days = 30
    }

    filter {}
  }
}

resource "aws_s3_bucket_object" "supply_cache" {
  bucket = aws_s3_bucket.safehouse.id
  key    = "supply-cache.txt"
  content = "🧰 Emergency supplies placeholder. Replace with real inventory."
  content_type = "text/plain"
}
