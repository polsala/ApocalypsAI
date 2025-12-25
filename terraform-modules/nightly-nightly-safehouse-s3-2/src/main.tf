terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "tags" {
  description = "Tags for the bucket"
  type        = map(string)
  default     = {}
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  tags   = var.tags

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  lifecycle_rule {
    id      = "expire-old-objects"
    enabled = true

    expiration {
      days = 30
    }
  }
}

output "bucket_id" {
  description = "The ID of the S3 bucket"
  value       = aws_s3_bucket.safehouse.id
}
