resource "aws_s3_bucket" "archive_vault" {
  bucket = var.bucket_name
  acl    = "private" # Best practice for private archives

  # Enable object lock at bucket creation if requested
  object_lock_enabled = var.enable_object_lock

  tags = {
    Environment = "ApocalypsAI-Archive"
    ManagedBy   = "NightlyTemporalArchiveVault"
  }
}

resource "aws_s3_bucket_versioning" "archive_vault_versioning" {
  bucket = aws_s3_bucket.archive_vault.id
  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Suspended"
  }
}

resource "aws_s3_bucket_object_lock_configuration" "archive_vault_object_lock" {
  # This resource configures the default retention *after* the bucket is created with object lock enabled.
  # It should only be applied if object lock is enabled on the bucket.
  count  = var.enable_object_lock ? 1 : 0
  bucket = aws_s3_bucket.archive_vault.id
  rule {
    default_retention {
      mode = var.retention_mode
      days = var.retention_period_days
    }
  }
  # Ensure this resource depends on the bucket being created with object lock enabled
  depends_on = [aws_s3_bucket.archive_vault]
}

# Block public access by default for security
resource "aws_s3_bucket_public_access_block" "archive_vault_public_access_block" {
  bucket = aws_s3_bucket.archive_vault.id

  block_public_acls       = true
  block_public_and_cross_account_access = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
