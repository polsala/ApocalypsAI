resource "aws_s3_bucket" "ephemeral_beacon" {
  bucket_prefix = var.bucket_prefix
  acl           = "private" # Secure by default

  # Block all public access for security
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  versioning {
    enabled = false
  }

  lifecycle_rule {
    id     = "ephemeral-object-expiration"
    enabled = true

    expiration {
      days = var.expiration_days
    }
  }

  tags = {
    Name        = "${var.bucket_prefix}-ephemeral-beacon"
    Environment = "ApocalypsAI"
    ManagedBy   = "Terraform"
    Purpose     = "EphemeralMessageBeacon"
  }
}

resource "aws_s3_bucket_ownership_controls" "ephemeral_beacon_ownership" {
  bucket = aws_s3_bucket.ephemeral_beacon.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "ephemeral_beacon_public_access_block" {
  bucket = aws_s3_bucket.ephemeral_beacon.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
