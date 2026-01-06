terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  # In a real environment, configure region and credentials.
  # For testing, this provider block can be left empty.
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "expire-old-objects"
    enabled = true

    expiration {
      days = 30
    }

    filter {}
  }

  tags = {
    Purpose = "Safehouse Supplies"
  }
}
