resource "aws_s3_bucket" "time_capsule" {
  bucket = var.bucket_name
  acl    = "private" # Ensure private access

  versioning {
    enabled = true
  }

  object_lock_configuration {
    object_lock_enabled = "Enabled"
    rule {
      default_retention {
        mode  = var.object_lock_mode
        days  = var.object_lock_days
      }
    }
  }

  lifecycle_rule {
    id      = "deep_archive_transition"
    enabled = true

    transition {
      days          = var.archive_transition_days
      storage_class = "GLACIER_DEEP_ARCHIVE"
    }

    # For a time capsule, we generally don't want objects to expire, only transition.
    # Omitting the expiration block means objects will not expire.
  }

  tags = merge(var.tags, {
    "ManagedBy" = "ApocalypsAI-NightlyIntegrator"
    "Purpose"   = "DigitalTimeCapsule"
  })
}

resource "aws_s3_bucket_public_access_block" "time_capsule_block_public_access" {
  bucket = aws_s3_bucket.time_capsule.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "time_capsule_encryption" {
  bucket = aws_s3_bucket.time_capsule.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
