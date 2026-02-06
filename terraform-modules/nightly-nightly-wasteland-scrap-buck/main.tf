terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check      = true
}

resource "aws_s3_bucket" "scrap" {
  bucket = var.bucket_name

  lifecycle_rule {
    id      = "expire-old-scrap"
    enabled = true

    expiration {
      days = 30
    }

    filter {}
  }
}
