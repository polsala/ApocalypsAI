resource "aws_s3_bucket" "safehouse" {
  bucket = var.bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "safehouse_versioning" {
  bucket = aws_s3_bucket.safehouse.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "safehouse_encryption" {
  bucket = aws_s3_bucket.safehouse.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "safehouse_lifecycle" {
  bucket = aws_s3_bucket.safehouse.id
  rule {
    id     = "expire-after-days"
    status = "Enabled"
    expiration {
      days = var.expiration_days
    }
    filter {}
  }
}

resource "aws_iam_policy" "safehouse_access" {
  name        = "${var.bucket_name}-access"
  description = "Read/write access to the safehouse S3 bucket"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      Resource = [
        aws_s3_bucket.safehouse.arn,
        "${aws_s3_bucket.safehouse.arn}/*"
      ]
    }]
  })
}

resource "aws_iam_policy_attachment" "attach_to_role" {
  name       = "${var.bucket_name}-policy-attachment"
  roles      = [var.allowed_role_arn]
  policy_arn = aws_iam_policy.safehouse_access.arn
}
