resource "aws_s3_bucket" "temporal_anchor_bucket" {
  bucket = var.bucket_name
  acl    = "public-read" # For static website hosting

  website {
    index_document = var.index_document
    error_document = var.error_document
  }

  tags = {
    Name        = "${var.bucket_name}-temporal-anchor"
    Environment = "ApocalypsAI"
    Purpose     = "TemporalStabilityAffirmations"
  }
}

resource "aws_s3_bucket_policy" "temporal_anchor_bucket_policy" {
  bucket = aws_s3_bucket.temporal_anchor_bucket.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "PublicReadGetObject",
        Effect    = "Allow",
        Principal = "*",
        Action    = ["s3:GetObject"],
        Resource  = ["${aws_s3_bucket.temporal_anchor_bucket.arn}/*"]
      }
    ]
  })
}

resource "aws_cloudfront_origin_access_identity" "temporal_anchor_oai" {
  comment = "OAI for ${var.bucket_name} S3 bucket"
}

resource "aws_cloudfront_distribution" "temporal_anchor_cdn" {
  origin {
    domain_name              = aws_s3_bucket.temporal_anchor_bucket.bucket_regional_domain_name
    origin_id                = "S3-${aws_s3_bucket.temporal_anchor_bucket.id}"
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.temporal_anchor_oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CloudFront distribution for Temporal Anchor Point: ${var.bucket_name}"
  default_root_object = var.index_document

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.temporal_anchor_bucket.id}"

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

  tags = {
    Name        = "${var.bucket_name}-temporal-anchor-cdn"
    Environment = "ApocalypsAI"
    Purpose     = "TemporalStabilityAffirmations"
  }
}
