terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws    = { source = "hashicorp/aws", version = ">= 4.0" }
    random = { source = "hashicorp/random", version = ">= 3.0" }
  }
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  tags   = var.tags
}

resource "aws_s3_bucket_versioning" "safehouse_versioning" {
  bucket = aws_s3_bucket.safehouse.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "safehouse_lifecycle" {
  bucket = aws_s3_bucket.safehouse.id
  rule {
    id     = "move-to-glacier"
    status = "Enabled"
    filter {}
    transition {
      days          = 30
      storage_class = "GLACIER"
    }
    expiration {
      days = 365
    }
    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "GLACIER"
    }
    noncurrent_version_expiration {
      noncurrent_days = 365
    }
  }
}

# Generate a random password – in a real scenario you would store this in Secrets Manager
resource "random_password" "access" {
  length  = var.password_length
  special = var.password_special
}

output "bucket_id" {
  description = "The ID of the created S3 bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "ARN of the bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "generated_password" {
  description = "Randomly generated password (for demo purposes)"
  value       = random_password.access.result
  sensitive   = true
}
