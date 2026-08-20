resource "aws_s3_bucket" "cache_vault" {
  bucket = var.bucket_name
  tags   = var.tags
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

resource "aws_s3_bucket_lifecycle_configuration" "cache_vault_lifecycle" {
  bucket = aws_s3_bucket.cache_vault.id

  rule {
    id     = "wasteland-resource-management"
    status = "Enabled"

    transition {
      days          = var.retention_days_standard_to_ia
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = var.retention_days_ia_to_glacier
      storage_class = "GLACIER"
    }

    expiration {
      days = var.retention_days_glacier_to_delete
    }

    noncurrent_version_transition {
      days          = var.retention_days_standard_to_ia
      storage_class = "STANDARD_IA"
    }

    noncurrent_version_expiration {
      days = var.retention_days_glacier_to_delete
    }
  }
}
