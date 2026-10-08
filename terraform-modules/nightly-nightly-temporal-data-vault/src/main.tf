resource "aws_s3_bucket" "vault" {
  bucket = var.bucket_name
  acl    = "private" # Best practice: use bucket policies for fine-grained access

  tags = {
    Environment = var.environment
    Project     = var.project
    ManagedBy   = "ApocalypsAI-TemporalDataVault"
  }
}

resource "aws_s3_bucket_versioning" "vault_versioning" {
  bucket = aws_s3_bucket.vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "vault_encryption" {
  bucket = aws_s3_bucket.vault.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "vault_lifecycle" {
  bucket = aws_s3_bucket.vault.id

  rule {
    id     = "noncurrent_version_transition_and_expiration"
    status = "Enabled"

    noncurrent_version_transition {
      days          = var.retention_days_to_glacier
      storage_class = "GLACIER"
    }

    noncurrent_version_expiration {
      days = var.expiration_days_noncurrent
    }
  }
}

resource "aws_s3_bucket_logging" "vault_logging" {
  count = var.enable_access_logging ? 1 : 0

  bucket        = aws_s3_bucket.vault.id
  target_bucket = var.logging_bucket_name
  target_prefix = "log/${var.bucket_name}/"
}
