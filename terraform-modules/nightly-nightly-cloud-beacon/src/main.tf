provider "aws" {
  region = var.aws_region
}

provider "random" {} # For generating unique bucket names

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

resource "aws_s3_bucket" "beacon_bucket" {
  bucket = "${var.bucket_name_prefix}-${random_string.suffix.result}"

  # S3 bucket should be private and only accessible via CloudFront OAC
  acl = "private"

  tags = {
    Name        = "${var.bucket_name_prefix}-beacon"
    Environment = "apocalypsai"
  }
}

# CloudFront Origin Access Control (OAC) to securely access the S3 bucket
resource "aws_cloudfront_origin_access_control" "beacon_oac" {
  name                              = "${var.bucket_name_prefix}-oac"
  description                       = "OAC for S3 bucket ${aws_s3_bucket.beacon_bucket.id}"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "no-override"
  signing_protocol                  = "sigv4"
}

# S3 bucket policy to grant CloudFront OAC read access
resource "aws_s3_bucket_policy" "beacon_bucket_policy" {
  bucket = aws_s3_bucket.beacon_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowCloudFrontServicePrincipalReadOnly",
        Effect    = "Allow",
        Principal = {
          Service = "cloudfront.amazonaws.com"
        },
        Action    = ["s3:GetObject"],
        Resource  = ["${aws_s3_bucket.beacon_bucket.arn}/*"],
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.beacon_distribution.arn
          }
        }
      }
    ]
  })
}

locals {
  beacon_html_content = <<EOT
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ApocalypsAI Cloud Beacon</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #1a1a1a; color: #00ff00; text-align: center; padding-top: 50px; }
        .beacon-message { font-size: 2em; border: 2px solid #00ff00; padding: 20px; display: inline-block; margin-top: 50px; animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <h1>ApocalypsAI Cloud Beacon</h1>
    <div class="beacon-message">${var.beacon_message}</div>
    <p>Last updated: ${timestamp()}</p>
</body>
</html>
EOT
}

resource "aws_s3_bucket_object" "beacon_index_html" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "index.html"
  content_type = "text/html"
  content      = local.beacon_html_content
  etag         = md5(local.beacon_html_content) # ETag based on content hash
}

resource "aws_cloudfront_distribution" "beacon_distribution" {
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
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = aws_s3_bucket.beacon_bucket.id
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

  tags = {
    Name        = "${var.bucket_name_prefix}-cloudfront"
    Environment = "apocalypsai"
  }
}
