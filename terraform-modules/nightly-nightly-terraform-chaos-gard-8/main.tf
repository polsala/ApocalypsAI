terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# Random whimsical names for chaos experiments
resource "random_pet" "chaos_garden_name" {
  count = length(var.chaos_scenarios)
}

# S3 bucket for chaos experiment logs
resource "aws_s3_bucket" "chaos_logs" {
  bucket = "${var.environment}-chaos-garden-logs-${random_pet.chaos_garden_name[0].id}"
  force_destroy = true

  tags = {
    Environment = var.environment
    Purpose     = "chaos-engineering"
    Terraform   = "true"
  }
}

# S3 bucket policy for chaos logs
resource "aws_s3_bucket_policy" "chaos_logs_policy" {
  bucket = aws_s3_bucket.chaos_logs.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Principal = "*"
        Action   = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.chaos_logs.arn}/*"
      }
    ]
  })
}

# Lambda function for chaos orchestration
resource "aws_lambda_function" "chaos_orchestrator" {
  filename         = data.archive_file.chaos_orchestrator_zip.output_path
  function_name    = "${var.environment}-chaos-orchestrator"
  role            = aws_iam_role.chaos_orchestrator.arn
  handler         = "index.handler"
  source_code_hash = data.archive_file.chaos_orchestrator_zip.output_base64sha256
  runtime         = "python3.9"
  timeout         = 300

  environment {
    variables = {
      ENVIRONMENT          = var.environment
      REGION              = var.region
      CHAOS_SCENARIOS     = join(",", var.chaos_scenarios)
      EXPERIMENT_DURATION = var.experiment_duration
      MAX_EXPERIMENTS     = var.max_concurrent_experiments
      ROLLBACK_ENABLED    = var.rollback_enabled
      LOG_BUCKET          = aws_s3_bucket.chaos_logs.id
    }
  }

  tags = {
    Environment = var.environment
    Purpose     = "chaos-engineering"
    Terraform   = "true"
  }
}

# Lambda function code archive
data "archive_file" "chaos_orchestrator_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/chaos_orchestrator.zip"
}

# IAM role for chaos orchestrator
resource "aws_iam_role" "chaos_orchestrator" {
  name = "${var.environment}-chaos-orchestrator-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM policy for chaos orchestrator
resource "aws_iam_policy" "chaos_orchestrator_policy" {
  name        = "${var.environment}-chaos-orchestrator-policy"
  description = "Policy for chaos orchestrator Lambda function"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect   = "Allow"
        Action   = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.chaos_logs.arn,
          "${aws_s3_bucket.chaos_logs.arn}/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = [
          "ec2:DescribeInstances",
          "ec2:StopInstances",
          "ec2:StartInstances",
          "ec2:CreateNetworkAclEntry",
          "ec2:DeleteNetworkAclEntry"
        ]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = [
          "cloudwatch:PutMetricData",
          "cloudwatch:GetMetricStatistics"
        ]
        Resource = "*"
      }
    ]
  })
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "chaos_orchestrator_policy_attachment" {
  role       = aws_iam_role.chaos_orchestrator.name
  policy_arn = aws_iam_policy.chaos_orchestrator_policy.arn
}

# CloudWatch log group for Lambda
resource "aws_cloudwatch_log_group" "chaos_orchestrator_logs" {
  name              = "/aws/lambda/${aws_lambda_function.chaos_orchestrator.function_name}"
  retention_in_days = 7
}

# EventBridge rule for chaos experiments
resource "aws_cloudwatch_event_rule" "chaos_schedule" {
  name        = "${var.environment}-chaos-schedule"
  description = "Schedule for chaos experiments"
  schedule_expression = "rate(1 hour)"
}

# EventBridge target for Lambda
resource "aws_cloudwatch_event_target" "chaos_lambda_target" {
  rule      = aws_cloudwatch_event_rule.chaos_schedule.name
  target_id = "ChaosOrchestratorTarget"
  arn       = aws_lambda_function.chaos_orchestrator.arn
}

# Grant Lambda permission to be invoked by EventBridge
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chaos_orchestrator.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.chaos_schedule.arn
}

# SNS topic for chaos experiment alerts
resource "aws_sns_topic" "chaos_alerts" {
  name = "${var.environment}-chaos-alerts"

  tags = {
    Environment = var.environment
    Purpose     = "chaos-engineering"
    Terraform   = "true"
  }
}

# SNS subscription for email alerts
resource "aws_sns_topic_subscription" "chaos_email_alerts" {
  count  = var.alert_email != "" ? 1 : 0
  topic_arn = aws_sns_topic.chaos_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# CloudWatch alarm for chaos experiment failures
resource "aws_cloudwatch_metric_alarm" "chaos_failure_alarm" {
  alarm_name          = "${var.environment}-chaos-experiment-failures"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "ChaosExperimentFailures"
  namespace           = "ChaosEngineering"
  period              = "300"
  statistic           = "Sum"
  threshold           = "0"
  alarm_description   = "This metric monitors chaos experiment failures"
  alarm_actions       = [aws_sns_topic.chaos_alerts.arn]
  dimensions = {
    Environment = var.environment
  }
}

# API Gateway for chaos garden dashboard
resource "aws_api_gateway_rest_api" "chaos_garden_api" {
  name        = "${var.environment}-chaos-garden-api"
  description = "API for chaos garden dashboard"

  tags = {
    Environment = var.environment
    Purpose     = "chaos-engineering"
    Terraform   = "true"
  }
}

# API Gateway resource for experiments
resource "aws_api_gateway_resource" "experiments" {
  rest_api_id = aws_api_gateway_rest_api.chaos_garden_api.id
  parent_id   = aws_api_gateway_rest_api.chaos_garden_api.root_resource_id
  path_part   = "experiments"
}

# API Gateway method for getting experiments
resource "aws_api_gateway_method" "experiments_get" {
  rest_api_id   = aws_api_gateway_rest_api.chaos_garden_api.id
  resource_id   = aws_api_gateway_resource.experiments.id
  http_method   = "GET"
  authorization = "NONE"
}

# API Gateway integration for Lambda
resource "aws_api_gateway_integration" "experiments_lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.chaos_garden_api.id
  resource_id = aws_api_gateway_resource.experiments.id
  http_method = aws_api_gateway_method.experiments_get.http_method

  integration_http_method = "POST"
  type                      = "AWS_PROXY"
  uri                       = aws_lambda_function.chaos_orchestrator.invoke_arn
}

# Grant API Gateway permission to invoke Lambda
resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chaos_orchestrator.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.chaos_garden_api.execution_arn}*/${aws_api_gateway_method.experiments_get.http_method}/${aws_api_gateway_resource.experiments.path}"
}

# Deploy API Gateway
resource "aws_api_gateway_deployment" "chaos_garden_deployment" {
  depends_on = [aws_api_gateway_integration.experiments_lambda_integration]

  rest_api_id = aws_api_gateway_rest_api.chaos_garden_api.id
  stage_name  = "prod"

  variables = {
    stage = var.environment
  }
}

# Output variables
output "chaos_garden_url" {
  description = "URL to access the chaos garden dashboard"
  value       = "${aws_api_gateway_rest_api.chaos_garden_api.id}.execute-api.${var.region}.amazonaws.com/prod/experiments"
}

output "experiment_results" {
  description = "S3 bucket containing experiment results"
  value       = aws_s3_bucket.chaos_logs.id
  sensitive   = true
}

output "monitoring_dashboard_url" {
  description = "CloudWatch dashboard for monitoring chaos experiments"
  value       = "https://console.aws.amazon.com/cloudwatch/home?region=${var.region}#alarmsV2:alarm/chaos-experiment-failures"
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic for chaos alerts"
  value       = aws_sns_topic.chaos_alerts.arn
}

output "lambda_function_arn" {
  description = "ARN of the chaos orchestrator Lambda function"
  value       = aws_lambda_function.chaos_orchestrator.arn
}
