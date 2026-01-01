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

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  tags   = var.tags
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
    id     = "expire-noncurrent"
    status = "Enabled"
    noncurrent_version_expiration {
      days = 30
    }
  }
}

resource "random_password" "access_token" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret" "access_secret" {
  count = var.enable_secret ? 1 : 0
  name  = "${var.bucket_name}-access-token"
}

resource "aws_secretsmanager_secret_version" "access_secret_version" {
  count         = var.enable_secret ? 1 : 0
  secret_id     = aws_secretsmanager_secret.access_secret[0].id
  secret_string = random_password.access_token.result
}
