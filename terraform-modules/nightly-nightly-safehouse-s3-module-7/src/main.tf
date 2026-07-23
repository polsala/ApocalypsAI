terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                       = var.region
  access_key                   = "mock"
  secret_key                   = "mock"
  skip_credentials_validation  = true
  skip_metadata_api_check      = true
  s3_use_path_style            = true
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  versioning {
    enabled = true
  }

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

  tags = {
    Purpose = "Post-apocalyptic supplies"
  }
}
