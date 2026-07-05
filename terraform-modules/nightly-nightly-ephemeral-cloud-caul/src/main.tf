terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # Specify a compatible version
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0" # Specify a compatible version
    }
  }
}

resource "aws_s3_bucket" "ephemeral_bucket" {
  bucket = "${var.resource_name_prefix}-${random_id.bucket_suffix.hex}"
  acl    = "private" # Default to private for security

  tags = merge(
    var.tags,
    {
      "ManagedBy" = "ApocalypsAI-EphemeralCauldron"
      "ExpiresAfterDays" = var.ttl_days
    }
  )
}

resource "aws_s3_bucket_lifecycle_configuration" "ephemeral_lifecycle" {
  bucket = aws_s3_bucket.ephemeral_bucket.id

  rule {
    id     = "expire-all-objects"
    status = "Enabled"

    expiration {
      days = var.ttl_days
    }
  }
}

# A random suffix to ensure bucket name uniqueness
resource "random_id" "bucket_suffix" {
  byte_length = 8
}
