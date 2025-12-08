resource "aws_kms_key" "cipher_lock" {
  description             = "KMS key for the Digital Data Bunker's cipher lock"
  deletion_window_in_days = 7
  enable_key_rotation     = true
  tags                    = var.tags
}

resource "aws_kms_alias" "cipher_lock_alias" {
  name          = "alias/${var.bunker_name_prefix}-cipher-lock"
  target_key_id = aws_kms_key.cipher_lock.id
}

resource "aws_s3_bucket" "data_bunker" {
  bucket        = "${var.bunker_name_prefix}-${random_id.suffix.hex}"
  force_destroy = false # Set to true for easy cleanup in non-prod environments
  tags          = var.tags
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket_acl" "data_bunker_acl" {
  bucket = aws_s3_bucket.data_bunker.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "data_bunker_versioning" {
  bucket = aws_s3_bucket.data_bunker.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_bunker_sse" {
  bucket = aws_s3_bucket.data_bunker.id
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.cipher_lock.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "data_bunker_public_access" {
  bucket                  = aws_s3_bucket.data_bunker.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "data_bunker_lifecycle" {
  bucket = aws_s3_bucket.data_bunker.id
  rule {
    id     = "glacier_transition"
    status = "Enabled"
    transition {
      days          = 30
      storage_class = "GLACIER"
    }
    expiration {
      days = 3650 # Expire objects after 10 years in Glacier
    }
  }
}
