terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "anomaly_logs" {
  bucket_prefix = "${var.beacon_name}-anomaly-logs-"

  tags = {
    Name      = "${var.beacon_name}-anomaly-logs"
    Purpose   = "TemporalAnomalyBeacon"
    ManagedBy = "ApocalypsAI"
  }
}

resource "aws_s3_bucket_public_access_block" "anomaly_logs_block" {
  bucket = aws_s3_bucket.anomaly_logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.beacon_name}-lambda-exec-role"

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
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "anomaly_handler" {
  function_name    = "${var.beacon_name}-anomaly-handler"
  handler          = "beacon_handler.lambda_handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_exec_role.arn
  timeout          = 30

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      LOG_LEVEL      = var.log_level
      S3_BUCKET_NAME = aws_s3_bucket.anomaly_logs.bucket
    }
  }

  tags = {
    Name      = "${var.beacon_name}-anomaly-handler"
    Purpose   = "TemporalAnomalyBeacon"
    ManagedBy = "ApocalypsAI"
  }
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/beacon_handler.py"
  output_path = "${path.module}/lambda/beacon_handler.zip"
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket created."
  value       = aws_s3_bucket.anomaly_logs.bucket
}

output "lambda_function_name" {
  description = "The name of the Lambda function created."
  value       = aws_lambda_function.anomaly_handler.function_name
}

output "lambda_invoke_arn" {
  description = "The ARN to invoke the Lambda function."
  value       = aws_lambda_function.anomaly_handler.invoke_arn
}
