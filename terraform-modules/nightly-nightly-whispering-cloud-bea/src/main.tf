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
  # Mock rationale: In a real scenario, credentials would be configured.
  # For offline validation/plan, provider block is needed but actual credentials aren't used.
  # We assume valid credentials for a real 'apply' operation.
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

resource "aws_s3_bucket" "beacon_bucket" {
  bucket = "${var.bucket_name_prefix}-${random_string.suffix.result}"

  tags = {
    Name        = "ApocalypsAI-Whispering-Beacon"
    Environment = "Apocalypse"
  }
}

resource "aws_s3_bucket_acl" "beacon_bucket_acl" {
  bucket = aws_s3_bucket.beacon_bucket.id
  acl    = "public-read"
}

resource "aws_s3_bucket_public_access_block" "beacon_public_access_block" {
  bucket = aws_s3_bucket.beacon_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_website_configuration" "beacon_website_config" {
  bucket = aws_s3_bucket.beacon_bucket.id

  index_document {
    suffix = var.index_document
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_policy" "beacon_bucket_policy" {
  bucket = aws_s3_bucket.beacon_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.beacon_bucket.arn}/*"
      },
    ]
  })
}

resource "aws_s3_object" "beacon_index_html" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = var.index_document
  content      = var.beacon_message_html
  content_type = "text/html"
  acl          = "public-read" # ACL on object for public read
}
