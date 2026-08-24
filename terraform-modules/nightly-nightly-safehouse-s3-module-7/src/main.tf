resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  tags   = var.tags
}

resource "aws_s3_bucket_versioning" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "safehouse" {
  bucket = aws_s3_bucket.safehouse.id

  rule {
    id     = "expire-after-30-days"
    status = "Enabled"

    expiration {
      days = 30
    }
  }
}

resource "aws_iam_policy" "read_only" {
  name   = "${var.bucket_name}-read-only"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = ["s3:GetObject"],
      Resource = "${aws_s3_bucket.safehouse.arn}/*"
    }]
  })
}

output "bucket_id" {
  value = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  value = aws_s3_bucket.safehouse.arn
}

output "read_only_policy_arn" {
  value = aws_iam_policy.read_only.arn
}
