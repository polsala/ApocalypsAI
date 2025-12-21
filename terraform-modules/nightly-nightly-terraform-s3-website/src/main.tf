terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "index_document" {
  description = "Index document for website"
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "Error document for website"
  type        = string
  default     = "error.html"
}

variable "enable_cdn" {
  description = "Whether to create a CloudFront distribution"
  type        = bool
  default     = false
}

resource "aws_s3_bucket" "website" {
  bucket = var.bucket_name

  website {
    index_document = var.index_document
    error_document = var.error_document
  }

  acl = "public-read"
}

resource "aws_s3_bucket_policy" "public_read" {
  bucket = aws_s3_bucket.website.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = "*"
      Action    = ["s3:GetObject"]
      Resource  = ["${aws_s3_bucket.website.arn}/*"]
    }]
  })
}

resource "aws_cloudfront_distribution" "cdn" {
  count = var.enable_cdn ? 1 : 0

  origin {
    domain_name = aws_s3_bucket.website.bucket_regional_domain_name
    origin_id   = "s3-${aws_s3_bucket.website.id}"
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = var.index_document

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "s3-${aws_s3_bucket.website.id}"
    viewer_protocol_policy = "redirect-to-https"
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
}

output "bucket_id" {
  value = aws_s3_bucket.website.id
}

output "website_endpoint" {
  value = aws_s3_bucket.website.website_endpoint
}

output "cloudfront_domain" {
  value = try(aws_cloudfront_distribution.cdn[0].domain_name, "")
}
