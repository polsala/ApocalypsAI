resource "aws_s3_bucket" "cosmic_dust" {
  bucket = "${var.bucket_name_prefix}-${random_id.suffix.hex}"

  tags = {
    Environment = var.environment
    ManagedBy   = "ApocalypsAI-NightlyIntegrator"
    Purpose     = "CosmicDustCollection"
  }
}

resource "random_id" "suffix" {
  byte_length = 8
}

resource "aws_s3_bucket_versioning" "cosmic_dust" {
  bucket = aws_s3_bucket.cosmic_dust.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "cosmic_dust" {
  bucket = aws_s3_bucket.cosmic_dust.id

  rule {
    id     = "dust-cleanup"
    status = "Enabled"

    transition {
      days          = var.transition_days_to_ia
      storage_class = "GLACIER_IR" # Using GLACIER_IR for cost-effective infrequent access
    }

    expiration {
      days = var.retention_days
    }
  }
}

resource "aws_s3_bucket_public_access_block" "cosmic_dust" {
  bucket = aws_s3_bucket.cosmic_dust.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "bucket_id" {
  description = "The ID (name) of the created S3 bucket."
  value       = aws_s3_bucket.cosmic_dust.id
}

output "bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.cosmic_dust.arn
}

output "bucket_domain_name" {
  description = "The domain name of the created S3 bucket."
  value       = aws_s3_bucket.cosmic_dust.bucket_domain_name
}
