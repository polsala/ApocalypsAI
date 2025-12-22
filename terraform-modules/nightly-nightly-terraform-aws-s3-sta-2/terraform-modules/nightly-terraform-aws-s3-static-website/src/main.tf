variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)."
  type        = string
}

variable "index_document" {
  description = "The index document for the website."
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "The error document for the website."
  type        = string
  default     = "error.html"
}

variable "public_read" {
  description = "If true, grants public read access to the bucket."
  type        = bool
  default     = false
}

resource "aws_s3_bucket" "website_bucket" {
  bucket = var.bucket_name
  acl    = var.public_read ? "public-read" : "private"

  tags = {
    Name        = "Apocalypse Oasis"
    Environment = "Production"
  }
}

resource "aws_s3_bucket_website_configuration" "website_config" {
  bucket = aws_s3_bucket.website_bucket.id

  index_document {
    suffix = var.index_document
  }

  error_document {
    key = var.error_document
  }
}

output "bucket_id" {
  description = "The ID of the created S3 bucket."
  value       = aws_s3_bucket.website_bucket.id
}

output "website_endpoint" {
  description = "The website endpoint URL."
  value       = aws_s3_bucket.website_bucket.website_endpoint
}
