resource "aws_s3_bucket" "chronos_cache" {
  bucket = var.bucket_name
  acl    = var.bucket_acl

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id = "chronos-echo-retention"

    enabled = true

    noncurrent_version_transition {
      days          = var.noncurrent_transition_days
      storage_class = var.noncurrent_transition_storage_class
    }

    noncurrent_version_expiration {
      days = var.noncurrent_expiration_days
    }
  }

  tags = merge(
    var.tags,
    {
      "ManagedBy" = "ApocalypsAI-ChronosCache"
      "Purpose"   = "TemporalEchoChamber"
    }
  )
}

resource "aws_s3_bucket_public_access_block" "chronos_cache_public_access_block" {
  bucket = aws_s3_bucket.chronos_cache.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
