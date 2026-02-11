resource "aws_s3_bucket" "signal_fire_bucket" {
  bucket = "${var.bucket_name_prefix}-${random_string.suffix.result}"
  acl    = "private" # CloudFront OAI will access it

  tags = {
    Name        = "ApocalypsAI-DigitalSignalFire"
    Environment = "Apocalypse"
  }
}

resource "aws_s3_bucket_public_access_block" "signal_fire_bucket_public_access_block" {
  bucket = aws_s3_bucket.signal_fire_bucket.id

  block_public_acls       = true
  block_public_and_cross_account_access = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "signal_fire_bucket_ownership_controls" {
  bucket = aws_s3_bucket.signal_fire_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_versioning" "signal_fire_bucket_versioning" {
  bucket = aws_s3_bucket.signal_fire_bucket.id
  enabled = true
}

# S3 bucket policy to allow CloudFront OAI access
resource "aws_s3_bucket_policy" "signal_fire_bucket_policy" {
  bucket = aws_s3_bucket.signal_fire_bucket.id
  policy = data.aws_iam_policy_document.s3_policy.json
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.signal_fire_bucket.arn}/*"]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.signal_fire_oai.iam_arn]
    }
  }
}

resource "aws_cloudfront_origin_access_identity" "signal_fire_oai" {
  comment = "OAI for ApocalypsAI Digital Signal Fire S3 bucket"
}

resource "aws_cloudfront_distribution" "signal_fire_cdn" {
  origin {
    domain_name = aws_s3_bucket.signal_fire_bucket.bucket_regional_domain_name
    origin_id   = aws_s3_bucket.signal_fire_bucket.id

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.signal_fire_oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "ApocalypsAI Digital Signal Fire CDN"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = aws_s3_bucket.signal_fire_bucket.id

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

  # Ensure CloudFront distribution waits for S3 bucket policy to be applied
  depends_on = [
    aws_s3_bucket_policy.signal_fire_bucket_policy,
    aws_s3_bucket_public_access_block.signal_fire_bucket_public_access_block,
    aws_s3_bucket_ownership_controls.signal_fire_bucket_ownership_controls
  ]
}

resource "aws_s3_bucket_object" "index_html" {
  bucket       = aws_s3_bucket.signal_fire_bucket.id
  key          = "index.html"
  content_type = "text/html"
  content      = <<EOT
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ApocalypsAI Digital Signal Fire</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #1a1a1a; color: #00ff00; text-align: center; padding-top: 50px; }
        .container { border: 2px solid #00ff00; padding: 20px; display: inline-block; margin: 20px; box-shadow: 0 0 15px #00ff00; }
        h1 { color: #00ff00; text-shadow: 0 0 10px #00ff00; }
        p { font-size: 1.2em; }
        .timestamp { font-size: 0.8em; color: #00cc00; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>&#x1F525; Digital Signal Fire &#x1F525;</h1>
        <p>${var.initial_message}</p>
        <div class="timestamp">Last updated: ${formatdate("YYYY-MM-DD hh:mm:ss ZZZ", timestamp())}</div>
    </div>
</body>
</html>
EOT
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}
