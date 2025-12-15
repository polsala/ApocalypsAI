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

# EC2 Instance (The Echo Chamber itself)
resource "aws_instance" "echo_chamber" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = merge(
    var.tags,
    {
      Name        = "TemporalEchoChamber-${random_id.suffix.hex}"
      ManagedBy   = "ApocalypsAI"
      Termination = "Scheduled"
    }
  )

  # Optional: User data to log a startup message
  user_data = <<-EOF
#!/bin/bash
echo "Temporal Echo Chamber instance ${self.id} started at $(date). Scheduled for termination in ${var.duration_minutes} minutes." | tee /var/log/echo_chamber_startup.log
EOF
}

# Random ID for unique naming
resource "random_id" "suffix" {
  byte_length = 4
}

# IAM Role for Lambda function to terminate EC2
resource "aws_iam_role" "lambda_exec_role" {
  name               = "temporal-echo-chamber-lambda-role-${random_id.suffix.hex}"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ],
  })

  tags = var.tags
}

resource "aws_iam_policy" "instance_terminator_policy" {
  name        = "temporal-echo-chamber-terminator-policy-${random_id.suffix.hex}"
  description = "Allows Lambda to terminate specific EC2 instances"
  policy      = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Action   = [
          "ec2:TerminateInstances",
          "ec2:DescribeInstances"
        ]
        Effect   = "Allow"
        Resource = [
          aws_instance.echo_chamber.arn
        ]
      },
      {
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.instance_terminator_policy.arn
}

# Lambda Function to terminate the EC2 instance
resource "aws_lambda_function" "terminator_lambda" {
  function_name    = "temporal-echo-chamber-terminator-${random_id.suffix.hex}"
  handler          = "index.lambda_handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_exec_role.arn
  timeout          = 30
  memory_size      = 128

  # Inline Python code for the Lambda function
  # This ensures the module is self-contained without external file dependencies.
  filename = "lambda_function_payload.zip"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      INSTANCE_ID = aws_instance.echo_chamber.id
      AWS_REGION  = var.aws_region
    }
  }

  tags = var.tags
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "lambda_function_payload.zip"
  source {
    content  = <<-EOF
import os
import boto3
import json

def lambda_handler(event, context):
    instance_id = os.environ.get('INSTANCE_ID')
    region = os.environ.get('AWS_REGION')

    if not instance_id or not region:
        print("Error: INSTANCE_ID or AWS_REGION environment variable not set.")
        return {
            'statusCode': 400,
            'body': json.dumps('Missing environment variables')
        }

    ec2 = boto3.client('ec2', region_name=region)

    try:
        response = ec2.terminate_instances(InstanceIds=[instance_id])
        print(f"Successfully initiated termination for instance {instance_id}. Response: {response}")
        return {
            'statusCode': 200,
            'body': json.dumps(f'Instance {instance_id} termination initiated.')
        }
    except Exception as e:
        print(f"Error terminating instance {instance_id}: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error terminating instance {instance_id}: {str(e)}')
        }
EOF
    filename = "index.py"
  }
}

# CloudWatch Event Rule to trigger Lambda for termination
resource "aws_cloudwatch_event_rule" "termination_schedule" {
  name                = "temporal-echo-chamber-termination-${random_id.suffix.hex}"
  description         = "Triggers Lambda to terminate EC2 instance after ${var.duration_minutes} minutes."
  schedule_expression = "cron(0/${var.duration_minutes} * ? * * *)" # Triggers every N minutes

  tags = var.tags
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.termination_schedule.name
  target_id = "InvokeLambdaForTermination"
  arn       = aws_lambda_function.terminator_lambda.arn
}

# Permission for CloudWatch Events to invoke Lambda
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.terminator_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.termination_schedule.arn
}
