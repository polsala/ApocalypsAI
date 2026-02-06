terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  # Dummy credentials for offline validation; no real calls will be made.
  access_key                     = "mock"
  secret_key                     = "mock"
  region                         = "us-east-1"
  skip_credentials_validation    = true
  skip_requesting_account_id     = true
  skip_get_ec2_platforms         = true
  skip_metadata_api_check        = true
  s3_use_path_style              = true
  endpoints {
    s3 = "http://localhost:4566" # Mock S3 endpoint – not required for validation
  }
}

provider "random" {}

variable "bucket_name_prefix" {
  description = "Prefix for the bucket name."
  type        = string
}

variable "tags" {
  description = "Tags to apply to the bucket."
  type        = map(string)
  default     = {}
}

resource "random_pet" "suffix" {
  length = 2
}

resource "aws_s3_bucket" "safehouse" {
  bucket = "${var.bucket_name_prefix}-${random_pet.suffix.id}"
  tags   = var.tags

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
}

output "bucket_id" {
  description = "The name of the bucket."
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the bucket."
  value       = aws_s3_bucket.safehouse.arn
}
