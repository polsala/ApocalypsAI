resource "random_id" "bucket_suffix" {
  byte_length = 8
}

resource "aws_s3_bucket" "message_drop" {
  bucket = "${var.bucket_name_prefix}${random_id.bucket_suffix.hex}"

  tags = var.tags

  # Enforce private access
  acl = "private"

  # Block all public access
  # https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id = "auto-delete-old-messages"

    enabled = true

    expiration {
      days = var.message_retention_days
    }

    # Optionally, clean up incomplete multipart uploads
    abort_incomplete_multipart_upload_days = 7
  }
}
