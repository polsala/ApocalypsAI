resource "aws_s3_bucket" "scavenger_cache" {
  bucket = var.bucket_name
  acl    = "private" # Ensure private access by default

  tags = var.tags
}

resource "aws_s3_bucket_versioning" "scavenger_cache_versioning" {
  count  = var.enable_versioning ? 1 : 0
  bucket = aws_s3_bucket.scavenger_cache.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "scavenger_cache_encryption" {
  count  = var.enable_encryption ? 1 : 0
  bucket = aws_s3_bucket.scavenger_cache.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "scavenger_cache_public_access_block" {
  bucket = aws_s3_bucket.scavenger_cache.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "scavenger_cache_lifecycle" {
  bucket = aws_s3_bucket.scavenger_cache.id

  rule {
    id     = "scavenger-cache-lifecycle-rule"
    status = "Enabled"

    # Transition noncurrent versions to GLACIER
    noncurrent_version_transition {
      days          = var.lifecycle_rule_days_to_transition_to_glacier
      storage_class = "GLACIER"
    }

    # Expire noncurrent versions
    noncurrent_version_expiration {
      days = var.lifecycle_rule_days_to_expire
    }
  }
}
