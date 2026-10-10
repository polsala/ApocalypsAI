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

resource "random_integer" "radiation" {
  min = 1
  max = 10
}

resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name

  tags = {
    "RadiationLevel" = random_integer.radiation.result
    "CreatedBy"      = "nightly‑apocalypse‑safehouse‑s3"
  }
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
    id     = "expire‑non‑current"
    status = "Enabled"

    noncurrent_version_expiration {
      days = 30
    }
  }
}
