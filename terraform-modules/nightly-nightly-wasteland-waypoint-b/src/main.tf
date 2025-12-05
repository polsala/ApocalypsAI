resource "aws_s3_bucket" "waypoint_content" {
  bucket = var.bucket_name

  tags = {
    Project     = "ApocalypsAI"
    Environment = "WastelandBeacon"
  }
}

resource "aws_s3_bucket_website_configuration" "waypoint_content" {
  bucket = aws_s3_bucket.waypoint_content.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_acl" "waypoint_content_acl" {
  bucket = aws_s3_bucket.waypoint_content.id
  acl    = "private"
}

resource "aws_s3_object" "index_html" {
  bucket       = aws_s3_bucket.waypoint_content.id
  key          = "index.html"
  source       = var.content_file_path
  content_type = "text/html"
  etag         = filemd5(var.content_file_path)
}

resource "aws_cloudfront_origin_access_control" "waypoint_oac" {
  name                              = "${var.bucket_name}-oac"
  description                       = "OAC for S3 bucket ${var.bucket_name}"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "waypoint_cdn" {
  origin {
    domain_name              = aws_s3_bucket.waypoint_content.bucket_regional_domain_name
    origin_id                = aws_s3_bucket.waypoint_content.id
    origin_access_control_id = aws_cloudfront_origin_access_control.waypoint_oac.id
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CloudFront distribution for Wasteland Waypoint Beacon"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = aws_s3_bucket.waypoint_content.id
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

  lifecycle {
    ignore_changes = [
      # Ignore changes to the default_root_object if it's managed by other means
      # or if we want to allow manual changes without Terraform reverting them.
      default_root_object,
    ]
  }
}

resource "aws_s3_bucket_policy" "waypoint_content_policy" {
  bucket = aws_s3_bucket.waypoint_content.id
  policy = data.aws_iam_policy_document.s3_policy.json
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.waypoint_content.arn}/*"]

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.waypoint_cdn.arn]
    }
  }
}
