terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "shelter" {
  bucket = var.bucket_name

  force_destroy = true

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  website {
    index_document = var.index_document
    error_document = var.error_document
  }

  tags = {
    Purpose = "Apocalyptic Shelter"
  }
}

resource "aws_iam_role" "cloudfront_access" {
  name = "${var.bucket_name}-cf-access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "cloudfront.amazonaws.com"
      }
      Action = "sts:AssumeRole"
      Condition = {
        StringEquals = {
          "aws:SourceArn" = aws_cloudfront_distribution.shelter.arn
        }
      }
    }]
  })
}

resource "aws_iam_policy" "s3_read" {
  name        = "${var.bucket_name}-s3-read"
  description = "Read access for CloudFront to the shelter bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject"]
      Resource = "${aws_s3_bucket.shelter.arn}/*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.cloudfront_access.name
  policy_arn = aws_iam_policy.s3_read.arn
}

resource "aws_cloudfront_origin_access_identity" "shelter" {
  comment = "Access identity for ${var.bucket_name}"
}

resource "aws_cloudfront_distribution" "shelter" {
  origin {
    domain_name = aws_s3_bucket.shelter.bucket_regional_domain_name
    origin_id   = "s3-${aws_s3_bucket.shelter.id}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.shelter.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = var.index_document

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "s3-${aws_s3_bucket.shelter.id}"
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Purpose = "Apocalyptic Shelter"
  }
}
