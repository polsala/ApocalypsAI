terraform {
  required_version = ">= 1.0"
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

variable "index_document" {
  description = "Index document for website"
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "Error document for website"
  type        = string
  default     = "error.html"
}

variable "versioning" {
  description = "Enable versioning"
  type        = bool
  default     = false
}

resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name

  website {
    index_document = var.index_document
    error_document = var.error_document
  }

  versioning {
    enabled = var.versioning
  }

  tags = {
    ManagedBy = "nightly-terraform-s3-website"
  }
}

output "bucket_id" {
  description = "ID of the created bucket"
  value       = aws_s3_bucket.this.id
}

output "website_endpoint" {
  description = "Website endpoint URL"
  value       = aws_s3_bucket.this.website_endpoint
}
