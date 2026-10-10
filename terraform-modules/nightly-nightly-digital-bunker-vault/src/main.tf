# This module provisions a secure, versioned AWS S3 bucket for critical digital survival data.

# --- Resources ---

resource "aws_s3_bucket" "bunker_vault" {
  bucket = var.bucket_name
  tags   = var.tags

  # Ensure bucket is created with a unique name if not provided, or use the provided one.
  # This is handled by the `bucket_name` variable.
}

resource "aws_s3_bucket_versioning" "bunker_vault_versioning" {
  bucket = aws_s3_bucket.bunker_vault.id
  versioning_configuration {
    status = "Enabled" # Essential for historical data and recovery
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bunker_vault_sse" {
  bucket = aws_s3_bucket.bunker_vault.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256" # Default encryption for data at rest
    }
  }
}

resource "aws_s3_bucket_public_access_block" "bunker_vault_public_access" {
  bucket = aws_s3_bucket.bunker_vault.id

  block_public_acls       = true # Prevent new public ACLs
  block_public_and_cross_account_access = true # Prevent public and cross-account access
  ignore_public_acls      = true # Ignore existing public ACLs
  restrict_public_buckets = true # Restrict access to buckets with public policies
}

resource "aws_s3_bucket_lifecycle_configuration" "bunker_vault_lifecycle" {
  count  = var.enable_glacier_transition ? 1 : 0 # Only create if enabled
  bucket = aws_s3_bucket.bunker_vault.id

  rule {
    id     = "old-versions-to-glacier"
    status = "Enabled"

    # Transition noncurrent versions to GLACIER after 30 days
    noncurrent_version_transition {
      days          = 30
      storage_class = "GLACIER"
    }

    # Expire noncurrent versions after 365 days (optional, can be adjusted)
    noncurrent_version_expiration {
      days = 365
    }
  }
}

# --- Variables ---

variable "bucket_name" {
  description = "The name of the S3 bucket. Must be globally unique."
  type        = string
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}

variable "enable_glacier_transition" {
  description = "Set to true to enable a lifecycle rule that transitions old object versions to Glacier after 30 days and expires them after 365 days."
  type        = bool
  default     = false
}

# --- Outputs ---

output "bucket_id" {
  description = "The ID (name) of the S3 bucket."
  value       = aws_s3_bucket.bunker_vault.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.bunker_vault.arn
}

output "bucket_domain_name" {
  description = "The S3 bucket's regional domain name."
  value       = aws_s3_bucket.bunker_vault.bucket_regional_domain_name
}
