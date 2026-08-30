resource "random_id" "id" {
  byte_length = 8
}

resource "aws_s3_bucket" "whispering_log_archive" {
  bucket = var.bucket_name == "" ? "whispering-log-archive-${random_id.id.hex}" : var.bucket_name

  tags = var.tags
}

resource "aws_s3_bucket_ownership_controls" "whispering_log_archive" {
  bucket = aws_s3_bucket.whispering_log_archive.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "whispering_log_archive" {
  depends_on = [aws_s3_bucket_ownership_controls.whispering_log_archive]

  bucket = aws_s3_bucket.whispering_log_archive.id
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "whispering_log_archive" {
  bucket = aws_s3_bucket.whispering_log_archive.id

  block_public_acls       = true
  block_public_and_cross_account_access = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "whispering_log_archive" {
  bucket = aws_s3_bucket.whispering_log_archive.id

  rule {
    id     = "expire-after-retention"
    status = "Enabled"

    expiration {
      days = var.retention_days
    }
  }
}
