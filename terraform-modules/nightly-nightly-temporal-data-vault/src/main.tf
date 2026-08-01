resource "aws_s3_bucket" "vault" {
  bucket = var.bucket_name
  acl    = "private" # Ensure private access by default

  versioning {
    enabled = var.enable_versioning
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  # Block all public access by default
  # This is a best practice for secure S3 buckets
  # Users can override if needed, but module encourages secure defaults
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  tags = merge(
    var.tags,
    {
      "ManagedBy" = "ApocalypsAI-TemporalDataVault"
      "Purpose"   = "TemporalDataStorage"
    }
  )
}

resource "aws_s3_bucket_lifecycle_configuration" "vault_lifecycle" {
  count  = var.enable_lifecycle_rules ? 1 : 0
  bucket = aws_s3_bucket.vault.id

  rule {
    id     = "expire-old-noncurrent-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      days = var.noncurrent_version_expiration_days
    }

    # Optional: Transition current versions to infrequent access
    dynamic "transition" {
      for_each = var.transition_current_to_ia_days > 0 ? [1] : []
      content {
        days          = var.transition_current_to_ia_days
        storage_class = "STANDARD_IA"
      }
    }

    # Optional: Transition noncurrent versions to infrequent access
    dynamic "noncurrent_version_transition" {
      for_each = var.transition_noncurrent_to_ia_days > 0 ? [1] : []
      content {
        noncurrent_days = var.transition_noncurrent_to_ia_days
        storage_class   = "STANDARD_IA"
      }
    }
  }
}
