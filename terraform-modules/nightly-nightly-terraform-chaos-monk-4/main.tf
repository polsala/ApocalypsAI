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

# Variables
variable "chaos_level" {
  description = "Level of chaos to introduce (gentle, medium, extreme)"
  type        = string
  default     = "medium"
  validation {
    condition     = contains(["gentle", "medium", "extreme"], var.chaos_level)
    error_message = "Chaos level must be one of: gentle, medium, extreme."
  }
}

variable "enabled" {
  description = "Whether chaos monkey is enabled"
  type        = bool
  default     = true
}

variable "target_instances" {
  description = "List of EC2 instance IDs to target for chaos"
  type        = list(string)
  default     = []
}

variable "minimum_instance_count" {
  description = "Minimum number of instances to keep running"
  type        = number
  default     = 1
}

variable "chaos_schedule" {
  description = "Cron expression for when chaos can occur"
  type        = string
  default     = "cron(0/30 * * * ? *)" # Every 30 minutes
}

variable "dry_run" {
  description = "Enable dry run mode (no actual disruption)"
  type        = bool
  default     = false
}

# Random number generator for chaos decisions
resource "random_integer" "chaos_trigger" {
  count   = var.enabled ? 1 : 0
  min     = 1
  max     = 100
  keepers = {
    timestamp = timestamp()
    schedule  = var.chaos_schedule
  }
}

# Calculate chaos probability based on level
locals {
  chaos_probability = {
    gentle  = 1
    medium  = 5
    extreme = 15
  }[var.chaos_level]
  
  should_trigger_chaos = var.enabled && (
    random_integer.chaos_trigger[0].result <= local.chaos_probability
  )
  
  safe_to_chaos = length(var.target_instances) > var.minimum_instance_count
}

# Chaos event resource (only creates when conditions are met)
resource "null_resource" "chaos_event" {
  count = var.enabled && local.should_trigger_chaos && local.safe_to_chaos ? 1 : 0
  
  triggers = {
    instance_id = element(var.target_instances, random_integer.chaos_trigger[0].result % length(var.target_instances))
    timestamp   = timestamp()
    chaos_type  = "instance_termination"
  }
  
  provisioner "local-exec" {
    when    = destroy
    command = var.dry_run ? "echo '[DRY RUN] Would terminate instance ${self.triggers.instance_id}'" : "aws ec2 terminate-instances --instance-ids ${self.triggers.instance_id}"
  }
  
  lifecycle {
    ignore_changes = [
      triggers.timestamp
    ]
  }
}

# CloudWatch Log Group for chaos events
resource "aws_cloudwatch_log_group" "chaos_events" {
  name              = "/apocalypsaid/chaos-monkey"
  retention_in_days = 30
}

# CloudWatch Log Stream for chaos events
resource "aws_cloudwatch_log_stream" "chaos_events_stream" {
  name           = "chaos-events"
  log_group_name = aws_cloudwatch_log_group.chaos_events.name
}

# Lambda function to log chaos events
resource "aws_lambda_function" "chaos_logger" {
  filename         = data.archive_file.chaos_logger_lambda.output_path
  function_name    = "chaos-monkey-logger"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "index.handler"
  source_code_hash = data.archive_file.chaos_logger_lambda.output_base64sha256
  runtime          = "python3.9"
  
  environment {
    variables = {
      LOG_GROUP_NAME = aws_cloudwatch_log_group.chaos_events.name
      LOG_STREAM_NAME = aws_cloudwatch_log_stream.chaos_events_stream.name
    }
  }
}

# Lambda deployment package
data "archive_file" "chaos_logger_lambda" {
  type        = "zip"
  output_path = "${path.module}/lambda/chaos_logger.zip"
  source {
    content = <<-EOF
import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cloudwatch = boto3.client('logs')

LOG_GROUP_NAME = os.environ['LOG_GROUP_NAME']
LOG_STREAM_NAME = os.environ['LOG_STREAM_NAME']

def handler(event, context):
    try:
        # Get existing log stream sequence token
        try:
            response = cloudwatch.describe_log_streams(
                logGroupName=LOG_GROUP_NAME,
                logStreamNamePrefix=LOG_STREAM_NAME
            )
            log_stream = next(
                (stream for stream in response['logStreams'] if stream['logStreamName'] == LOG_STREAM_NAME),
                None
            )
            sequence_token = log_stream['uploadSequenceToken'] if log_stream else None
        except Exception as e:
            logger.warning(f"Could not get sequence token: {e}")
            sequence_token = None
        
        # Prepare log event
        log_event = {
            'timestamp': int(event.get('timestamp', 0)),
            'message': json.dumps({
                'event_type': 'chaos_monkey_event',
                'instance_id': event.get('instance_id', 'unknown'),
                'chaos_type': event.get('chaos_type', 'unknown'),
                'dry_run': event.get('dry_run', False),
                'timestamp': event.get('timestamp', 0)
            })
        }
        
        # Put log event
        kwargs = {
            'logGroupName': LOG_GROUP_NAME,
            'logStreamName': LOG_STREAM_NAME,
            'logEvents': [log_event]
        }
        
        if sequence_token:
            kwargs['sequenceToken'] = sequence_token
        
        cloudwatch.put_log_events(**kwargs)
        
        return {'statusCode': 200, 'body': 'Log event recorded'}
        
    except Exception as e:
        logger.error(f"Error logging chaos event: {e}")
        return {'statusCode': 500, 'body': f'Error: {str(e)}'}
EOF
    filename = "index.py"
  }
}

# IAM Role for Lambda execution
resource "aws_iam_role" "lambda_exec" {
  name = "chaos-monkey-lambda-exec"
  
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

# IAM Policy for Lambda
resource "aws_iam_policy" "lambda_policy" {
  name        = "chaos-monkey-lambda-policy"
  description = "Policy for chaos monkey lambda to write to CloudWatch Logs"
  
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
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# EventBridge rule to trigger chaos
resource "aws_cloudwatch_event_rule" "chaos_schedule" {
  count  = var.enabled ? 1 : 0
  name   = "chaos-monkey-schedule"
  schedule_expression = var.chaos_schedule
}

resource "aws_cloudwatch_event_target" "chaos_lambda_target" {
  count      = var.enabled ? 1 : 0
  rule       = aws_cloudwatch_event_rule.chaos_schedule[0].name
  target_id  = "ChaosMonkeyLambda"
  arn        = aws_lambda_function.chaos_logger.arn
}

# Output variables
output "chaos_enabled" {
  description = "Whether chaos monkey is enabled"
  value       = var.enabled
}

output "chaos_level" {
  description = "Current chaos level"
  value       = var.chaos_level
}

output "chaos_schedule" {
  description = "Cron schedule for chaos events"
  value       = var.chaos_schedule
}

output "log_group_name" {
  description = "CloudWatch Log Group for chaos events"
  value       = aws_cloudwatch_log_group.chaos_events.name
}

output "target_instance_count" {
  description = "Number of target instances"
  value       = length(var.target_instances)
}

output "dry_run_mode" {
  description = "Whether dry run mode is enabled"
  value       = var.dry_run
}
