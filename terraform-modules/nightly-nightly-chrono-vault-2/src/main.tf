resource "aws_s3_bucket" "chrono_vault" {
  bucket = var.bucket_name
  acl    = "private" # Best practice, though Block Public Access is more robust

  tags = {
    Name        = var.bucket_name
    Environment = "production" # Example tag
    ManagedBy   = "ApocalypsAI"
  }
}

resource "aws_s3_bucket_versioning" "chrono_vault_versioning" {
  bucket = aws_s3_bucket.chrono_vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "chrono_vault_encryption" {
  bucket = aws_s3_bucket.chrono_vault.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = var.kms_key_id == null ? "AES256" : "aws:kms"
      kms_master_key_id = var.kms_key_id
    }
  }
}

resource "aws_s3_bucket_public_access_block" "chrono_vault_public_access_block" {
  bucket = aws_s3_bucket.chrono_vault.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "chrono_vault_lifecycle" {
  bucket = aws_s3_bucket.chrono_vault.id

  rule {
    id     = "archive_and_expire"
    status = "Enabled"

    transition {
      days          = var.transition_days_standard_ia
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = var.transition_days_glacier
      storage_class = "GLACIER"
    }

    noncurrent_version_transition {
      days          = var.expiration_days_noncurrent_versions
      storage_class = "GLACIER"
    }

    noncurrent_version_expiration {
      days = var.expiration_days_noncurrent_versions * 2 # Expire non-current versions after a longer period
    }
  }
}

resource "aws_s3_bucket_logging" "chrono_vault_logging" {
  count = var.enable_access_logging ? 1 : 0

  bucket        = aws_s3_bucket.chrono_vault.id
  target_bucket = var.log_bucket_name
  target_prefix = "log/${var.bucket_name}/"
}
