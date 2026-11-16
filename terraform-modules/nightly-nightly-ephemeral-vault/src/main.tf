resource "aws_s3_bucket" "ephemeral_vault" {
  bucket_prefix = var.bucket_name_prefix
  acl           = "private" # Private by default

  tags = var.tags
}

resource "aws_s3_bucket_versioning" "ephemeral_vault_versioning" {
  bucket = aws_s3_bucket.ephemeral_vault.id
  versioning_configuration {
    status = "Disabled" # Versioning not typically needed for ephemeral data
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "ephemeral_vault_lifecycle" {
  bucket = aws_s3_bucket.ephemeral_vault.id

  rule {
    id     = "ephemeral_data_expiration"
    status = "Enabled"

    expiration {
      days = var.retention_days
    }
  }
}
