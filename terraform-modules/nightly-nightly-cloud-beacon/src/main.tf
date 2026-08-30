terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

resource "aws_s3_bucket" "beacon_bucket" {
  bucket = "${var.bucket_name_prefix}-${random_string.suffix.result}"
  acl    = "public-read" # For static website hosting

  tags = {
    Name        = "NightlyCloudBeacon"
    Environment = "ApocalypsAI"
  }
}

resource "aws_s3_bucket_website_configuration" "beacon_website" {
  bucket = aws_s3_bucket.beacon_bucket.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_policy" "beacon_bucket_policy" {
  bucket = aws_s3_bucket.beacon_bucket.id
  policy = data.aws_iam_policy_document.beacon_policy.json
}

data "aws_iam_policy_document" "beacon_policy" {
  statement {
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject",
    ]

    resources = [
      "${aws_s3_bucket.beacon_bucket.arn}/*",
    ]
  }
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

resource "aws_s3_bucket_object" "index_html" {
  bucket       = aws_s3_bucket.beacon_bucket.id
  key          = "index.html"
  content      = templatefile("${path.module}/templates/index.html.tpl", {
    message   = var.message_seed
    timestamp = formatdate("YYYY-MM-DD HH:MM ZZZ", timestamp())
  })
  content_type = "text/html"
  acl          = "public-read"
}
