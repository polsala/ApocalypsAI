terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  # In tests we use a dummy region; real deployments should override as needed.
  region = "us-east-1"
}

variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)."
  type        = string
}

variable "enable_encryption" {
  description = "Enable AES‑256 server‑side encryption."
  type        = bool
  default     = false
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "expire-old-objects"
    enabled = true
    expiration {
      days = 365
    }
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
    # Only create the block if encryption is requested.
    # Terraform's `count` meta‑argument cannot be used inside a nested block, so we use a conditional expression.
    # The block will be ignored when `enable_encryption` is false because the values are the same as defaults.
  }

  # Conditional creation of encryption block
  dynamic "server_side_encryption_configuration" {
    for_each = var.enable_encryption ? [1] : []
    content {
      rule {
        apply_server_side_encryption_by_default {
          sse_algorithm = "AES256"
        }
      }
    }
  }
}

output "bucket_id" {
  description = "The ID of the created bucket."
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the created bucket."
  value       = aws_s3_bucket.safehouse.arn
}
