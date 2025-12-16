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
  region = var.aws_region
}

# Generate whimsical chaos garden name
locals {
  whimsical_prefix = var.whimsy_level == "high" ? "Whimsical" : var.whimsy_level == "medium" ? "Playful" : "Mild"
  chaos_garden_id  = "${local.whimsical_prefix}${var.chaos_garden_name}-${random_id.garden_suffix.hex}"
}

# Random suffix for unique naming
resource "random_id" "garden_suffix" {
  byte_length = 4
}

# ECS Cluster for chaos tasks
resource "aws_ecs_cluster" "chaos_garden" {
  name = local.chaos_garden_id
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Name        = "${local.chaos_garden_id}-cluster"
    Environment = var.environment
    Purpose     = "chaos-garden"
    WhimsyLevel = var.whimsy_level
  }
}

# IAM role for ECS tasks
resource "aws_iam_role" "chaos_task_role" {
  name = "${local.chaos_garden_id}-task-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
  
  tags = {
    Name        = "${local.chaos_garden_id}-task-role"
    Environment = var.environment
  }
}

# IAM role for ECS execution
resource "aws_iam_role" "chaos_execution_role" {
  name = "${local.chaos_garden_id}-execution-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
  
  tags = {
    Name        = "${local.chaos_garden_id}-execution-role"
    Environment = var.environment
  }
}

# IAM policy for execution role
resource "aws_iam_role_policy" "chaos_execution_policy" {
  name = "${local.chaos_garden_id}-execution-policy"
  role = aws_iam_role.chaos_execution_role.id
  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      }
    ]
  })
}

# CloudWatch log group for chaos tasks
resource "aws_cloudwatch_log_group" "chaos_logs" {
  name              = "/aws/ecs/${local.chaos_garden_id}"
  retention_in_days = var.log_retention_days
  
  tags = {
    Name        = "${local.chaos_garden_id}-logs"
    Environment = var.environment
  }
}

# ECS task definition for chaos
resource "aws_ecs_task_definition" "chaos_task" {
  family                   = "${local.chaos_garden_id}-chaos-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.chaos_execution_role.arn
  task_role_arn            = aws_iam_role.chaos_task_role.arn
  
  container_definitions = jsonencode([
    {
      name  = "chaos-container",
      image = "${var.chaos_container_image}",
      
      essential = true,
      
      portMappings = [
        {
          containerPort = 80,
          protocol      = "tcp"
        }
      ],
      
      environment = [
        {
          name  = "CHAOS_DURATION",
          value = var.chaos_duration
        },
        {
          name  = "ENABLE_NETWORK_CHAOS",
          value = tostring(var.enable_network_chaos)
        },
        {
          name  = "NETWORK_LATENCY_MS",
          value = tostring(var.network_latency_ms)
        },
        {
          name  = "ENABLE_CPU_CHAOS",
          value = tostring(var.enable_cpu_chaos)
        },
        {
          name  = "CPU_STRESS_DURATION",
          value = var.cpu_stress_duration
        },
        {
          name  = "ENABLE_RANDOM_FAILURES",
          value = tostring(var.enable_random_failures)
        },
        {
          name  = "FAILURE_RATE",
          value = tostring(var.failure_rate)
        },
        {
          name  = "WHIMSY_LEVEL",
          value = var.whimsy_level
        }
      ],
      
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = aws_cloudwatch_log_group.chaos_logs.name,
          awslogs-region        = var.aws_region,
          awslogs-stream-prefix = "ecs"
        }
      },
      
      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost/ || exit 1"],
        interval    = 30,
        timeout     = 5,
        retries     = 3,
        startPeriod = 60
      }
    }
  ])
  
  tags = {
    Name        = "${local.chaos_garden_id}-task-definition"
    Environment = var.environment
    WhimsyLevel = var.whimsy_level
  }
}

