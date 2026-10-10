resource "aws_s3_bucket" "echo_chamber" {
  bucket_prefix = var.prefix
  acl           = "private" # Best practice for private storage

  tags = {
    Name        = "${var.prefix}-temporal-echo-chamber"
    Environment = "ApocalypsAI"
    Purpose     = "TemporalEchoChamber"
  }
}

resource "aws_s3_bucket_versioning" "echo_chamber_versioning" {
  bucket = aws_s3_bucket.echo_chamber.id
  versioning_configuration {
    status = "Enabled" # Recommended for lifecycle rules to manage all versions
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "echo_chamber_lifecycle" {
  bucket = aws_s3_bucket.echo_chamber.id

  rule {
    id     = "expire_current_echoes"
    status = "Enabled"

    expiration {
      days = var.retention_days
    }

    # Clean up incomplete multipart uploads to prevent orphaned parts
    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }

  rule {
    id     = "expire_old_noncurrent_echoes"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = var.retention_days
    }
  }
}
