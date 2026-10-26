resource "aws_s3_bucket" "chrono_vault" {
  bucket = var.bucket_name
  acl    = "private" # Default to private, users can override with specific policies

  tags = merge(
    {
      "ManagedBy" = "ApocalypsAI-ChronoVault"
    },
    var.tags
  )
}

resource "aws_s3_bucket_versioning" "chrono_vault_versioning" {
  bucket = aws_s3_bucket.chrono_vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "chrono_vault_lifecycle" {
  bucket = aws_s3_bucket.chrono_vault.id

  rule {
    id     = "temporal-stasis-and-entropic-decay"
    status = "Enabled"

    transition {
      days          = var.temporal_stasis_days
      storage_class = "GLACIER"
    }

    dynamic "expiration" {
      for_each = var.entropic_decay_days != null ? [1] : []
      content {
        days = var.entropic_decay_days
      }
    }
  }
}
