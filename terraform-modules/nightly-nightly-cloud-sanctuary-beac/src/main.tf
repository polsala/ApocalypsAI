provider "aws" {
  region = var.region
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket" "beacon" {
  bucket = "${var.bucket_name_prefix}-${random_string.bucket_suffix.result}"

  tags = {
    Name        = "ApocalypsAI-Beacon"
    Environment = "Production"
  }
}

resource "aws_s3_bucket_website_configuration" "beacon" {
  bucket = aws_s3_bucket.beacon.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_public_access_block" "beacon" {
  bucket = aws_s3_bucket.beacon.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject"
    ]

    resources = [
      "${aws_s3_bucket.beacon.arn}/*"
    ]
  }
}

resource "aws_s3_bucket_policy" "beacon" {
  bucket = aws_s3_bucket.beacon.id
  policy = data.aws_iam_policy_document.s3_policy.json
}

resource "aws_s3_object" "beacon_content" {
  bucket       = aws_s3_bucket.beacon.id
  key          = "index.html"
  source       = var.content_file_path
  content_type = "text/html"
  acl          = "public-read" # Required for S3 static website hosting
}

resource "aws_cloudfront_distribution" "beacon" {
  origin {
    domain_name = aws_s3_bucket.beacon.bucket_regional_domain_name
    origin_id   = aws_s3_bucket.beacon.id

    s3_origin_config {
      origin_access_identity = ""
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "ApocalypsAI Community Beacon"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = aws_s3_bucket.beacon.id

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  # Ensure CloudFront is destroyed last
  depends_on = [
    aws_s3_bucket_policy.beacon,
    aws_s3_object.beacon_content
  ]
}
