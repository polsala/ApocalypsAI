provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "content_bucket" {
  bucket = var.content_bucket_name
  acl    = "private" # CloudFront OAI will access it
  tags = {
    Project     = var.project_name
    Environment = "ApocalypsAI-Beacon"
  }
}

resource "aws_s3_bucket_public_access_block" "content_bucket_public_access_block" {
  bucket = aws_s3_bucket.content_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "content_bucket_ownership_controls" {
  bucket = aws_s3_bucket.content_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "content_bucket_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.content_bucket_ownership_controls]

  bucket = aws_s3_bucket.content_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_website_configuration" "content_bucket_website_config" {
  bucket = aws_s3_bucket.content_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for ${var.project_name} Cloud-Whisperer Beacon"
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions = ["s3:GetObject"]
    resources = [
      "${aws_s3_bucket.content_bucket.arn}/*",
    ]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.oai.iam_arn]
    }
  }
}

resource "aws_s3_bucket_policy" "content_bucket_policy" {
  bucket = aws_s3_bucket.content_bucket.id
  policy = data.aws_iam_policy_document.s3_policy.json
}

resource "aws_cloudfront_distribution" "s3_distribution" {
  origin {
    domain_name = aws_s3_bucket.content_bucket.bucket_regional_domain_name
    origin_id   = aws_s3_bucket.content_bucket.id

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Cloud-Whisperer Beacon for ${var.project_name}"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = aws_s3_bucket.content_bucket.id

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
    Project     = var.project_name
    Environment = "ApocalypsAI-Beacon"
  }
}

# Upload default content
resource "aws_s3_object" "index_html" {
  bucket       = aws_s3_bucket.content_bucket.id
  key          = "index.html"
  content_type = "text/html"
  source       = "${path.module}/content/index.html"
  etag         = filemd5("${path.module}/content/index.html")
}

resource "aws_s3_object" "error_html" {
  bucket       = aws_s3_bucket.content_bucket.id
  key          = "error.html"
  content_type = "text/html"
  source       = "${path.module}/content/error.html"
  etag         = filemd5("${path.module}/content/error.html")
}
