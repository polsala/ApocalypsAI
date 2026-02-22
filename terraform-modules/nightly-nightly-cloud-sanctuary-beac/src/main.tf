# Configure the AWS provider
provider "aws" {
  region = var.aws_region
}

# S3 Bucket for static website content
resource "aws_s3_bucket" "sanctuary_beacon_bucket" {
  bucket = var.bucket_name
  acl    = "private" # CloudFront OAC will provide access

  tags = {
    Name        = "SanctuaryBeaconBucket"
    Environment = "ApocalypsAI"
  }
}

# S3 Bucket Public Access Block
resource "aws_s3_bucket_public_access_block" "sanctuary_beacon_bucket_public_access_block" {
  bucket = aws_s3_bucket.sanctuary_beacon_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# CloudFront Origin Access Control (OAC)
resource "aws_cloudfront_origin_access_control" "sanctuary_beacon_oac" {
  name                              = "${var.bucket_name}-oac"
  description                       = "OAC for Sanctuary Beacon S3 bucket"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# S3 Bucket Policy to allow CloudFront OAC access
resource "aws_s3_bucket_policy" "sanctuary_beacon_bucket_policy" {
  bucket = aws_s3_bucket.sanctuary_beacon_bucket.id
  policy = data.aws_iam_policy_document.sanctuary_beacon_bucket_policy_document.json
}

data "aws_iam_policy_document" "sanctuary_beacon_bucket_policy_document" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.sanctuary_beacon_bucket.arn}/*"]

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "cloudfront:SourceArn"
      values   = [aws_cloudfront_distribution.sanctuary_beacon_distribution.arn]
    }
  }
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "sanctuary_beacon_distribution" {
  origin {
    domain_name              = aws_s3_bucket.sanctuary_beacon_bucket.bucket_regional_domain_name
    origin_id                = aws_s3_bucket.sanctuary_beacon_bucket.id
    origin_access_control_id = aws_cloudfront_origin_access_control.sanctuary_beacon_oac.id
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CloudFront distribution for the Nightly Cloud Sanctuary Beacon"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = aws_s3_bucket.sanctuary_beacon_bucket.id
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true

    forwarded_values {
      query_string = false
      headers      = []
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

  tags = {
    Name        = "SanctuaryBeaconCloudFront"
    Environment = "ApocalypsAI"
  }
}

# Upload default index.html to S3
resource "aws_s3_bucket_object" "index_html" {
  bucket       = aws_s3_bucket.sanctuary_beacon_bucket.id
  key          = "index.html"
  source       = "${path.module}/index.html"
  content_type = "text/html"
  etag         = filemd5("${path.module}/index.html")
}
