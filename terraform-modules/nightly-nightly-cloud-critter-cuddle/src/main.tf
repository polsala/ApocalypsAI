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
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}

provider "aws" {
  region = "us-east-1" # Default region, can be overridden by AWS_REGION env var
}

resource "aws_instance" "critter" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  subnet_id     = var.subnet_id
  vpc_security_group_ids = [aws_security_group.critter_sg.id]

  tags = merge(var.tags, {
    Name = "${var.name}-critter-instance"
  })
}

resource "aws_s3_bucket" "critter_data" {
  bucket = "${var.name}-critter-data-${random_id.bucket_suffix.hex}"
  acl    = "private"

  tags = merge(var.tags, {
    Name = "${var.name}-critter-data-bucket"
  })
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_security_group" "critter_sg" {
  name        = "${var.name}-critter-sg"
  description = "Security group for the Cloud Critter Cuddler EC2 instance"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # WARNING: For dev/test only. Restrict in production.
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.name}-critter-sg"
  })
}

# IAM Role for Lambda to stop/start EC2
resource "aws_iam_role" "critter_lambda_role" {
  name = "${var.name}-critter-lambda-role"

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

  tags = merge(var.tags, {
    Name = "${var.name}-critter-lambda-role"
  })
}

resource "aws_iam_role_policy" "critter_lambda_policy" {
  name = "${var.name}-critter-lambda-policy"
  role = aws_iam_role.critter_lambda_role.id

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
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Action = [
          "ec2:StartInstances",
          "ec2:StopInstances",
          "ec2:DescribeInstances",
        ],
        Effect   = "Allow",
        Resource = "arn:aws:ec2:*:*:instance/${aws_instance.critter.id}"
      },
      {
        Action = [
          "ec2:DescribeInstances",
        ],
        Effect   = "Allow",
        Resource = "*" # Required for DescribeInstances to find the instance by tag
      }
    ]
  })
}

# Archive the Lambda function code
data "archive_file" "critter_manager_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_critter_manager.py"
  output_path = "${path.module}/lambda_critter_manager.zip"
}

# Lambda function to stop/start the EC2 instance
resource "aws_lambda_function" "critter_manager" {
  function_name = "${var.name}-critter-manager"
  handler       = "lambda_critter_manager.handler"
  runtime       = "python3.9"
  role          = aws_iam_role.critter_lambda_role.arn
  timeout       = 30

  filename         = data.archive_file.critter_manager_zip.output_path
  source_code_hash = data.archive_file.critter_manager_zip.output_base64sha256

  environment {
    variables = {
      INSTANCE_ID = aws_instance.critter.id
    }
  }

  tags = merge(var.tags, {
    Name = "${var.name}-critter-manager-lambda"
  })
}

# CloudWatch Event Rule for stopping the instance
resource "aws_cloudwatch_event_rule" "critter_sleep_schedule" {
  name                = "${var.name}-critter-sleep-schedule"
  description         = "Schedule to stop the Cloud Critter EC2 instance"
  schedule_expression = var.sleep_cron_expression

  tags = merge(var.tags, {
    Name = "${var.name}-critter-sleep-schedule"
  })
}

resource "aws_cloudwatch_event_target" "critter_sleep_target" {
  rule      = aws_cloudwatch_event_rule.critter_sleep_schedule.name
  target_id = "critter-sleep-lambda"
  arn       = aws_lambda_function.critter_manager.arn
  input     = jsonencode({ "action": "stop" })
}

resource "aws_lambda_permission" "critter_sleep_permission" {
  statement_id  = "AllowExecutionFromCloudWatchSleep"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.critter_manager.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.critter_sleep_schedule.arn
}

# CloudWatch Event Rule for starting the instance
resource "aws_cloudwatch_event_rule" "critter_wake_schedule" {
  name                = "${var.name}-critter-wake-schedule"
  description         = "Schedule to start the Cloud Critter EC2 instance"
  schedule_expression = var.wake_cron_expression

  tags = merge(var.tags, {
    Name = "${var.name}-critter-wake-schedule"
  })
}

resource "aws_cloudwatch_event_target" "critter_wake_target" {
  rule      = aws_cloudwatch_event_rule.critter_wake_schedule.name
  target_id = "critter-wake-lambda"
  arn       = aws_lambda_function.critter_manager.arn
  input     = jsonencode({ "action": "start" })
}

resource "aws_lambda_permission" "critter_wake_permission" {
  statement_id  = "AllowExecutionFromCloudWatchWake"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.critter_manager.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.critter_wake_schedule.arn
}
