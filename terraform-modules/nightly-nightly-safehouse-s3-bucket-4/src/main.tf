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
  # In test environment, use dummy credentials
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_s3_bucket" "safehouse" {
  bucket        = var.bucket_name
  force_destroy = true

  tags = {
    Name        = "Safehouse Bucket"
    Environment = var.environment
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

resource "aws_s3_bucket_lifecycle_configuration" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id

  rule {
    id     = "expire-old-objects"
    status = "Enabled"

    expiration {
      days = 30
    }

    filter {}
  }
}

resource "aws_s3_bucket_public_access_block" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id

  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls  = true
  restrict_public_buckets = true
}
