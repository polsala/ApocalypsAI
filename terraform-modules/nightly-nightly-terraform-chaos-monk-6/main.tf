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

# Random number generator for chaos decisions
resource "random_integer" "chaos_seed" {
  min = 1
  max = 100
}

# Lambda function for chaos logic
resource "aws_lambda_function" "chaos_monkey" {
  filename         = data.archive_file.chaos_lambda_zip.output_path
  function_name    = "${var.prefix}-chaos-monkey"
  role             = aws_iam_role.chaos_lambda_role.arn
  handler          = "index.handler"
  source_code_hash = filebase64sha256(data.archive_file.chaos_lambda_zip.output_path)
  runtime          = "python3.9"
  timeout          = 300

  environment {
    variables = {
      CHAOS_INTENSITY    = var.chaos_intensity
      TARGET_RESOURCES = jsonencode(var.target_resources)
      EXCLUDED_TAGS    = jsonencode(var.excluded_tags)
      SAFE_MODE        = var.safe_mode
      REGION           = var.region
    }
  }
}

# Lambda deployment package
data "archive_file" "chaos_lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/chaos_lambda.zip"
  source {
    content = <<-EOF
import json
import boto3
import os
import random
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuration from environment variables
CHAOS_INTENSITY = int(os.environ.get('CHAOS_INTENSITY', 5))
TARGET_RESOURCES = json.loads(os.environ.get('TARGET_RESOURCES', '[]'))
EXCLUDED_TAGS = json.loads(os.environ.get('EXCLUDED_TAGS', '[]'))
SAFE_MODE = os.environ.get('SAFE_MODE', 'true').lower() == 'true'
REGION = os.environ.get('REGION', 'us-east-1')

ec2 = boto3.client('ec2', region_name=REGION)
rds = boto3.client('rds', region_name=REGION)
ecs = boto3.client('ecs', region_name=REGION)


def is_resource_protected(tags):
    """Check if resource has excluded tags"""
    if not tags:
        return False
    
    tag_dict = {tag['Key']: tag['Value'] for tag in tags}
    for excluded_tag in EXCLUDED_TAGS:
        if excluded_tag in tag_dict.values():
            return True
    return False


def get_ec2_instances():
    """Get all EC2 instances"""
    try:
        response = ec2.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] in ['running', 'stopped']:
                    instances.append({
                        'id': instance['InstanceId'],
                        'type': 'aws_instance',
                        'state': instance['State']['Name'],
                        'tags': instance.get('Tags', []),
                        'name': next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'Unknown')
                    })
        return instances
    except Exception as e:
        logger.error(f"Error getting EC2 instances: {e}")
        return []


def get_rds_instances():
    """Get all RDS instances"""
    try:
        response = rds.describe_db_instances()
        instances = []
        for db in response['DBInstances']:
            if db['DBInstanceStatus'] == 'available':
                instances.append({
                    'id': db['DBInstanceIdentifier'],
                    'type': 'aws_rds_instance',
                    'state': db['DBInstanceStatus'],
                    'tags': db.get('TagList', []),
                    'name': db['DBInstanceIdentifier']
                })
        return instances
    except Exception as e:
        logger.error(f"Error getting RDS instances: {e}")
        return []


def get_ecs_services():
    """Get all ECS services"""
    try:
        response = ecs.list_clusters()
        services = []
        for cluster_arn in response['clusterArns']:
            service_response = ecs.list_services(cluster=cluster_arn)
            for service_arn in service_response['serviceArns']:
                service_details = ecs.describe_services(
                    cluster=cluster_arn,
                    services=[service_arn]
                )
                service = service_details['services'][0]
                if service['status'] == 'ACTIVE':
                    services.append({
                        'id': service['serviceName'],
                        'type': 'aws_ecs_service',
                        'state': service['status'],
                        'tags': service.get('tags', []),
                        'name': service['serviceName']
                    })
        return services
    except Exception as e:
        logger.error(f"Error getting ECS services: {e}")
        return []


def terminate_ec2_instance(instance_id):
    """Terminate EC2 instance"""
    try:
        if SAFE_MODE:
            logger.info(f"[SAFE MODE] Would terminate EC2 instance: {instance_id}")
            return True
        else:
            ec2.terminate_instances(InstanceIds=[instance_id])
            logger.info(f"Terminated EC2 instance: {instance_id}")
            return True
    except Exception as e:
        logger.error(f"Error terminating EC2 instance {instance_id}: {e}")
        return False


