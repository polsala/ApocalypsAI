resource "aws_s3_bucket" "beacon_bucket" {
  bucket_prefix = var.bucket_name_prefix
  tags          = var.tags
}

resource "aws_s3_bucket_website_configuration" "beacon_website" {
  bucket = aws_s3_bucket.beacon_bucket.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "beacon_public_access_block" {
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
        Action    = ["s3:GetObject"],
        Resource  = ["${aws_s3_bucket.beacon_bucket.arn}/*"]
      }
    ]
  })
}

resource "local_file" "index_html" {
  content  = <<EOT
<!DOCTYPE html>
<html>
<head>
    <title>ApocalypsAI Cloud Beacon</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: monospace; background-color: #1a1a1a; color: #00ff00; text-align: center; padding-top: 50px; margin: 0; }
        .container { 
            border: 2px solid #00ff00; 
            padding: 20px; 
            display: inline-block; 
            margin-top: 50px; 
            box-shadow: 0 0 20px #00ff00; 
            max-width: 90%; 
            box-sizing: border-box;
        }
        h1 { font-size: 3em; text-shadow: 0 0 10px #00ff00; margin-bottom: 20px; }
        p { font-size: 1.5em; margin: 10px 0; }
        @media (max-width: 600px) {
            h1 { font-size: 2em; }
            p { font-size: 1em; }
            .container { margin-top: 20px; padding: 15px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ApocalypsAI Cloud Beacon</h1>
        <p>${var.content_body}</p>
        <p>Signal established. We are watching.</p>
    </div>
</body>
</html>
EOT
  filename = "${path.module}/index.html"
}

resource "aws_s3_object" "index_html_object" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "index.html"
  content_type = "text/html"
  source       = local_file.index_html.filename
  etag         = filemd5(local_file.index_html.filename)
}

resource "aws_cloudfront_origin_access_control" "beacon_oac" {
  name                              = "${aws_s3_bucket.beacon_bucket.id}-oac"
  description                       = "OAC for S3 bucket ${aws_s3_bucket.beacon_bucket.id}"
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
  comment             = "ApocalypsAI Cloud Beacon Distribution"
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

  tags = var.tags
}
