terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
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
  region = var.region
}

# Generate a whimsical name if none supplied
resource "random_pet" "bucket_name" {
  length    = 2
  separator = "-"
}

locals {
  final_bucket_name = var.bucket_name != null ? var.bucket_name : random_pet.bucket_name.id
}

resource "aws_s3_bucket" "safehouse" {
  bucket = local.final_bucket_name
  force_destroy = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "cleanup-old-objects"
    enabled = true
    expiration {
      days = 30
    }
  }
}

resource "aws_s3_bucket_public_access_block" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id
  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls  = true
  restrict_public_buckets = true
}
