terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "aws" {
  # In tests we use a dummy region; real usage expects proper credentials.
  region = var.aws_region
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "expire-old-versions"
    enabled = true

    noncurrent_version_expiration {
      days = 365
    }
  }

  tags = {
    Purpose = "Safehouse"
  }
}

resource "random_password" "safehouse_pwd" {
  length  = 16
  special = true
}

resource "aws_secretsmanager_secret" "safehouse_secret" {
  count = var.enable_secret ? 1 : 0
  name  = "${var.bucket_name}-access"
}

resource "aws_secretsmanager_secret_version" "safehouse_secret_version" {
  count         = var.enable_secret ? 1 : 0
  secret_id     = aws_secretsmanager_secret.safehouse_secret[0].id
  secret_string = jsonencode({
    password = random_password.safehouse_pwd.result
  })
}
