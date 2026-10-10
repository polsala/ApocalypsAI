resource "aws_s3_bucket" "chronos_cache" {
  bucket_prefix = var.bucket_name_prefix
  tags          = var.tags

  # Enable versioning to allow lifecycle rules to work correctly with non-current versions
  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "chronos_cache_lifecycle" {
  bucket = aws_s3_bucket.chronos_cache.id

  rule {
    id     = "chronos-cache-expiration"
    status = "Enabled"

    expiration {
      days = var.expiration_days
    }

    noncurrent_version_expiration {
      noncurrent_days = var.expiration_days
    }

    # Clean up incomplete multipart uploads
    abort_incomplete_multipart_upload {
      days_after_initiation = var.expiration_days
    }
  }
}

resource "aws_s3_bucket_public_access_block" "chronos_cache_public_access_block" {
  bucket = aws_s3_bucket.chronos_cache.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
