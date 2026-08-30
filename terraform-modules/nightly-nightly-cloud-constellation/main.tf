terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# To ensure unique names for resources
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

# To get current AWS account ID for IAM policy
data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "lambda_code_bucket" {
  bucket = "${var.project_name}-constellation-mapper-code-${random_string.suffix.result}"
  acl    = "private"

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_s3_bucket" "constellation_data_bucket" {
  bucket = "${var.project_name}-constellation-data-${random_string.suffix.result}"
  acl    = "private"

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.project_name}-constellation-mapper-lambda-role-${random_string.suffix.result}"

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

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-constellation-mapper-lambda-policy-${random_string.suffix.result}"
  role = aws_iam_role.lambda_exec_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ],
        Effect   = "Allow",
        Resource = "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/*:*"
      },
      {
        Action = [
          "ec2:DescribeInstances",
          "s3:ListAllMyBuckets",
          "s3:GetBucketTagging",
          "rds:DescribeDBInstances",
          "tag:GetResources", # General tag scanning
        ],
        Effect   = "Allow",
        Resource = "*" # Needs to scan all resources for tags
      },
      {
        Action = [
          "s3:PutObject",
          "s3:GetObject",
        ],
        Effect   = "Allow",
        Resource = "${aws_s3_bucket.constellation_data_bucket.arn}/*"
      },
    ]
  })
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/constellation_mapper.py"
  output_path = "/tmp/constellation_mapper.zip" # Temporary path for local execution
}

resource "aws_s3_bucket_object" "lambda_code_upload" {
  bucket = aws_s3_bucket.lambda_code_bucket.id
  key    = "constellation_mapper.zip"
  source = data.archive_file.lambda_zip.output_path
  etag   = filemd5(data.archive_file.lambda_zip.output_path)
}

resource "aws_lambda_function" "constellation_mapper" {
  function_name    = "${var.project_name}-ConstellationMapper-${random_string.suffix.result}"
  s3_bucket        = aws_s3_bucket.lambda_code_bucket.id
  s3_key           = aws_s3_bucket_object.lambda_code_upload.key
  handler          = "constellation_mapper.lambda_handler"
  runtime          = "python3.9" # Or python3.11 if available in all regions
  timeout          = 300
  memory_size      = 128
  role             = aws_iam_role.lambda_exec_role.arn

  environment {
    variables = {
      PROJECT_TAG_KEY     = var.project_tag_key
      ENVIRONMENT_TAG_KEY = var.environment_tag_key
      S3_BUCKET_NAME      = aws_s3_bucket.constellation_data_bucket.id
    }
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_cloudwatch_event_rule" "schedule_rule" {
  name                = "${var.project_name}-ConstellationMapperSchedule-${random_string.suffix.result}"
  schedule_expression = var.scan_schedule_expression

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.schedule_rule.name
  target_id = "ConstellationMapperLambda"
  arn       = aws_lambda_function.constellation_mapper.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.constellation_mapper.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule_rule.arn
}
