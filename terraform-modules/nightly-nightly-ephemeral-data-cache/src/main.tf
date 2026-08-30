resource "aws_s3_bucket" "ephemeral_cache" {
  bucket_prefix = var.bucket_name_prefix
  acl           = "private" # Best practice for data caches

  tags = {
    ManagedBy = "ApocalypsAI-NightlyEphemeralDataCache"
    Purpose   = "EphemeralDataCache"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "ephemeral_cache_lifecycle" {
  bucket = aws_s3_bucket.ephemeral_cache.id

  rule {
    id     = "auto-expire-objects"
    status = "Enabled"

    expiration {
      days = var.expiration_days
    }

    # Optional: Transition to Glacier for older versions if versioning is enabled
    # noncurrent_version_transition {
    #   days          = 30
    #   storage_class = "GLACIER"
    # }
    # noncurrent_version_expiration {
    #   days = 60
    # }
  }
}

# Block public access for security best practices
resource "aws_s3_bucket_public_access_block" "ephemeral_cache_public_access_block" {
  bucket = aws_s3_bucket.ephemeral_cache.id

  block_public_acls       = true
  block_public_and_cross_account_access = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
