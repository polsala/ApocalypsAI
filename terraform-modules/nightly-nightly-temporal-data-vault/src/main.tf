resource "aws_s3_bucket" "vault" {
  bucket = var.bucket_name

  tags = {
    Name        = "${var.bucket_name}-vault"
    Environment = var.environment
    ManagedBy   = "ApocalypsAI"
  }
}

resource "aws_s3_bucket_versioning_configuration" "vault_versioning" {
  bucket = aws_s3_bucket.vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "vault_lifecycle" {
  bucket = aws_s3_bucket.vault.id

  rule {
    id     = "archive_old_versions"
    status = "Enabled"

    noncurrent_version_transition {
      days          = var.retention_days_standard
      storage_class = "GLACIER"
    }

    noncurrent_version_expiration {
      days = var.retention_days_glacier
    }

    transition {
      days          = var.retention_days_standard
      storage_class = "GLACIER"
    }

    expiration {
      days = var.retention_days_glacier
    }
  }
}

resource "aws_s3_bucket_public_access_block" "vault_public_access_block" {
  bucket = aws_s3_bucket.vault.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
