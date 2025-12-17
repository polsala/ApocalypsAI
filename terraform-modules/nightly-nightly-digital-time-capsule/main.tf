resource "aws_s3_bucket" "time_capsule" {
  bucket = var.bucket_name
  tags   = var.tags

  # Ensure public access is blocked by default
  # The `acl` argument is deprecated for new buckets, `aws_s3_bucket_public_access_block` is preferred.
  # Keeping it for broader compatibility, but the dedicated resource below is more robust.
  acl = "private"

  # Enable versioning for historical preservation
  versioning {
    enabled = true
  }

  # Enable server-side encryption by default
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  # Lifecycle rules for digital burial (transition to cheaper storage)
  lifecycle_rule {
    id      = "transition_to_glacier"
    enabled = true

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    # Optional: expire old noncurrent versions after a very long time
    noncurrent_version_transition {
      days          = 365
      storage_class = "GLACIER"
    }
    noncurrent_version_expiration {
      days = 3650 # Expire noncurrent versions after 10 years
    }
  }
}

# Explicitly block all public access to the bucket
resource "aws_s3_bucket_public_access_block" "time_capsule_block" {
  bucket = aws_s3_bucket.time_capsule.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
