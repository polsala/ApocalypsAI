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

resource "random_id" "suffix" {
  byte_length = 4
}

locals {
  final_bucket_name = var.bucket_name != "" ? var.bucket_name : "apocalypse-safehouse-${random_id.suffix.hex}"
}

resource "aws_s3_bucket" "safehouse" {
  bucket = local.final_bucket_name

  force_destroy = true

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
    id      = "expire-old-versions"
    enabled = true

    noncurrent_version_expiration {
      days = 30
    }
  }

  tags = {
    Purpose = "Post‑Apocalyptic Safehouse"
  }
}
