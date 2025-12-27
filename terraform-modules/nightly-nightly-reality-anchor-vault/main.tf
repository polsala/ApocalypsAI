resource "aws_s3_bucket" "reality_anchor_vault" {
  bucket = var.bucket_name
  tags   = merge(var.tags, {
    Environment = var.environment
    ManagedBy   = "ApocalypsAI-RealityAnchor"
  })
  object_lock_enabled = true # CRITICAL: Object Lock must be enabled at bucket creation.
}

resource "aws_s3_bucket_versioning" "reality_anchor_vault_versioning" {
  bucket = aws_s3_bucket.reality_anchor_vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_object_lock_configuration" "reality_anchor_vault_object_lock" {
  bucket = aws_s3_bucket.reality_anchor_vault.id
  rule {
    default_retention {
      mode = "COMPLIANCE" # Prevents any user, including the root user, from deleting or overwriting an object version until the retention period expires.
      days = var.retention_days
    }
  }
}

resource "aws_s3_bucket_acl" "reality_anchor_vault_acl" {
  bucket = aws_s3_bucket.reality_anchor_vault.id
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "reality_anchor_vault_public_access_block" {
  bucket = aws_s3_bucket.reality_anchor_vault.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "reality_anchor_vault_encryption" {
  bucket = aws_s3_bucket.reality_anchor_vault.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
