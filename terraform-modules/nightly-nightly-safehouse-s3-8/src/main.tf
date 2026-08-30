terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws    = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

provider "aws" {
  # The region can be overridden via the AWS_DEFAULT_REGION env var.
  region = "us-east-1"
}

variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)"
  type        = string
}

# Generate a whimsical radiation level (1‑10)
resource "random_integer" "radiation" {
  min = 1
  max = 10
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  tags = {
    "Purpose"          = "Post‑Apocalyptic Safe‑House"
    "Radiation‑Level" = random_integer.radiation.result
  }
}

resource "aws_s3_bucket_versioning" "safehouse_versioning" {
  bucket = aws_s3_bucket.safehouse.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "safehouse_enc" {
  bucket = aws_s3_bucket.safehouse.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "safehouse_lifecycle" {
  bucket = aws_s3_bucket.safehouse.id

  rule {
    id     = "expire‑old‑objects"
    status = "Enabled"

    expiration {
      days = 30
    }
  }
}

output "bucket_arn" {
  description = "ARN of the created bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "radiation_level" {
  description = "Random radiation level (1‑10)"
  value       = random_integer.radiation.result
}
