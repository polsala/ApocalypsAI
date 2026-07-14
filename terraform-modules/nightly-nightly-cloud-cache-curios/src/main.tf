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

resource "aws_s3_bucket" "curiosity_cache" {
  bucket = "${var.bucket_name_prefix}-${random_id.suffix.hex}"

  tags = var.tags
}

resource "aws_s3_bucket_versioning" "curiosity_cache_versioning" {
  bucket = aws_s3_bucket.curiosity_cache.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "curiosity_cache_sse" {
  bucket = aws_s3_bucket.curiosity_cache.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "curiosity_cache_public_access_block" {
  bucket = aws_s3_bucket.curiosity_cache.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "curiosity_cache_lifecycle" {
  bucket = aws_s3_bucket.curiosity_cache.id

  rule {
    id     = "temporal-decay"
    status = "Enabled"

    transition {
      days          = var.transition_to_ia_days
      storage_class = "STANDARD_IA"
    }

    expiration {
      days = var.retention_days
    }

    noncurrent_version_expiration {
      noncurrent_days = var.retention_days
    }
  }
}

# Used to generate a unique suffix for the bucket name
resource "random_id" "suffix" {
  byte_length = 8
}
