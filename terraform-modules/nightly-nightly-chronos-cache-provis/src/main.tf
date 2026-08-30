resource "aws_s3_bucket" "chronos_cache" {
  bucket = var.bucket_name

  tags = merge(
    {
      "ManagedBy" = "ApocalypsAI-ChronosCache"
      "Purpose"   = "TemporalDataCache"
    },
    var.tags
  )
}

resource "aws_s3_bucket_versioning" "chronos_cache_versioning" {
  bucket = aws_s3_bucket.chronos_cache.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "chronos_cache_sse" {
  bucket = aws_s3_bucket.chronos_cache.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
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
