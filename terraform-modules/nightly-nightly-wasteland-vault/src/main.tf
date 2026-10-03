terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
  required_version = "~> 1.0"
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

resource "aws_s3_bucket" "wasteland_vault" {
  bucket = "${var.bucket_name_prefix}-${var.environment}-${random_string.bucket_suffix.result}"

  tags = merge(
    var.tags,
    {
      "Name"        = "${var.bucket_name_prefix}-${var.environment}-vault"
      "Environment" = var.environment
      "ManagedBy"   = "ApocalypsAI"
    }
  )
}

resource "aws_s3_bucket_acl" "wasteland_vault_acl" {
  bucket = aws_s3_bucket.wasteland_vault.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "wasteland_vault_versioning" {
  bucket = aws_s3_bucket.wasteland_vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "wasteland_vault_sse" {
  bucket = aws_s3_bucket.wasteland_vault.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "wasteland_vault_public_access_block" {
  bucket = aws_s3_bucket.wasteland_vault.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
