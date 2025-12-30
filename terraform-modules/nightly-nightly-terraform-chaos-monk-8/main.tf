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

# Configuration variables
variable "enabled" {
  description = "Enable chaos monkey functionality"
  type        = bool
  default     = false
}

variable "chaos_probability" {
  description = "Probability (0.0-1.0) of chaos per hour"
  type        = number
  default     = 0.01
  validation {
    condition     = var.chaos_probability >= 0 && var.chaos_probability <= 1
    error_message = "Chaos probability must be between 0 and 1."
  }
}

variable "target_resource_types" {
  description = "Resource types to target for chaos"
  type        = list(string)
  default     = ["aws_instance"]
}

variable "excluded_tags" {
  description = "Tags that exclude resources from chaos"
  type        = map(string)
  default     = {}
}

variable "safe_mode" {
  description = "Enable safety checks and confirmations"
  type        = bool
  default     = true
}

variable "time_window_start" {
  description = "Start hour for chaos (0-23)"
  type        = number
  default     = 9
  validation {
    condition     = var.time_window_start >= 0 && var.time_window_start <= 23
    error_message = "Time window start must be between 0 and 23."
  }
}

variable "time_window_end" {
  description = "End hour for chaos (0-23)"
  type        = number
  default     = 17
  validation {
    condition     = var.time_window_end >= 0 && var.time_window_end <= 23
    error_message = "Time window end must be between 0 and 23."
  }
}

# Random number generator for chaos decision
resource "random_integer" "chaos_trigger" {
  count = var.enabled ? 1 : 0
  
  min = 1
  max = 100
  
  # Only regenerate during specific time windows
  lifecycle {
    ignore_changes = [
      # Only change during business hours (configurable)
      # This is handled by the time window logic below
    ]
  }
}

# Lambda function for chaos execution
resource "aws_lambda_function" "chaos_executor" {
  count = var.enabled ? 1 : 0
  
  filename         = data.archive_file.chaos_lambda_zip.output_path
  function_name    = "${var.environment_name}-chaos-monkey"
  role             = aws_iam_role.chaos_lambda_role.arn
  handler          = "index.handler"
  source_code_hash = data.archive_file.chaos_lambda_zip.output_base64sha256
  runtime          = "python3.9"
  timeout          = 300
  
  environment {
    variables = {
      CHAOS_PROBABILITY      = var.chaos_probability
      TARGET_RESOURCE_TYPES  = join(",", var.target_resource_types)
      EXCLUDED_TAGS          = jsonencode(var.excluded_tags)
      SAFE_MODE             = var.safe_mode
      TIME_WINDOW_START     = var.time_window_start
      TIME_WINDOW_END       = var.time_window_end
    }
  }
  
  # Add VPC configuration if needed
  # vpc_config {
  #   subnet_ids         = var.subnet_ids
  #   security_group_ids = var.security_group_ids
  # }
}

# Lambda function code
resource "aws_cloudwatch_log_group" "chaos_logs" {
  count = var.enabled ? 1 : 0
  
  name              = "/aws/lambda/${aws_lambda_function.chaos_executor[0].function_name}"
  retention_in_days = 7
}

# IAM role for Lambda
resource "aws_iam_role" "chaos_lambda_role" {
  count = var.enabled ? 1 : 0
  
  name = "${var.environment_name}-chaos-monkey-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# IAM policy for Lambda
resource "aws_iam_policy" "chaos_lambda_policy" {
  count = var.enabled ? 1 : 0
  
  name        = "${var.environment_name}-chaos-monkey-policy"
  description = "Policy for chaos monkey Lambda function"
  
  policy = jsonencode({
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
          "ec2:DescribeInstances",
          "ec2:TerminateInstances",
          "rds:DescribeDBInstances",
          "rds:DeleteDBInstance",
          "elasticloadbalancing:DescribeLoadBalancers",
          "elasticloadbalancing:DeregisterInstancesFromLoadBalancer"
        ]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = [
          "cloudwatch:PutMetricData"
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "cloudwatch:namespace" = "ChaosMonkey"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "chaos_lambda_policy_attach" {
  count = var.enabled ? 1 : 0
  
  role       = aws_iam_role.chaos_lambda_role[0].name
  policy_arn = aws_iam_policy.chaos_lambda_policy[0].arn
}

# CloudWatch Event Rule for scheduling chaos
resource "aws_cloudwatch_event_rule" "chaos_schedule" {
  count = var.enabled ? 1 : 0
  
  name                = "${var.environment_name}-chaos-monkey-schedule"
  description         = "Schedule for chaos monkey execution"
  schedule_expression = "rate(1 hour)"
  
  # Add time window filtering
  event_pattern = jsonencode({
    source      = ["aws.events"],
    detail-type = ["Scheduled Event"],
    detail = {
      time = [{
        "numeric": [">=", var.time_window_start * 100, "<=", var.time_window_end * 100]
      }]
    }
  })
}

resource "aws_cloudwatch_event_target" "chaos_target" {
  count = var.enabled ? 1 : 0
  
  rule      = aws_cloudwatch_event_rule.chaos_schedule[0].name
  target_id = "ChaosMonkeyTarget"
  arn       = aws_lambda_function.chaos_executor[0].arn
}

# Allow CloudWatch Events to invoke Lambda
resource "aws_lambda_permission" "allow_cloudwatch" {
  count = var.enabled ? 1 : 0
  
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chaos_executor[0].function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.chaos_schedule[0].arn
}

# Lambda function code archive
data "archive_file" "chaos_lambda_zip" {
  count = var.enabled ? 1 : 0
  
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/chaos_lambda.zip"
}

# CloudWatch metrics for monitoring
resource "aws_cloudwatch_metric_alarm" "chaos_events_alarm" {
  count = var.enabled ? 1 : 0
  
  alarm_name          = "${var.environment_name}-chaos-events-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "ChaosEvents"
  namespace           = "ChaosMonkey"
  period              = "3600"
  statistic           = "Sum"
  threshold           = "5"
  alarm_description   = "Too many chaos events in the last hour"
  alarm_actions       = var.alarm_sns_topic_arn != "" ? [var.alarm_sns_topic_arn] : []
}

# Outputs
output "chaos_enabled" {
  description = "Whether chaos monkey is enabled"
  value       = var.enabled
}

output "chaos_probability" {
  description = "Current chaos probability setting"
  value       = var.chaos_probability
}

output "chaos_lambda_arn" {
  description = "ARN of the chaos monkey Lambda function"
  value       = var.enabled ? aws_lambda_function.chaos_executor[0].arn : ""
  sensitive   = true
}

output "chaos_schedule_rule" {
  description = "CloudWatch Event Rule for chaos schedule"
  value       = var.enabled ? aws_cloudwatch_event_rule.chaos_schedule[0].name : ""
}

# Variables for environment name and SNS topic
variable "environment_name" {
  description = "Name of the environment (e.g., production, staging)"
  type        = string
  default     = "nightly"
}

variable "alarm_sns_topic_arn" {
  description = "SNS topic ARN for chaos event alarms"
  type        = string
  default     = ""
}
