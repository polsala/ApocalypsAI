resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

resource "aws_s3_bucket" "bunker" {
  bucket = "${var.bucket_name_prefix}-${random_string.bucket_suffix.result}"
  region = var.region

  tags = merge(
    {
      "ManagedBy" = "ApocalypsAI"
      "Utility"   = "DigitalDoomsdayBunker"
    },
    var.tags
  )
}

resource "aws_s3_bucket_ownership_controls" "bunker_ownership_controls" {
  bucket = aws_s3_bucket.bunker.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "bunker_public_access_block" {
  bucket = aws_s3_bucket.bunker.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_acl" "bunker_acl" {
  depends_on = [
    aws_s3_bucket_ownership_controls.bunker_ownership_controls,
    aws_s3_bucket_public_access_block.bunker_public_access_block,
  ]

  bucket = aws_s3_bucket.bunker.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "bunker_versioning" {
  bucket = aws_s3_bucket.bunker.id
  configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bunker_sse" {
  bucket = aws_s3_bucket.bunker.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "bunker_lifecycle" {
  bucket = aws_s3_bucket.bunker.id

  rule {
    id     = "glacier_transition_and_expiration"
    status = "Enabled"

    noncurrent_version_transition {
      days          = var.glacier_transition_days
      storage_class = "DEEP_ARCHIVE"
    }

    noncurrent_version_expiration {
      days = var.glacier_expiration_days
    }
  }
}