def delete_rds_instance(instance_id):
    """Delete RDS instance"""
    try:
        if SAFE_MODE:
            logger.info(f"[SAFE MODE] Would delete RDS instance: {instance_id}")
            return True
        else:
            rds.delete_db_instance(
                DBInstanceIdentifier=instance_id,
                SkipFinalSnapshot=True,
                DeleteAutomatedBackups=True
            )
            logger.info(f"Deleted RDS instance: {instance_id}")
            return True
    except Exception as e:
        logger.error(f"Error deleting RDS instance {instance_id}: {e}")
        return False


def update_ecs_service(service_name, cluster_arn):
    """Scale down ECS service"""
    try:
        if SAFE_MODE:
            logger.info(f"[SAFE MODE] Would scale down ECS service: {service_name}")
            return True
        else:
            ecs.update_service(
                cluster=cluster_arn,
                service=service_name,
                desiredCount=0
            )
            logger.info(f"Scaled down ECS service: {service_name}")
            return True
    except Exception as e:
        logger.error(f"Error scaling down ECS service {service_name}: {e}")
        return False


def lambda_handler(event, context):
    """Main Lambda handler"""
    logger.info(f"Chaos Monkey execution started at {datetime.now()}")
    logger.info(f"Configuration: Intensity={CHAOS_INTENSITY}%, SafeMode={SAFE_MODE}")
    
    chaos_events = []
    
    # Get all target resources
    all_resources = []
    
    if 'aws_instance' in TARGET_RESOURCES:
        all_resources.extend(get_ec2_instances())
    
    if 'aws_rds_instance' in TARGET_RESOURCES:
        all_resources.extend(get_rds_instances())
    
    if 'aws_ecs_service' in TARGET_RESOURCES:
        all_resources.extend(get_ecs_services())
    
    # Filter out protected resources
    unprotected_resources = [r for r in all_resources if not is_resource_protected(r['tags'])]
    
    logger.info(f"Found {len(all_resources)} total resources, {len(unprotected_resources)} unprotected")
    
    # Calculate how many resources to terminate
    num_to_terminate = max(1, int(len(unprotected_resources) * CHAOS_INTENSITY / 100))
    
    # Randomly select resources to terminate
    selected_resources = random.sample(unprotected_resources, min(num_to_terminate, len(unprotected_resources)))
    
    logger.info(f"Selected {len(selected_resources)} resources for termination")
    
    # Execute chaos
    for resource in selected_resources:
        event = {
            'timestamp': datetime.now().isoformat(),
            'resource_id': resource['id'],
            'resource_type': resource['type'],
            'resource_name': resource['name'],
            'action': 'terminate'
        }
        
        success = False
        if resource['type'] == 'aws_instance':
            success = terminate_ec2_instance(resource['id'])
        elif resource['type'] == 'aws_rds_instance':
            success = delete_rds_instance(resource['id'])
        elif resource['type'] == 'aws_ecs_service':
            # Need to find cluster ARN for ECS service
            cluster_arn = next((s['clusterArn'] for s in ecs.describe_services(
                cluster='default',
                services=[resource['id']]
            )['services'] if s['serviceName'] == resource['id']), None)
            if cluster_arn:
                success = update_ecs_service(resource['id'], cluster_arn)
        
        event['success'] = success
        chaos_events.append(event)
        
        if success:
            logger.info(f"Successfully executed chaos on {resource['type']}: {resource['id']}")
        else:
            logger.error(f"Failed to execute chaos on {resource['type']}: {resource['id']}")
    
    # Generate chaos report
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_resources': len(all_resources),
        'unprotected_resources': len(unprotected_resources),
        'selected_for_termination': len(selected_resources),
        'successful_terminations': sum(1 for e in chaos_events if e['success']),
        'failed_terminations': sum(1 for e in chaos_events if not e['success']),
        'chaos_events': chaos_events
    }
    
    logger.info(f"Chaos Monkey execution completed: {json.dumps(report, indent=2)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps(report, indent=2)
    }
    EOF
    filename = "index.py"
  }
}

# IAM role for Lambda
resource "aws_iam_role" "chaos_lambda_role" {
  name = "${var.prefix}-chaos-lambda-role"

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
  name        = "${var.prefix}-chaos-lambda-policy"
  description = "Policy for Chaos Monkey Lambda function"
  policy      = jsonencode({
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
          "ecs:ListClusters",
          "ecs:ListServices",
          "ecs:DescribeServices",
          "ecs:UpdateService"
        ]
        Resource = "*"
      }
    ]
  })
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "chaos_lambda_policy_attachment" {
  role       = aws_iam_role.chaos_lambda_role.name
  policy_arn = aws_iam_policy.chaos_lambda_policy.arn
}

