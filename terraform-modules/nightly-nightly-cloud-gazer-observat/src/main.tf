resource "aws_s3_bucket" "observatory_bucket" {
  bucket_prefix = var.bucket_name_prefix
  acl           = "private" # Ensures private access by default

  tags = merge(var.tags, {
    "ManagedBy" = "ApocalypsAI-CloudGazer"
    "Purpose"   = "CelestialAnomalyStorage"
  })
}

resource "aws_s3_bucket_versioning" "observatory_bucket_versioning" {
  bucket = aws_s3_bucket.observatory_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "observatory_bucket_sse" {
  bucket = aws_s3_bucket.observatory_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "observatory_bucket_public_access_block" {
  bucket = aws_s3_bucket.observatory_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Optional: Lifecycle rule for archiving old data
resource "aws_s3_bucket_lifecycle_configuration" "observatory_bucket_lifecycle" {
  count  = var.enable_glacier_archive ? 1 : 0
  bucket = aws_s3_bucket.observatory_bucket.id

  rule {
    id     = "archive_old_anomalies"
    status = "Enabled"

    transition {
      days          = var.glacier_archive_days
      storage_class = "GLACIER"
    }

    expiration {
      days = var.glacier_expiration_days
    }
  }
}
