resource "aws_s3_bucket" "time_capsule" {
  bucket_prefix = var.bucket_name_prefix
  tags          = var.tags
}

resource "aws_s3_bucket_versioning" "time_capsule_versioning" {
  bucket = aws_s3_bucket.time_capsule.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "time_capsule_encryption" {
  bucket = aws_s3_bucket.time_capsule.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "time_capsule_public_access_block" {
  bucket                  = aws_s3_bucket.time_capsule.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "time_capsule_lifecycle" {
  count  = var.enable_lifecycle_rules ? 1 : 0
  bucket = aws_s3_bucket.time_capsule.id

  rule {
    id     = "archive_and_delete_old_versions"
    status = "Enabled"

    noncurrent_version_transition {
      days          = var.lifecycle_rule_days_to_glacier
      storage_class = "GLACIER_IR"
    }

    noncurrent_version_expiration {
      days = var.lifecycle_rule_days_to_delete
    }

    # Clean up incomplete multipart uploads
    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}