# ECS service for chaos tasks
resource "aws_ecs_service" "chaos_service" {
  name            = "${local.chaos_garden_id}-chaos-service"
  cluster         = aws_ecs_cluster.chaos_garden.id
  task_definition = aws_ecs_task_definition.chaos_task.arn
  desired_count   = var.chaos_task_count
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = var.security_group_ids
    assign_public_ip = true
  }
  
  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }
  
  tags = {
    Name        = "${local.chaos_garden_id}-chaos-service"
    Environment = var.environment
    WhimsyLevel = var.whimsy_level
  }
}

# CloudWatch Events rule for chaos scheduling
resource "aws_cloudwatch_event_rule" "chaos_schedule" {
  name        = "${local.chaos_garden_id}-chaos-schedule"
  description = "Schedule for chaos garden runs"
  
  # Run chaos every hour for testing
  schedule_expression = "rate(1 hour)"
  
  tags = {
    Name        = "${local.chaos_garden_id}-chaos-schedule"
    Environment = var.environment
  }
}

# CloudWatch Events target for chaos
resource "aws_cloudwatch_event_target" "chaos_target" {
  rule      = aws_cloudwatch_event_rule.chaos_schedule.name
  target_id = "chaos-target"
  arn       = aws_ecs_cluster.chaos_garden.arn
  
  role_arn = aws_iam_role.chaos_execution_role.arn
  
  input = jsonencode({
    taskDefinition = aws_ecs_task_definition.chaos_task.family,
    count          = var.chaos_task_count,
    networkConfiguration = {
      awsvpcConfiguration = {
        subnets          = var.subnet_ids,
        securityGroups   = var.security_group_ids,
        assignPublicIp   = "ENABLED"
      }
    }
  })
}

# IAM policy for CloudWatch Events to ECS
resource "aws_iam_role_policy" "cloudwatch_to_ecs" {
  name = "${local.chaos_garden_id}-cloudwatch-ecs"
  role = aws_iam_role.chaos_execution_role.id
  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ecs:RunTask"
        ],
        Resource = aws_ecs_task_definition.chaos_task.arn
      },
      {
        Effect = "Allow",
        Action = [
          "iam:PassRole"
        ],
        Resource = [
          aws_iam_role.chaos_task_role.arn,
          aws_iam_role.chaos_execution_role.arn
        ]
      }
    ]
  })
}

# SNS topic for chaos notifications
resource "aws_sns_topic" "chaos_notifications" {
  name = "${local.chaos_garden_id}-chaos-notifications"
  
  tags = {
    Name        = "${local.chaos_garden_id}-chaos-notifications"
    Environment = var.environment
  }
}

# CloudWatch alarm for chaos failures
resource "aws_cloudwatch_metric_alarm" "chaos_failures" {
  alarm_name          = "${local.chaos_garden_id}-chaos-failures"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = "120"
  statistic           = "Average"
  threshold           = "90"
  alarm_description   = "This metric monitors ecs cpu utilization"
  alarm_actions       = [aws_sns_topic.chaos_notifications.arn]
  
  dimensions = {
    ServiceName = aws_ecs_service.chaos_service.name
    ClusterName = aws_ecs_cluster.chaos_garden.name
  }
  
  tags = {
    Name        = "${local.chaos_garden_id}-chaos-failures-alarm"
    Environment = var.environment
  }
}

# Output the chaos cluster ID
output "chaos_cluster_id" {
  description = "ECS cluster ID for chaos tasks"
  value       = aws_ecs_cluster.chaos_garden.id
}

# Output the chaos task definition
output "chaos_task_definition" {
  description = "ARN of the chaos task definition"
  value       = aws_ecs_task_definition.chaos_task.arn
}

# Output the chaos schedule rule
output "chaos_schedule_rule" {
  description = "CloudWatch Events rule for chaos scheduling"
  value       = aws_cloudwatch_event_rule.chaos_schedule.arn
}

# Output the SNS topic for notifications
output "chaos_notifications_topic" {
  description = "SNS topic ARN for chaos notifications"
  value       = aws_sns_topic.chaos_notifications.arn
}

# Output the log group name
output "chaos_log_group" {
  description = "CloudWatch log group for chaos tasks"
  value       = aws_cloudwatch_log_group.chaos_logs.name
}
