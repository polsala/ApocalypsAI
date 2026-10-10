resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

resource "aws_s3_bucket" "chronicle_vault" {
  bucket = "${var.bucket_name_prefix}-${random_string.bucket_suffix.result}"
  tags   = var.tags
}

resource "aws_s3_bucket_acl" "chronicle_vault_acl" {
  bucket = aws_s3_bucket.chronicle_vault.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "chronicle_vault_versioning" {
  bucket = aws_s3_bucket.chronicle_vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "chronicle_vault_sse" {
  bucket = aws_s3_bucket.chronicle_vault.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "chronicle_vault_public_access_block" {
  bucket = aws_s3_bucket.chronicle_vault.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "chronicle_vault_lifecycle" {
  bucket = aws_s3_bucket.chronicle_vault.id

  rule {
    id     = "glacier_deep_archive_noncurrent_versions"
    status = "Enabled"

    noncurrent_version_transition {
      days          = var.glacier_transition_days
      storage_class = "DEEP_ARCHIVE"
    }

    noncurrent_version_expiration {
      days = var.glacier_transition_days + 30 # Expire noncurrent versions after they've been in DEEP_ARCHIVE for 30 days
    }
  }

  rule {
    id     = "abort_incomplete_multipart_uploads"
    status = "Enabled"

    abort_incomplete_multipart_upload_days = var.multipart_upload_expiration_days
  }

  rule {
    id     = "delete_expired_object_delete_markers"
    status = "Enabled"

    expired_object_delete_markers = true
  }
}
