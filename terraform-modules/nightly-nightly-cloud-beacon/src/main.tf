resource "aws_s3_bucket" "beacon_bucket" {
  bucket_prefix = var.bucket_name_prefix
  acl           = "public-read" # For static website hosting

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  tags = {
    Name        = "${var.bucket_name_prefix}-beacon-bucket"
    Environment = "ApocalypsAI"
    ManagedBy   = "NightlyCloudBeacon"
  }
}

resource "aws_s3_bucket_public_access_block" "beacon_bucket_public_access_block" {
  bucket = aws_s3_bucket.beacon_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
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
        Action    = "s3:GetObject",
        Resource  = "${aws_s3_bucket.beacon_bucket.arn}/*"
      }
    ]
  })
}

locals {
  index_html_content = <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ApocalypsAI Cloud Beacon</title>
    <style>
        body { font-family: monospace; background-color: #1a1a1a; color: #00ff00; text-align: center; padding-top: 50px; }
        h1 { color: #00cc00; }
        p { font-size: 1.2em; }
        .footer { margin-top: 50px; font-size: 0.8em; color: #008800; }
    </style>
</head>
<body>
    <h1>ApocalypsAI Cloud Beacon Active</h1>
    <p>${var.content_message}</p>
    <div class="footer">
        <p>Beacon ID: ${aws_s3_bucket.beacon_bucket.id}</p>
        <p>Last updated: ${timestamp()}</p>
    </div>
</body>
</html>
EOF
}

resource "aws_s3_bucket_object" "index_html" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "index.html"
  content_type = "text/html"
  content      = local.index_html_content
  etag         = md5(local.index_html_content) # ETag for content changes
}

resource "aws_cloudfront_origin_access_control" "beacon_oac" {
  name                              = "${var.bucket_name_prefix}-beacon-oac"
  description                       = "OAC for S3 bucket origin"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "no-override"
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
  comment             = "CloudFront distribution for ApocalypsAI Cloud Beacon"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = aws_s3_bucket.beacon_bucket.id

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
    Name        = "${var.bucket_name_prefix}-beacon-cdn"
    Environment = "ApocalypsAI"
    ManagedBy   = "NightlyCloudBeacon"
  }
}

# Provider configuration
provider "aws" {
  region = var.aws_region
}
