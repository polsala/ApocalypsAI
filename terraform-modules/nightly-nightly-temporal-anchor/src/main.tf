provider "aws" {
  region = "us-east-1" # CloudFront distributions are global but managed from us-east-1
}

resource "aws_s3_bucket" "anchor_bucket" {
  bucket = "${var.bucket_name_prefix}-temporal-anchor-${random_string.suffix.result}"

  tags = {
    ManagedBy = "ApocalypsAI"
    Utility   = "nightly-temporal-anchor"
  }
}

resource "aws_s3_bucket_website_configuration" "anchor_website_config" {
  bucket = aws_s3_bucket.anchor_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_public_access_block" "anchor_bucket_public_access_block" {
  bucket = aws_s3_bucket.anchor_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_cloudfront_origin_access_identity" "anchor_oai" {
  comment = "OAI for Nightly Temporal Anchor S3 bucket"
}

resource "aws_s3_bucket_policy" "anchor_bucket_policy" {
  bucket = aws_s3_bucket.anchor_bucket.id
  policy = data.aws_iam_policy_document.s3_policy.json
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.anchor_bucket.arn}/*"]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.anchor_oai.iam_arn]
    }
  }
}

resource "aws_cloudfront_distribution" "anchor_distribution" {
  origin {
    domain_name = aws_s3_bucket.anchor_bucket.bucket_regional_domain_name
    origin_id   = "S3-TemporalAnchor"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.anchor_oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CloudFront distribution for Nightly Temporal Anchor"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3-TemporalAnchor"
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
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

  # Add a random string to the bucket name to ensure global uniqueness
  # This is crucial for S3 bucket names.
  # The random_string resource is from the hashicorp/random provider.
  # Make sure to run `terraform init` to download this provider.
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}
