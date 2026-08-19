variable "region" {
  description = "The AWS region to deploy the S3 bucket in."
  type        = string
}

variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name."
  type        = string
}

variable "signal_message" {
  description = "The whimsical message to display on the beacon's page."
  type        = string
}

resource "aws_s3_bucket" "beacon_bucket" {
  bucket = "${var.bucket_name_prefix}-${random_id.bucket_suffix.hex}"
  acl    = "public-read"

  tags = {
    Name        = "ApocalypsAI-Signal-Beacon"
    Environment = "ApocalypsAI"
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket_website_configuration" "beacon_website" {
  bucket = aws_s3_bucket.beacon_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_public_access_block" "beacon_public_access_block" {
  bucket = aws_s3_bucket.beacon_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "beacon_policy" {
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

resource "aws_s3_object" "index_html" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "index.html"
  content_type = "text/html"
  content      = templatefile("${path.module}/templates/index.html.tpl", {
    signal_message = var.signal_message
    timestamp      = formatdate("YYYY-MM-DD hh:mm:ss ZZZ", timestamp())
  })
  acl          = "public-read"
  depends_on   = [aws_s3_bucket_policy.beacon_policy, aws_s3_bucket_public_access_block.beacon_public_access_block]
}

resource "aws_s3_object" "error_html" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "error.html"
  content_type = "text/html"
  content      = "<!DOCTYPE html><html><head><title>Error</title></head><body><h1>404 - Signal Lost</h1><p>The beacon signal is momentarily disrupted. Please try again.</p></body></html>"
  acl          = "public-read"
  depends_on   = [aws_s3_bucket_policy.beacon_policy, aws_s3_bucket_public_access_block.beacon_public_access_block]
}

output "website_endpoint" {
  description = "The S3 static website endpoint URL for the beacon."
  value       = aws_s3_bucket_website_configuration.beacon_website.website_endpoint
}
