resource "aws_s3_bucket" "beacon_bucket" {
  bucket = var.bucket_name
  acl    = "public-read" # Mock rationale: For a simple public static website beacon, public-read is acceptable. In a real scenario, OAC/OAI with a bucket policy is preferred.

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  tags = {
    Project     = "ApocalypsAI"
    Environment = "Beacon"
    Utility     = "NightlyCloudBeacon"
  }
}

resource "aws_s3_bucket_policy" "beacon_bucket_policy" {
  bucket = aws_s3_bucket.beacon_bucket.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "PublicReadGetObject",
        Effect    = "Allow",
        Principal = "*",
        Action    = ["s3:GetObject"],
        Resource  = ["${aws_s3_bucket.beacon_bucket.arn}/*"]
      }
    ]
  })
}

resource "aws_cloudfront_origin_access_control" "beacon_oac" {
  # Mock rationale: Using OAC for CloudFront to S3 access, which is the recommended secure way.
  # This resource is mocked in tests to avoid actual AWS calls.
  name                              = "${var.bucket_name}-oac"
  description                       = "OAC for Nightly Cloud Beacon S3 bucket"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "beacon_distribution" {
  origin {
    domain_name              = aws_s3_bucket.beacon_bucket.bucket_regional_domain_name
    origin_id                = aws_s3_bucket.beacon_bucket.id
    origin_access_control_id = aws_cloudfront_origin_access_control.beacon_oac.id
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CloudFront distribution for the Nightly Cloud Beacon"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = aws_s3_bucket.beacon_bucket.id
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
    # Mock rationale: Query string and cookie forwarding are disabled for a simple static site.
    # In a real dynamic site, these would be configured differently.
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

  tags = {
    Project     = "ApocalypsAI"
    Environment = "Beacon"
    Utility     = "NightlyCloudBeacon"
  }
}

# Optional: Route 53 record for custom domain
resource "aws_route53_record" "beacon_cname" {
  count = var.domain_name != "" && var.zone_id != "" ? 1 : 0

  zone_id = var.zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.beacon_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.beacon_distribution.hosted_zone_id
    evaluate_target_health = false
  }
}

# Example content for the beacon
resource "aws_s3_bucket_object" "index_html" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "index.html"
  content_type = "text/html"
  content      = "<html><body><h1>Hello from the Nightly Cloud Beacon!</h1><p>The ApocalypsAI community is here.</p></body></html>"
  acl          = "public-read" # Mock rationale: Public read for static website content.
}

resource "aws_s3_bucket_object" "error_html" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "error.html"
  content_type = "text/html"
  content      = "<html><body><h1>404 - Beacon Lost!</h1><p>The requested signal could not be found.</p></body></html>"
  acl          = "public-read" # Mock rationale: Public read for static website content.
}
