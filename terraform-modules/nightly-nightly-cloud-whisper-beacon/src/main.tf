provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "beacon_bucket" {
  bucket = "${var.project_name}-apocalypsai-beacon-${var.region}"

  tags = {
    Project   = var.project_name
    ManagedBy = "ApocalypsAI"
    Utility   = "NightlyCloudWhisperBeacon"
  }
}

resource "aws_s3_bucket_website_configuration" "beacon_website" {
  bucket = aws_s3_bucket.beacon_bucket.id

  index_document {
    suffix = var.index_document
  }

  error_document {
    key = var.error_document
  }
}

resource "aws_cloudfront_origin_access_identity" "beacon_oai" {
  comment = "OAI for ${var.project_name} ApocalypsAI Beacon S3 bucket"
}

resource "aws_s3_bucket_policy" "beacon_bucket_policy" {
  bucket = aws_s3_bucket.beacon_bucket.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          AWS = aws_cloudfront_origin_access_identity.beacon_oai.iam_arn
        },
        Action = "s3:GetObject",
        Resource = [
          "${aws_s3_bucket.beacon_bucket.arn}/*",
        ]
      }
    ]
  })
}

resource "aws_cloudfront_distribution" "beacon_distribution" {
  origin {
    domain_name = aws_s3_bucket.beacon_bucket.bucket_regional_domain_name
    origin_id   = "S3-Beacon-Origin"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.beacon_oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CloudFront distribution for ApocalypsAI Beacon"
  default_root_object = var.index_document

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
    Project   = var.project_name
    ManagedBy = "ApocalypsAI"
    Utility   = "NightlyCloudWhisperBeacon"
  }
}

resource "aws_s3_bucket_object" "index_html" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = var.index_document
  content_type = "text/html"
  content      = <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>ApocalypsAI Beacon</title>
    <style>
        body { font-family: monospace; background-color: #1a1a1a; color: #00ff00; text-align: center; padding-top: 50px; }
        .beacon-message { border: 2px solid #00ff00; padding: 20px; display: inline-block; margin-top: 50px; }
        .timestamp { font-size: 0.8em; color: #00cc00; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>ApocalypsAI Cloud Whisperer Beacon</h1>
    <div class="beacon-message">
        <p>${var.beacon_message}</p>
        <p class="timestamp">Last updated: ${formatdate("YYYY-MM-DD HH:mm ZZZ", timestamp())}</p>
    </div>
</body>
</html>
EOF
  acl          = "private"
}

resource "aws_s3_bucket_object" "error_html" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = var.error_document
  content_type = "text/html"
  content      = <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Error - ApocalypsAI Beacon</title>
    <style>
        body { font-family: monospace; background-color: #1a1a1a; color: #ff0000; text-align: center; padding-top: 50px; }
        .error-message { border: 2px solid #ff0000; padding: 20px; display: inline-block; margin-top: 50px; }
    </style>
</head>
<body>
    <h1>Error - ApocalypsAI Cloud Whisperer Beacon</h1>
    <div class="error-message">
        <p>Uh oh! The signal is weak. Please try again later or contact your local Integrator Agent.</p>
    </div>
</body>
</html>
EOF
  acl          = "private"
}
