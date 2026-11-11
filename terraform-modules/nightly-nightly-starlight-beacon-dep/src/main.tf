resource "aws_s3_bucket" "beacon_bucket" {
  bucket = "${var.bucket_name_prefix}-${random_string.suffix.result}"
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "index.html"
  }

  tags = {
    Name        = "StarlightBeaconBucket"
    Environment = "ApocalypsAI"
  }
}

resource "aws_s3_bucket_policy" "beacon_bucket_policy" {
  bucket = aws_s3_bucket.beacon_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject",
        Effect    = "Allow",
        Principal = "*",
        Action    = "s3:GetObject",
        Resource  = "${aws_s3_bucket.beacon_bucket.arn}/*"
      },
    ]
  })
}

resource "aws_s3_bucket_object" "beacon_index" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "index.html"
  content_type = "text/html"
  content      = templatefile("${path.module}/index.html", { beacon_message = var.beacon_message })
  etag         = md5(templatefile("${path.module}/index.html", { beacon_message = var.beacon_message }))
}

resource "aws_cloudfront_distribution" "beacon_cdn" {
  origin {
    domain_name = aws_s3_bucket.beacon_bucket.website_endpoint
    origin_id   = "S3-Beacon-Origin"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CloudFront distribution for Starlight Beacon"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-Beacon-Origin"

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
    Name        = "StarlightBeaconCDN"
    Environment = "ApocalypsAI"
  }
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}
