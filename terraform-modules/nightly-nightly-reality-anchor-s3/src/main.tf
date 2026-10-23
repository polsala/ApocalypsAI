resource "aws_s3_bucket" "reality_anchor" {
  bucket_prefix = var.bucket_name_prefix
  tags          = var.tags

  # Enable versioning for data integrity and recovery
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

  # Ensure bucket is private by default
  acl = "private"
}

resource "aws_s3_bucket_public_access_block" "reality_anchor_block" {
  bucket = aws_s3_bucket.reality_anchor.id

  # Block all public access for security
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
