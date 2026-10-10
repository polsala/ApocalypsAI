resource "aws_s3_bucket" "wasteland_cache" {
  bucket = var.bucket_name
  acl    = "private" # Ensure private access by default

  tags = merge(
    {
      "ManagedBy" = "ApocalypsAI"
      "Purpose"   = "WastelandResourceCache"
    },
    var.tags
  )
}

resource "aws_s3_bucket_versioning" "wasteland_cache_versioning" {
  count  = var.enable_versioning ? 1 : 0
  bucket = aws_s3_bucket.wasteland_cache.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "wasteland_cache_encryption" {
  count  = var.enable_encryption ? 1 : 0
  bucket = aws_s3_bucket.wasteland_cache.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "wasteland_cache_public_access_block" {
  count  = var.enable_public_access_block ? 1 : 0
  bucket = aws_s3_bucket.wasteland_cache.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
