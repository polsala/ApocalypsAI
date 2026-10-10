resource "aws_s3_bucket" "whisper_vault" {
  bucket = "${var.bucket_name_prefix}${random_id.suffix.hex}"

  tags = {
    Name        = "${var.bucket_name_prefix}vault"
    Environment = "apocalypsai-community"
    ManagedBy   = "ApocalypsAI-Integrator"
  }
}

resource "random_id" "suffix" {
  byte_length = 8
}

resource "aws_s3_bucket_acl" "whisper_vault_acl" {
  bucket = aws_s3_bucket.whisper_vault.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "whisper_vault_versioning" {
  bucket = aws_s3_bucket.whisper_vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "whisper_vault_sse" {
  bucket = aws_s3_bucket.whisper_vault.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "whisper_vault_lifecycle" {
  bucket = aws_s3_bucket.whisper_vault.id

  rule {
    id     = "expire-old-whispers"
    status = "Enabled"

    expiration {
      days = var.retention_days
    }

    noncurrent_version_expiration {
      noncurrent_days = var.retention_days
    }
  }
}
