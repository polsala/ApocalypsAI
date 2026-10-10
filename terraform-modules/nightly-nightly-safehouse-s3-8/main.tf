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
  # Configuration is expected to be provided via environment variables or shared config
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
    id      = "glacier-transition"
    enabled = true

    transition {
      days          = 30
      storage_class = "GLACIER"
    }

    expiration {
      days = 3650
    }
  }

  tags = {
    Purpose = "Apocalypse Safehouse"
  }
}

resource "random_password" "access" {
  length  = 16
  special = true
  override_characters = "!@#$%^&*()-_=+[]{}"
}

resource "aws_ssm_parameter" "password" {
  name  = var.ssm_parameter_name
  type  = "SecureString"
  value = random_password.access.result
}
