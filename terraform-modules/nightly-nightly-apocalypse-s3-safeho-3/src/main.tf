terraform {
  required_version = ">= 1.0.0"
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

variable "enable_public_access" {
  description = "Allow public read access"
  type        = bool
  default     = false
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  force_destroy = true

  lifecycle_rule {
    id      = "glacier-transition"
    enabled = true

    transition {
      days          = 30
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }

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

  acl = var.enable_public_access ? "public-read" : "private"
}
