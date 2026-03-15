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
  # In tests we use a mock endpoint; no real credentials needed.
  region = var.aws_region
}

resource "random_pet" "name" {
  length    = 2
  separator = "-"
}

resource "aws_s3_bucket" "safehouse" {
  bucket        = "${var.bucket_prefix}-${random_pet.name.id}"
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
    id      = "expire-old-objects"
    enabled = true

    expiration {
      days = 30
    }
  }

  tags = {
    Purpose = "Apocalypse Safehouse"
  }
}
