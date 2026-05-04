# AWS Provider configuration
# This module assumes the AWS provider is configured in the root module.
# provider "aws" {
#   region = "us-east-1" # Or any desired region
# }

resource "aws_s3_bucket" "echo_chamber_bucket" {
  bucket_prefix = var.bucket_name_prefix
  tags          = var.tags
}

resource "aws_s3_bucket_website_configuration" "echo_chamber_website" {
  bucket = aws_s3_bucket.echo_chamber_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_public_access_block" "echo_chamber_public_access_block" {
  bucket = aws_s3_bucket.echo_chamber_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Upload initial index.html content
resource "aws_s3_object" "index_html" {
  bucket       = aws_s3_bucket.echo_chamber_bucket.id
  key          = "index.html"
  content      = var.content_html
  content_type = "text/html"
  acl          = "private" # Managed by OAC/CloudFront
  tags         = var.tags
}

# CloudFront Origin Access Control (OAC) for secure S3 access
resource "aws_cloudfront_origin_access_control" "echo_chamber_oac" {
  name                              = "${aws_s3_bucket.echo_chamber_bucket.id}-oac"
  description                       = "OAC for S3 bucket ${aws_s3_bucket.echo_chamber_bucket.id}"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# S3 Bucket Policy to allow CloudFront OAC access
resource "aws_s3_bucket_policy" "echo_chamber_policy" {
  bucket = aws_s3_bucket.echo_chamber_bucket.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = {
          Service = "cloudfront.amazonaws.com"
        },
        Action    = "s3:GetObject",
        Resource  = "${aws_s3_bucket.echo_chamber_bucket.arn}/*",
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_origin_access_control.echo_chamber_oac.cloudfront_access_control_origin_type_arn
          }
        }
      }
    ]
  })
}

resource "aws_cloudfront_distribution" "echo_chamber_cdn" {
  origin {
    domain_name              = aws_s3_bucket.echo_chamber_bucket.bucket_regional_domain_name
    origin_id                = aws_s3_bucket.echo_chamber_bucket.id
    origin_access_control_id = aws_cloudfront_origin_access_control.echo_chamber_oac.id
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CloudFront distribution for the Temporal Echo Chamber"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = aws_s3_bucket.echo_chamber_bucket.id
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600 # Cache for 1 hour by default
    max_ttl                = 86400 # Max cache for 24 hours
    compress               = true

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = var.tags
}
