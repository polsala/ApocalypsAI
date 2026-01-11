provider "aws" {
  region = var.region
}

# S3 Bucket for Access Logs
resource "aws_s3_bucket" "logging_bucket" {
  bucket = "${var.bucket_name_prefix}-access-logs"
  acl    = "log-delivery-write" # Required for S3 log delivery

  tags = merge(var.tags, {
    Name = "${var.bucket_name_prefix}-access-logs"
  })
}

resource "aws_s3_bucket_versioning" "logging_bucket_versioning" {
  bucket = aws_s3_bucket.logging_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "logging_bucket_sse" {
  bucket = aws_s3_bucket.logging_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "logging_bucket_public_access_block" {
  bucket = aws_s3_bucket.logging_bucket.id

  block_public_acls       = true
  block_public_and_cross_account_access = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Main S3 Echo Chamber Bucket
resource "aws_s3_bucket" "echo_chamber_bucket" {
  bucket = "${var.bucket_name_prefix}-echo-chamber"

  logging {
    target_bucket = aws_s3_bucket.logging_bucket.id
    target_prefix = "log/"
  }

  tags = merge(var.tags, {
    Name = "${var.bucket_name_prefix}-echo-chamber"
  })
}

resource "aws_s3_bucket_versioning" "echo_chamber_bucket_versioning" {
  bucket = aws_s3_bucket.echo_chamber_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "echo_chamber_bucket_sse" {
  bucket = aws_s3_bucket.echo_chamber_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "echo_chamber_bucket_public_access_block" {
  bucket = aws_s3_bucket.echo_chamber_bucket.id

  block_public_acls       = true
  block_public_and_cross_account_access = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Lambda Echo Function (Optional)
resource "aws_iam_role" "lambda_echo_role" {
  count = var.enable_lambda_echo ? 1 : 0

  name = "${var.bucket_name_prefix}-lambda-echo-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy" "lambda_echo_policy" {
  count = var.enable_lambda_echo ? 1 : 0

  name = "${var.bucket_name_prefix}-lambda-echo-policy"
  role = aws_iam_role.lambda_echo_role[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:${var.region}:*:*"
      },
      {
        Action = [
          "s3:GetObject",
          "s3:GetObjectAcl",
          "s3:GetObjectTagging",
        ]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.echo_chamber_bucket.arn}/*"
      },
    ]
  })
}

resource "aws_cloudwatch_log_group" "lambda_echo_log_group" {
  count = var.enable_lambda_echo ? 1 : 0

  name              = "/aws/lambda/${var.bucket_name_prefix}-echo-chamber-lambda"
  retention_in_days = 7

  tags = var.tags
}

data "archive_file" "lambda_zip" {
  count = var.enable_lambda_echo ? 1 : 0

  type        = "zip"
  source_file = "${path.module}/lambda/echo_handler.py"
  output_path = "${path.module}/lambda/echo_handler.zip"
}

resource "aws_lambda_function" "echo_chamber_lambda" {
  count = var.enable_lambda_echo ? 1 : 0

  filename         = data.archive_file.lambda_zip[0].output_path
  function_name    = "${var.bucket_name_prefix}-echo-chamber-lambda"
  role             = aws_iam_role.lambda_echo_role[0].arn
  handler          = "echo_handler.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip[0].output_base64sha256
  runtime          = "python3.9"
  timeout          = 30

  environment {
    variables = {
      LOG_LEVEL = "INFO"
    }
  }

  tags = var.tags
}

resource "aws_lambda_permission" "allow_s3_to_call_lambda" {
  count = var.enable_lambda_echo ? 1 : 0

  statement_id  = "AllowS3InvokeLambda"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.echo_chamber_lambda[0].function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.echo_chamber_bucket.arn
}

resource "aws_s3_bucket_notification" "s3_bucket_notification" {
  count = var.enable_lambda_echo ? 1 : 0

  bucket = aws_s3_bucket.echo_chamber_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.echo_chamber_lambda[0].arn
    events              = ["s3:ObjectCreated:*"]
  }
}
