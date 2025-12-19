terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0"
    }
  }
}

# Random provider for chaos selection
provider "random" {}

# Variables
variable "chaos_enabled" {
  description = "Enable or disable chaos engineering"
  type        = bool
  default     = false
}

variable "chaos_interval" {
  description = "Interval between chaos cycles in minutes"
  type        = number
  default     = 60
}

variable "target_resource_types" {
  description = "List of resource types to target for chaos"
  type        = list(string)
  default     = ["aws_instance", "aws_rds_instance"]
}

variable "protected_resources" {
  description = "List of resource names to protect from chaos"
  type        = list(string)
  default     = []
}

variable "max_destructions_per_cycle" {
  description = "Maximum number of resources to destroy per chaos cycle"
  type        = number
  default     = 1
}

variable "chaos_schedule" {
  description = "Cron schedule for chaos execution"
  type        = string
  default     = "0 */6 * * *" # Every 6 hours
}

variable "dry_run" {
  description = "Enable dry run mode (logs actions but doesn't execute them)"
  type        = bool
  default     = false
}

# Random number generator for chaos selection
resource "random_integer" "chaos_selector" {
  count   = var.chaos_enabled ? 1 : 0
  min     = 1
  max     = 100
  keepers = {
    timestamp = formatdate("YYYY-MM-DD-HH", timestamp())
  }
}

# Lambda function for chaos execution
resource "aws_lambda_function" "chaos_monkey" {
  count = var.chaos_enabled ? 1 : 0
  
  filename         = data.archive_file.chaos_lambda_zip.output_path
  function_name    = "chaos-monkey-${random_integer.chaos_selector[0].result}"
  role             = aws_iam_role.chaos_lambda_role.arn
  handler          = "index.handler"
  source_code_hash = data.archive_file.chaos_lambda_zip.output_base64sha256
  runtime          = "python3.9"
  timeout          = 300
  
  environment {
    variables = {
      CHAOS_INTERVAL              = var.chaos_interval
      TARGET_RESOURCE_TYPES       = join(",", var.target_resource_types)
      PROTECTED_RESOURCES         = join(",", var.protected_resources)
      MAX_DESTRUCTIONS_PER_CYCLE  = var.max_destructions_per_cycle
      DRY_RUN                     = var.dry_run
      AWS_REGION                  = var.aws_region
    }
  }
  
  depends_on = [aws_iam_role_policy_attachment.chaos_lambda_policy]
}

# IAM role for Lambda
resource "aws_iam_role" "chaos_lambda_role" {
  count = var.chaos_enabled ? 1 : 0
  
  name = "chaos-monkey-role-${random_integer.chaos_selector[0].result}"
  
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

# IAM policy for Lambda
resource "aws_iam_policy" "chaos_lambda_policy" {
  count = var.chaos_enabled ? 1 : 0
  
  name        = "chaos-monkey-policy-${random_integer.chaos_selector[0].result}"
  description = "Policy for chaos monkey lambda function"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:DescribeInstances",
          "ec2:TerminateInstances",
          "rds:DescribeDBInstances",
          "rds:DeleteDBInstance",
          "lambda:ListFunctions",
          "lambda:DeleteFunction"
        ]
        Resource = "*"
      }
    ]
  })
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "chaos_lambda_policy" {
  count = var.chaos_enabled ? 1 : 0
  
  role       = aws_iam_role.chaos_lambda_role[0].name
  policy_arn = aws_iam_policy.chaos_lambda_policy[0].arn
}

# CloudWatch Events rule for scheduling
resource "aws_cloudwatch_event_rule" "chaos_schedule" {
  count = var.chaos_enabled ? 1 : 0
  
  name                = "chaos-monkey-schedule-${random_integer.chaos_selector[0].result}"
  description         = "Schedule for chaos monkey execution"
  schedule_expression = "cron(${var.chaos_schedule})"
}

# CloudWatch Events target
resource "aws_cloudwatch_event_target" "chaos_lambda_target" {
  count = var.chaos_enabled ? 1 : 0
  
  rule      = aws_cloudwatch_event_rule.chaos_schedule[0].name
  target_id = "chaosMonkeyTarget"
  arn       = aws_lambda_function.chaos_monkey[0].arn
}

# Lambda permission for CloudWatch Events
resource "aws_lambda_permission" "allow_cloudwatch" {
  count = var.chaos_enabled ? 1 : 0
  
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chaos_monkey[0].function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.chaos_schedule[0].arn
}

# CloudWatch log group for Lambda
resource "aws_cloudwatch_log_group" "chaos_lambda_logs" {
  count  = var.chaos_enabled ? 1 : 0
  name   = "/aws/lambda/${aws_lambda_function.chaos_monkey[0].function_name}"
  retention_in_days = 7
}

# Lambda function code archive
data "archive_file" "chaos_lambda_zip" {
  count        = var.chaos_enabled ? 1 : 0
  type         = "zip"
  source_dir   = "${path.module}/lambda"
  output_path  = "${path.module}/chaos_lambda.zip"
  output_base64sha256 = true
}

# Outputs
output "chaos_enabled" {
  description = "Whether chaos engineering is enabled"
  value       = var.chaos_enabled
}

output "chaos_schedule" {
  description = "Cron schedule for chaos execution"
  value       = var.chaos_schedule
}

output "chaos_lambda_arn" {
  description = "ARN of the chaos monkey lambda function"
  value       = var.chaos_enabled ? aws_lambda_function.chaos_monkey[0].arn : ""
  sensitive   = true
}

output "protected_resources" {
  description = "Resources protected from chaos"
  value       = var.protected_resources
}
