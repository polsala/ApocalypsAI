resource "aws_s3_bucket" "cache_bucket" {
  bucket = var.bucket_name
  acl    = "private" # Ensure private access by default

  versioning {
    enabled = var.enable_versioning
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  lifecycle_rule {
    id      = "standard_to_glacier_and_expire"
    enabled = true

    transition {
      days          = var.transition_to_glacier_days
      storage_class = "GLACIER"
    }

    expiration {
      days = var.expire_after_days
    }
  }

  tags = merge(var.tags, {
    "ManagedBy"   = "ApocalypsAI-CloudCacheKeeper"
    "Environment" = var.environment
  })
}

resource "aws_s3_bucket_public_access_block" "cache_bucket_public_access_block" {
  bucket = aws_s3_bucket.cache_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
