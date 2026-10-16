resource "aws_s3_bucket" "echo_chamber" {
  bucket = var.bucket_name
  tags   = var.tags
}

resource "aws_s3_bucket_versioning" "echo_chamber_versioning" {
  bucket = aws_s3_bucket.echo_chamber.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "echo_chamber_lifecycle" {
  bucket = aws_s3_bucket.echo_chamber.id

  rule {
    id     = "echo-chamber-retention"
    status = "Enabled"

    noncurrent_version_transition {
      storage_class = "GLACIER_IR"
      days          = 30
    }

    noncurrent_version_transition {
      storage_class = "GLACIER"
      days          = 90
    }

    noncurrent_version_expiration {
      days = 3650 # Expire noncurrent versions after 10 years
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}
