provider "aws" {
  region = var.aws_region
}

locals {
  lambda_python_code = <<EOT
import boto3
import os
import json

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    action = event.get('action')
    instance_tags = event.get('instance_tags', {})

    if not action or action not in ['stop', 'start']:
        print(f"Invalid action: {action}. Must be 'stop' or 'start'.")
        return {
            'statusCode': 400,
            'body': json.dumps(f"Invalid action: {action}")
        }

    if not instance_tags:
        print("No instance tags provided. Skipping EC2 action.")
        return {
            'statusCode': 200,
            'body': json.dumps("No instance tags provided.")
        }

    filters = []
    for key, value in instance_tags.items():
        filters.append({'Name': f'tag:{key}', 'Values': [value]})
    
    # Add filter for running/stopped state to avoid errors
    if action == 'stop':
        filters.append({'Name': 'instance-state-name', 'Values': ['running']})
    elif action == 'start':
        filters.append({'Name': 'instance-state-name', 'Values': ['stopped']})

    try:
        response = ec2.describe_instances(Filters=filters)
        instance_ids = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_ids.append(instance['InstanceId'])

        if not instance_ids:
            print(f"No EC2 instances found with tags {instance_tags} in state for {action}.")
            return {
                'statusCode': 200,
                'body': json.dumps(f"No instances found for {action}.")
            }

        print(f"Found instances for {action}: {instance_ids}")

        if action == 'stop':
            ec2.stop_instances(InstanceIds=instance_ids)
            message = f"Initiated slumber for instances: {instance_ids}"
        elif action == 'start':
            ec2.start_instances(InstanceIds=instance_ids)
            message = f"Initiated awakening for instances: {instance_ids}"
        
        print(message)
        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }

    except Exception as e:
        print(f"Error performing EC2 action '{action}': {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
EOT
}

resource "local_file" "lambda_main_py" {
  content  = local.lambda_python_code
  filename = "${path.module}/main.py"
}

data "archive_file" "slumber_manager_zip" {
  type        = "zip"
  source_file = local_file.lambda_main_py.filename
  output_path = "${path.module}/slumber_manager.zip"
  # Mock rationale: This data source creates a local zip file, which is a deterministic, offline operation.
  # It ensures the Lambda code is packaged correctly for `terraform plan` to validate the `source_code_hash`.
}

resource "aws_iam_role" "slumber_manager_role" {
  name = "slumber-manager-lambda-role-${random_id.suffix.hex}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "slumber_manager_policy" {
  name = "slumber-manager-lambda-policy-${random_id.suffix.hex}"
  role = aws_iam_role.slumber_manager_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "ec2:DescribeInstances",
          "ec2:StopInstances",
          "ec2:StartInstances"
        ],
        Effect   = "Allow",
        Resource = "*" # Restrict this in production by instance ARN if possible
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect   = "Allow",
        Resource = "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/*:*"
      }
    ]
  })
}

resource "aws_lambda_function" "slumber_manager" {
  function_name    = "ec2-slumber-manager-${random_id.suffix.hex}"
  handler          = "main.lambda_handler"
  runtime          = "python3.9"
  role             = aws_iam_role.slumber_manager_role.arn
  memory_size      = var.lambda_memory_size
  timeout          = var.lambda_timeout

  filename         = data.archive_file.slumber_manager_zip.output_path
  source_code_hash = data.archive_file.slumber_manager_zip.output_base64sha256
}

resource "aws_cloudwatch_event_rule" "slumber_time_trigger" {
  name                = "ec2-slumber-time-trigger-${random_id.suffix.hex}"
  schedule_expression = var.stop_cron_schedule
}

resource "aws_cloudwatch_event_target" "slumber_time_target" {
  rule      = aws_cloudwatch_event_rule.slumber_time_trigger.name
  target_id = "slumber-manager-stop"
  arn       = aws_lambda_function.slumber_manager.arn

  input = jsonencode({
    action        = "stop",
    instance_tags = var.instance_tags
  })
}

resource "aws_lambda_permission" "slumber_time_permission" {
  statement_id  = "AllowExecutionFromCloudWatchSlumber-${random_id.suffix.hex}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.slumber_manager.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.slumber_time_trigger.arn
}

resource "aws_cloudwatch_event_rule" "wake_up_call_trigger" {
  name                = "ec2-wake-up-call-trigger-${random_id.suffix.hex}"
  schedule_expression = var.start_cron_schedule
}

resource "aws_cloudwatch_event_target" "wake_up_call_target" {
  rule      = aws_cloudwatch_event_rule.wake_up_call_trigger.name
  target_id = "slumber-manager-start"
  arn       = aws_lambda_function.slumber_manager.arn

  input = jsonencode({
    action        = "start",
    instance_tags = var.instance_tags
  })
}

resource "aws_lambda_permission" "wake_up_call_permission" {
  statement_id  = "AllowExecutionFromCloudWatchWakeUp-${random_id.suffix.hex}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.slumber_manager.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.wake_up_call_trigger.arn
}

resource "random_id" "suffix" {
  byte_length = 4
}

data "aws_caller_identity" "current" {}
