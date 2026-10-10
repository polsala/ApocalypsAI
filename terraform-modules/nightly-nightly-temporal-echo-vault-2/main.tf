resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket" "temporal_echo_vault" {
  bucket = "${var.bucket_name_prefix}-${random_string.bucket_suffix.result}"

  tags = var.tags
}

resource "aws_s3_bucket_acl" "temporal_echo_vault_acl" {
  bucket = aws_s3_bucket.temporal_echo_vault.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "temporal_echo_vault_versioning" {
  bucket = aws_s3_bucket.temporal_echo_vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "temporal_echo_vault_sse" {
  bucket = aws_s3_bucket.temporal_echo_vault.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "temporal_echo_vault_public_access_block" {
  bucket = aws_s3_bucket.temporal_echo_vault.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
