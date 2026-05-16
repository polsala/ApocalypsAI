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

resource "random_id" "suffix" {
  byte_length = 8
}

resource "aws_s3_bucket" "beacon_bucket" {
  bucket = "${var.project_name}-${var.environment}-sanctuary-beacon-${random_id.suffix.hex}"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_s3_bucket_public_access_block" "beacon_bucket_public_access_block" {
  bucket = aws_s3_bucket.beacon_bucket.id

  # When using CloudFront OAC, the S3 bucket should not be publicly accessible directly.
  # CloudFront will access the bucket via the OAC, and the bucket policy grants this access.
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_object" "beacon_content" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "index.html"
  source       = var.content_file_path
  content_type = "text/html"
  etag         = filemd5(var.content_file_path)
}

resource "aws_cloudfront_origin_access_control" "beacon_oac" {
  name                              = "${var.project_name}-${var.environment}-beacon-oac"
  description                       = "OAC for S3 bucket ${aws_s3_bucket.beacon_bucket.id}"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "beacon_cdn" {
  origin {
    domain_name              = aws_s3_bucket.beacon_bucket.bucket_regional_domain_name
    origin_id                = aws_s3_bucket.beacon_bucket.id
    origin_access_control_id = aws_cloudfront_origin_access_control.beacon_oac.id
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Cloud Sanctuary Beacon for ${var.project_name}-${var.environment}"
  default_root_object = "index.html" # CloudFront handles the default root object

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = aws_s3_bucket.beacon_bucket.id
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
    field_level_encryption_id = ""

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

data "aws_iam_policy_document" "s3_bucket_policy" {
  statement {
    actions = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.beacon_bucket.arn}/*"]

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [aws_cloudfront_distribution.beacon_cdn.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "beacon_bucket_policy" {
  bucket = aws_s3_bucket.beacon_bucket.id
  policy = data.aws_iam_policy_document.s3_bucket_policy.json
}
