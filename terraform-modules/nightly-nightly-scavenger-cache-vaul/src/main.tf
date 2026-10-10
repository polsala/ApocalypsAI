resource "aws_s3_bucket" "cache_vault" {
  bucket = var.bucket_name
  tags   = var.tags

  lifecycle_rule {
    id      = "glacier_transition"
    enabled = true

    transition {
      days          = var.glacier_transition_days
      storage_class = "GLACIER"
    }

    # Example: Expire objects after 10 years (3650 days) if not explicitly managed
    expiration {
      days = 3650
    }
  }
}

resource "aws_s3_bucket_versioning" "cache_vault_versioning" {
  bucket = aws_s3_bucket.cache_vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "cache_vault_encryption" {
  bucket = aws_s3_bucket.cache_vault.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "cache_vault_public_access_block" {
  bucket = aws_s3_bucket.cache_vault.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_logging" "cache_vault_logging" {
  count = var.access_logging_bucket_name != null ? 1 : 0

  bucket        = aws_s3_bucket.cache_vault.id
  target_bucket = var.access_logging_bucket_name[0]
  target_prefix = "log/${var.bucket_name}/"
}
