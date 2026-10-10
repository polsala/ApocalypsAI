terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "expire-noncurrent"
    enabled = true

    noncurrent_version_expiration {
      days = 30
    }
  }

  tags = {
    Purpose = "SafehouseData"
  }
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.safehouse.arn
}
