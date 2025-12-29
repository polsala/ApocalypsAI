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

# Input variables
variable "enabled" {
  description = "Enable/disable the chaos monkey"
  type        = bool
  default     = false
}

variable "destruction_probability" {
  description = "Probability (0.0-1.0) of destroying a resource"
  type        = number
  default     = 0.05
  validation {
    condition     = var.destruction_probability >= 0 && var.destruction_probability <= 1
    error_message = "Destruction probability must be between 0 and 1."
  }
}

variable "target_resource_types" {
  description = "Resource types to target for chaos"
  type        = list(string)
  default     = []
}

variable "chaos_schedule" {
  description = "Cron schedule for chaos execution"
  type        = string
  default     = "0 2 * * *"
}

variable "safe_mode" {
  description = "Log actions without actually destroying resources"
  type        = bool
  default     = true
}

variable "max_resources_per_run" {
  description = "Maximum number of resources to destroy per chaos run"
  type        = number
  default     = 3
}

variable "excluded_resources" {
  description = "Resource IDs to exclude from chaos"
  type        = list(string)
  default     = []
}

variable "aws_region" {
  description = "AWS region for chaos operations"
  type        = string
  default     = "us-east-1"
}

# Random number generator for chaos decisions
resource "random_integer" "chaos_seed" {
  min = 0
  max = 100
}

# Lambda function for chaos execution
resource "aws_lambda_function" "chaos_monkey" {
  count = var.enabled ? 1 : 0

  filename         = data.archive_file.chaos_lambda_zip.output_path
  function_name    = "chaos-monkey-${random_pet.chaos_suffix.id}"
  role             = aws_iam_role.chaos_lambda_role.arn
  handler          = "index.handler"
  source_code_hash = data.archive_file.chaos_lambda_zip.output_base64sha256
  runtime          = "python3.9"
  timeout          = 300

  environment {
    variables = {
      DESTRUCTION_PROBABILITY = var.destruction_probability
      TARGET_RESOURCE_TYPES   = join(",", var.target_resource_types)
      SAFE_MODE               = var.safe_mode
      MAX_RESOURCES_PER_RUN   = var.max_resources_per_run
      EXCLUDED_RESOURCES      = join(",", var.excluded_resources)
      AWS_REGION              = var.aws_region
    }
  }
}

# Lambda execution role
resource "aws_iam_role" "chaos_lambda_role" {
  count = var.enabled ? 1 : 0

  name = "chaos-monkey-role-${random_pet.chaos_suffix.id}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Lambda execution policy
resource "aws_iam_role_policy" "chaos_lambda_policy" {
  count = var.enabled ? 1 : 0

  name = "chaos-monkey-policy-${random_pet.chaos_suffix.id}"
  role = aws_iam_role.chaos_lambda_role[0].id

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
          "ec2:RunInstances",
          "rds:DescribeDBInstances",
          "rds:DeleteDBInstance",
          "rds:CreateDBInstance",
          "s3:ListBuckets",
          "s3:DeleteBucket",
          "s3:CreateBucket",
          "lambda:ListFunctions",
          "lambda:DeleteFunction",
          "lambda:CreateFunction"
        ]
        Resource = "*"
      }
    ]
  })
}

# CloudWatch Event Rule for scheduling
resource "aws_cloudwatch_event_rule" "chaos_schedule" {
  count = var.enabled ? 1 : 0

  name                = "chaos-monkey-schedule-${random_pet.chaos_suffix.id}"
  description         = "Schedule for chaos monkey execution"
  schedule_expression = var.chaos_schedule
}

# CloudWatch Event Target to invoke Lambda
resource "aws_cloudwatch_event_target" "chaos_lambda_target" {
  count = var.enabled ? 1 : 0

  rule      = aws_cloudwatch_event_rule.chaos_schedule[0].name
  target_id = "chaosMonkeyTarget"
  arn       = aws_lambda_function.chaos_monkey[0].arn
}

# Lambda permission for CloudWatch Events
resource "aws_lambda_permission" "allow_cloudwatch" {
  count = var.enabled ? 1 : 0

  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chaos_monkey[0].function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.chaos_schedule[0].arn
}

# Lambda function code archive
data "archive_file" "chaos_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/chaos_lambda.zip"
}

# Random suffix for unique naming
resource "random_pet" "chaos_suffix" {
  length = 2
}

# Outputs
output "chaos_monkey_enabled" {
  description = "Whether the chaos monkey is enabled"
  value       = var.enabled
}

output "chaos_schedule" {
  description = "Cron schedule for chaos execution"
  value       = var.chaos_schedule
}

output "safe_mode" {
  description = "Whether safe mode is enabled"
  value       = var.safe_mode
}

output "lambda_function_arn" {
  description = "ARN of the chaos monkey Lambda function"
  value       = var.enabled ? aws_lambda_function.chaos_monkey[0].arn : ""
  sensitive   = true
}

output "lambda_function_name" {
  description = "Name of the chaos monkey Lambda function"
  value       = var.enabled ? aws_lambda_function.chaos_monkey[0].function_name : ""
}

# Data sources for resource discovery
# Note: These would be implemented in the Lambda function itself
# for dynamic resource discovery, but we include them here for completeness

data "aws_instances" "all_instances" {
  filter {
    name   = "instance-state-name"
    values = ["running"]
  }
}

# Conditional resources based on target types
locals {
  target_ec2_instances = contains(var.target_resource_types, "aws_instance") ? data.aws_instances.all_instances.ids : []
}

# Resource count output for monitoring
output "target_resource_count" {
  description = "Number of resources that could be targeted"
  value       = length(local.target_ec2_instances)
}
