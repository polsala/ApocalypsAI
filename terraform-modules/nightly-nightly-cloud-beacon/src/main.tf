resource "aws_s3_bucket" "beacon_bucket" {
  bucket = "${var.bucket_name_prefix}-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
  acl    = "private" # CloudFront OAC will access

  tags = var.tags
}

resource "aws_s3_bucket_website_configuration" "beacon_website_config" {
  bucket = aws_s3_bucket.beacon_bucket.id

  index_document {
    suffix = var.index_document
  }

  error_document {
    key = var.error_document
  }
}

resource "aws_s3_bucket_policy" "beacon_bucket_policy" {
  bucket = aws_s3_bucket.beacon_bucket.id
  policy = data.aws_iam_policy_document.s3_policy.json
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.beacon_bucket.arn}/*"]

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.beacon_cdn.arn]
    }
  }
}

resource "aws_cloudfront_origin_access_control" "beacon_oac" {
  name                              = "${var.bucket_name_prefix}-oac"
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
  comment             = "CloudFront distribution for Nightly Cloud Beacon: ${var.bucket_name_prefix}"
  default_root_object = var.index_document

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD", "OPTIONS"]
    target_origin_id       = aws_s3_bucket.beacon_bucket.id
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
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

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
