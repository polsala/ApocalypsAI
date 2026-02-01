resource "aws_s3_bucket" "chronicle_archive" {
  bucket = var.bucket_name
  tags = {
    Environment = var.environment
    Project     = "ApocalypsAI Chronicle Archive"
  }
}

resource "aws_s3_bucket_versioning" "chronicle_archive_versioning" {
  bucket = aws_s3_bucket.chronicle_archive.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "chronicle_archive_encryption" {
  bucket = aws_s3_bucket.chronicle_archive.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "chronicle_archive_public_access_block" {
  bucket = aws_s3_bucket.chronicle_archive.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "chronicle_archive_lifecycle" {
  count = var.enable_lifecycle_rules ? 1 : 0
  bucket = aws_s3_bucket.chronicle_archive.id

  rule {
    id     = "archive_old_versions"
    status = "Enabled"

    noncurrent_version_transition {
      days          = var.noncurrent_version_transition_days
      storage_class = "GLACIER"
    }

    noncurrent_version_expiration {
      days = var.noncurrent_version_expiration_days
    }
  }
}
