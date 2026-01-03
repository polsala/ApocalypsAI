terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  # Provider configuration inherited from root module
}

# Lambda function for chaos execution
resource "aws_lambda_function" "chaos_monkey" {
  filename         = data.archive_file.chaos_lambda_zip.output_path
  function_name    = "${var.prefix}-chaos-monkey"
  role             = aws_iam_role.chaos_lambda_role.arn
  handler          = "index.handler"
  source_code_hash = data.archive_file.chaos_lambda_zip.output_base64sha256
  runtime          = "python3.9"
  timeout          = 300
  
  environment {
    variables = {
      RESOURCE_TYPES    = join(",", var.resource_types)
      EXCLUDE_TAGS      = jsonencode(var.exclude_tags)
      MAX_CHAOS_PER_RUN = var.max_chaos_per_run
      DRY_RUN           = var.dry_run ? "true" : "false"
      AWS_REGION        = var.aws_region
    }
  }
  
  lifecycle {
    ignore_changes = [
      # Allow manual updates to function code without recreating
      filename,
      source_code_hash
    ]
  }
}

# Lambda execution role
resource "aws_iam_role" "chaos_lambda_role" {
  name = "${var.prefix}-chaos-lambda-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Lambda execution policy
resource "aws_iam_role_policy" "chaos_lambda_policy" {
  name = "${var.prefix}-chaos-lambda-policy"
  role = aws_iam_role.chaos_lambda_role.id
  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect   = "Allow",
        Action   = [
          "ec2:DescribeInstances",
          "ec2:TerminateInstances",
          "ec2:DescribeTags",
          "rds:DescribeDBInstances",
          "rds:DeleteDBInstance",
          "elasticache:DescribeCacheClusters",
          "elasticache:DeleteCacheCluster"
        ],
        Resource = "*"
      }
    ]
  })
}

# CloudWatch Events rule for scheduling
resource "aws_cloudwatch_event_rule" "chaos_schedule" {
  name                = "${var.prefix}-chaos-schedule"
  description         = "Schedule for chaos monkey execution"
  schedule_expression = var.chaos_schedule
  
  depends_on = [
    aws_lambda_permission.chaos_event_permission
  ]
}

# Lambda permission for CloudWatch Events
resource "aws_lambda_permission" "chaos_event_permission" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chaos_monkey.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.chaos_schedule.arn
}

# CloudWatch Events target
resource "aws_cloudwatch_event_target" "chaos_target" {
  rule      = aws_cloudwatch_event_rule.chaos_schedule.name
  target_id = "ChaosMonkeyTarget"
  arn       = aws_lambda_function.chaos_monkey.arn
}

# Lambda deployment package
data "archive_file" "chaos_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/lambda/chaos_monkey.zip"
}

# Optional: SNS topic for chaos notifications
resource "aws_sns_topic" "chaos_notifications" {
  count = var.enable_notifications ? 1 : 0
  
  name = "${var.prefix}-chaos-notifications"
}

# Lambda environment variable for SNS topic
locals {
  sns_topic_arn = var.enable_notifications ? aws_sns_topic.chaos_notifications[0].arn : ""
}

# Update Lambda environment with SNS topic
resource "aws_lambda_function" "chaos_monkey" {
  # ... existing configuration ...
  
  environment {
    variables = {
      RESOURCE_TYPES    = join(",", var.resource_types)
      EXCLUDE_TAGS      = jsonencode(var.exclude_tags)
      MAX_CHAOS_PER_RUN = var.max_chaos_per_run
      DRY_RUN           = var.dry_run ? "true" : "false"
      AWS_REGION        = var.aws_region
      SNS_TOPIC_ARN     = local.sns_topic_arn
    }
  }
  
  # ... rest of configuration ...
}

# SNS subscription for notifications
resource "aws_sns_topic_subscription" "chaos_email_subscription" {
  count = var.enable_notifications && var.notification_email != "" ? 1 : 0
  
  topic_arn = aws_sns_topic.chaos_notifications[0].arn
  protocol  = "email"
  endpoint  = var.notification_email
}

# CloudWatch log group for Lambda
resource "aws_cloudwatch_log_group" "chaos_lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.chaos_monkey.function_name}"
  retention_in_days = var.log_retention_days
}

# Optional: CloudWatch dashboard for chaos metrics
resource "aws_cloudwatch_dashboard" "chaos_dashboard" {
  count = var.create_dashboard ? 1 : 0
  
  dashboard_name = "${var.prefix}-chaos-monkey-dashboard"
  
  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric",
        x      = 0,
        y      = 0,
        width  = 12,
        height = 6,
        properties = {
          metrics = [
            ["AWS/Lambda", "Invocations", "FunctionName", aws_lambda_function.chaos_monkey.function_name],
            ["AWS/Lambda", "Errors", "FunctionName", aws_lambda_function.chaos_monkey.function_name]
          ],
          period = 300,
          stat   = "Sum",
          region = var.aws_region,
          title  = "Chaos Monkey Lambda Metrics"
        }
      }
    ]
  })
}
