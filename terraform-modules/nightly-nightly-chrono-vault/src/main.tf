resource "aws_s3_bucket" "chrono_vault" {
  bucket = var.bucket_name
  acl    = "private" # Ensure private by default

  versioning {
    enabled = true # Essential for a survival cache
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm     = var.encryption_algorithm
        kms_master_key_id = var.encryption_algorithm == "aws:kms" ? var.kms_key_arn : null
      }
    }
  }

  # Block all public access by default
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  # Lifecycle rules for old versions
  lifecycle_rule {
    id      = "archive_old_versions"
    enabled = true

    noncurrent_version_transition {
      days          = var.noncurrent_version_transition_days
      storage_class = "GLACIER"
    }

    noncurrent_version_expiration {
      days = var.noncurrent_version_expiration_days
    }
  }

  tags = merge(var.tags, {
    "ManagedBy" = "ApocalypsAI-ChronoVault"
    "Purpose"   = "DigitalSurvivalCache"
  })
}

resource "aws_s3_bucket_policy" "chrono_vault_policy" {
  count  = var.attach_policy ? 1 : 0
  bucket = aws_s3_bucket.chrono_vault.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "RequireTLS"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          "${aws_s3_bucket.chrono_vault.arn}/*",
          aws_s3_bucket.chrono_vault.arn
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}

# Optional: Static website hosting for a manifest
resource "aws_s3_bucket_website_configuration" "chrono_vault_website" {
  count  = var.enable_static_website ? 1 : 0
  bucket = aws_s3_bucket.chrono_vault.id

  index_document {
    suffix = var.website_index_document
  }

  error_document {
    key = var.website_error_document
  }
}

output "bucket_id" {
  description = "The ID of the S3 bucket."
  value       = aws_s3_bucket.chrono_vault.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.chrono_vault.arn
}

output "bucket_regional_domain_name" {
  description = "The regional domain name of the S3 bucket."
  value       = aws_s3_bucket.chrono_vault.bucket_regional_domain_name
}

output "website_endpoint" {
  description = "The S3 bucket website endpoint (if enabled)."
  value       = var.enable_static_website ? aws_s3_bucket_website_configuration.chrono_vault_website[0].website_endpoint : null
}