# CloudWatch Event Rule for scheduling
resource "aws_cloudwatch_event_rule" "chaos_schedule" {
  count  = var.enabled ? 1 : 0
  name   = "${var.prefix}-chaos-schedule"
  schedule_expression = var.chaos_schedule
  description = "Schedule for Chaos Monkey execution"
}

# CloudWatch Event Target
resource "aws_cloudwatch_event_target" "chaos_target" {
  count = var.enabled ? 1 : 0
  rule      = aws_cloudwatch_event_rule.chaos_schedule[0].name
  target_id = "ChaosMonkeyTarget"
  arn       = aws_lambda_function.chaos_monkey.arn
}

# Lambda permission for CloudWatch Events
resource "aws_lambda_permission" "allow_cloudwatch" {
  count        = var.enabled ? 1 : 0
  statement_id = "AllowExecutionFromCloudWatch"
  action       = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chaos_monkey.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.chaos_schedule[0].arn
}

# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "chaos_lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.chaos_monkey.function_name}"
  retention_in_days = var.log_retention_days
}

# SNS Topic for chaos notifications
resource "aws_sns_topic" "chaos_notifications" {
  name = "${var.prefix}-chaos-notifications"
}

# SNS Topic Policy
resource "aws_sns_topic_policy" "chaos_notifications_policy" {
  arn = aws_sns_topic.chaos_notifications.arn
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = { "Service" = "lambda.amazonaws.com" }
        Action = "SNS:Publish"
        Resource = aws_sns_topic.chaos_notifications.arn
      }
    ]
  })
}

# Lambda environment variables for SNS
resource "aws_lambda_function" "chaos_monkey" {
  # ... existing configuration ...
  
  environment {
    variables = {
      CHAOS_INTENSITY    = var.chaos_intensity
      TARGET_RESOURCES = jsonencode(var.target_resources)
      EXCLUDED_TAGS    = jsonencode(var.excluded_tags)
      SAFE_MODE        = var.safe_mode
      REGION           = var.region
      SNS_TOPIC_ARN    = aws_sns_topic.chaos_notifications.arn
    }
  }
  
  # ... rest of configuration ...
}

# Lambda permission for SNS
resource "aws_lambda_permission" "allow_sns_publish" {
  statement_id = "AllowSNSPublish"
  action       = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chaos_monkey.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.chaos_notifications.arn
}

# CloudWatch Alarm for failed chaos executions
resource "aws_cloudwatch_metric_alarm" "chaos_failures" {
  count              = var.enabled ? 1 : 0
  alarm_name          = "${var.prefix}-chaos-failures"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = "0"
  alarm_description   = "This metric monitors failed chaos executions"
  alarm_actions       = [aws_sns_topic.chaos_notifications.arn]
  dimensions = {
    FunctionName = aws_lambda_function.chaos_monkey.function_name
  }
}

# CloudWatch Dashboard for chaos metrics
resource "aws_cloudwatch_dashboard" "chaos_dashboard" {
  count = var.enabled ? 1 : 0
  dashboard_name = "${var.prefix}-chaos-dashboard"
  
  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["AWS/Lambda", "Invocations", "FunctionName", aws_lambda_function.chaos_monkey.function_name],
            ["AWS/Lambda", "Errors", "FunctionName", aws_lambda_function.chaos_monkey.function_name]
          ]
          period = 300
          stat   = "Sum"
          region = var.region
          title  = "Chaos Monkey Execution Metrics"
        }
      },
      {
        type   = "log"
        x      = 0
        y      = 6
        width  = 24
        height = 6
        properties = {
          query = "SOURCE '${aws_cloudwatch_log_group.chaos_lambda_logs.name}'
| fields @timestamp, @message
| sort @timestamp desc
| limit 100"
          region = var.region
          title  = "Chaos Monkey Logs"
        }
      }
    ]
  })
}

# Outputs
output "chaos_lambda_arn" {
  description = "ARN of the Chaos Monkey Lambda function"
  value       = aws_lambda_function.chaos_monkey.arn
}

output "chaos_sns_topic_arn" {
  description = "ARN of the Chaos Monkey SNS topic"
  value       = aws_sns_topic.chaos_notifications.arn
}

output "chaos_schedule_rule" {
  description = "CloudWatch Event Rule for Chaos Monkey schedule"
  value       = var.enabled ? aws_cloudwatch_event_rule.chaos_schedule[0].name : "disabled"
}

output "chaos_dashboard_url" {
  description = "URL of the Chaos Monkey CloudWatch dashboard"
  value       = var.enabled ? "https://${var.region}.console.aws.amazon.com/cloudwatch/home?region=${var.region}#dashboards:name=${aws_cloudwatch_dashboard.chaos_dashboard[0].dashboard_name}" : "disabled"
}
