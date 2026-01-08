terraform {
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
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "bucket_name" {
  type = string
}

variable "expiration_days" {
  type    = number
  default = 365
}

variable "password_length" {
  type    = number
  default = 32
}

resource "aws_s3_bucket" "safehouse" {
  bucket        = var.bucket_name
  force_destroy = true
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
    id     = "expire-old-objects"
    status = "Enabled"
    filter {}
    expiration {
      days = var.expiration_days
    }
  }
}

resource "random_password" "vault" {
  length  = var.password_length
  special = true
}

output "bucket_arn" {
  description = "ARN of the created S3 bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "vault_password" {
  description = "Randomly generated vault password"
  value       = random_password.vault.result
}
