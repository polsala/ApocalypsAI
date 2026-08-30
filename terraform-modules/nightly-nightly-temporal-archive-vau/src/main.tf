resource "aws_s3_bucket" "archive_vault" {
  bucket = var.bucket_name
  acl    = "private" # Best practice, combined with block_public_access

  tags = merge(var.tags, {
    "ManagedBy" = "ApocalypsAI-TemporalArchiveVault"
  })
}

resource "aws_s3_bucket_versioning" "archive_vault_versioning" {
  bucket = aws_s3_bucket.archive_vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "archive_vault_sse" {
  bucket = aws_s3_bucket.archive_vault.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "archive_vault_public_access_block" {
  bucket                  = aws_s3_bucket.archive_vault.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "archive_vault_lifecycle" {
  bucket = aws_s3_bucket.archive_vault.id

  rule {
    id     = "archive_rule"
    status = "Enabled"

    transition {
      days          = var.glacier_ir_transition_days
      storage_class = "GLACIER_IR"
    }

    transition {
      days          = var.deep_archive_transition_days
      storage_class = "DEEP_ARCHIVE"
    }

    dynamic "expiration" {
      for_each = var.expiration_days != null ? [1] : []
      content {
        days = var.expiration_days
      }
    }

    noncurrent_version_transition {
      days          = var.glacier_ir_transition_days
      storage_class = "GLACIER_IR"
    }

    noncurrent_version_transition {
      days          = var.deep_archive_transition_days
      storage_class = "DEEP_ARCHIVE"
    }

    noncurrent_version_expiration {
      days = var.expiration_days != null ? var.expiration_days : null
    }
  }
}
