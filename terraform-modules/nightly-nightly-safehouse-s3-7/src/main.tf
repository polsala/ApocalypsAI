terraform {
  required_version = ">= 1.0.0"
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
  region = var.region
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

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
    id      = "expire-objects"
    enabled = true

    expiration {
      days = var.expiration_days
    }
  }
}

resource "random_password" "access" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret" "access_secret" {
  name = "${var.bucket_name}-access"
}

resource "aws_secretsmanager_secret_version" "access_secret_version" {
  secret_id     = aws_secretsmanager_secret.access_secret.id
  secret_string = random_password.access.result
}
