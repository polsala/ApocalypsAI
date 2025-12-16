# ECS Cluster Information
output "chaos_cluster_id" {
  description = "ECS cluster ID for chaos tasks"
  value       = aws_ecs_cluster.chaos_garden.id
  sensitive   = false
}

output "chaos_cluster_arn" {
  description = "ECS cluster ARN for chaos tasks"
  value       = aws_ecs_cluster.chaos_garden.arn
  sensitive   = false
}

# Task Definition Information
output "chaos_task_definition" {
  description = "ARN of the chaos task definition"
  value       = aws_ecs_task_definition.chaos_task.arn
  sensitive   = false
}

output "chaos_task_family" {
  description = "Family name of the chaos task definition"
  value       = aws_ecs_task_definition.chaos_task.family
  sensitive   = false
}

# Service Information
output "chaos_service_name" {
  description = "Name of the ECS service running chaos tasks"
  value       = aws_ecs_service.chaos_service.name
  sensitive   = false
}

output "chaos_service_arn" {
  description = "ARN of the ECS service running chaos tasks"
  value       = aws_ecs_service.chaos_service.arn
  sensitive   = false
}

output "chaos_task_count" {
  description = "Number of chaos tasks running"
  value       = aws_ecs_service.chaos_service.desired_count
  sensitive   = false
}

# Scheduling Information
output "chaos_schedule_rule" {
  description = "CloudWatch Events rule for chaos scheduling"
  value       = aws_cloudwatch_event_rule.chaos_schedule.arn
  sensitive   = false
}

output "chaos_schedule_expression" {
  description = "Schedule expression for chaos runs"
  value       = aws_cloudwatch_event_rule.chaos_schedule.schedule_expression
  sensitive   = false
}

# Monitoring and Logging
output "chaos_log_group" {
  description = "CloudWatch log group for chaos tasks"
  value       = aws_cloudwatch_log_group.chaos_logs.name
  sensitive   = false
}

output "chaos_log_group_arn" {
  description = "CloudWatch log group ARN for chaos tasks"
  value       = aws_cloudwatch_log_group.chaos_logs.arn
  sensitive   = false
}

output "chaos_notifications_topic" {
  description = "SNS topic ARN for chaos notifications"
  value       = aws_sns_topic.chaos_notifications.arn
  sensitive   = false
}

output "chaos_notifications_topic_name" {
  description = "SNS topic name for chaos notifications"
  value       = aws_sns_topic.chaos_notifications.name
  sensitive   = false
}

# IAM Information
output "chaos_task_role_arn" {
  description = "ARN of the IAM role used by chaos tasks"
  value       = aws_iam_role.chaos_task_role.arn
  sensitive   = false
}

output "chaos_execution_role_arn" {
  description = "ARN of the IAM role used for ECS execution"
  value       = aws_iam_role.chaos_execution_role.arn
  sensitive   = false
}

# Resource Names and IDs
output "chaos_garden_name" {
  description = "Generated whimsical chaos garden name"
  value       = local.chaos_garden_id
  sensitive   = false
}

output "chaos_garden_suffix" {
  description = "Random suffix used in chaos garden naming"
  value       = random_id.garden_suffix.hex
  sensitive   = false
}

# Configuration Summary
output "chaos_configuration" {
  description = "Summary of chaos configuration settings"
  value = {
    environment           = var.environment
    chaos_duration        = var.chaos_duration
    whimsy_level          = var.whimsy_level
    chaos_garden_name     = var.chaos_garden_name
    enable_network_chaos  = var.enable_network_chaos
    network_latency_ms    = var.network_latency_ms
    enable_cpu_chaos      = var.enable_cpu_chaos
    cpu_stress_duration   = var.cpu_stress_duration
    enable_random_failures = var.enable_random_failures
    failure_rate          = var.failure_rate
    task_cpu              = var.task_cpu
    task_memory           = var.task_memory
    chaos_task_count      = var.chaos_task_count
  }
  sensitive   = false
}

# Security Groups and Subnets
output "chaos_security_groups" {
  description = "Security groups attached to chaos tasks"
  value       = var.security_group_ids
  sensitive   = false
}

output "chaos_subnets" {
  description = "Subnets used by chaos tasks"
  value       = var.subnet_ids
  sensitive   = false
}

# Alarms and Monitoring
output "chaos_failure_alarm" {
  description = "CloudWatch alarm for chaos failures"
  value       = aws_cloudwatch_metric_alarm.chaos_failures.arn
  sensitive   = false
}

output "chaos_alarm_threshold" {
  description = "CPU utilization threshold for chaos failure alarms"
  value       = var.chaos_alarm_threshold
  sensitive   = false
}

# Container Information
output "chaos_container_image" {
  description = "Docker image used for chaos container"
  value       = var.chaos_container_image
  sensitive   = false
}

# Tags
output "resource_tags" {
  description = "Tags applied to chaos garden resources"
  value = merge(
    {
      Name        = local.chaos_garden_id
      Environment = var.environment
      Purpose     = "chaos-garden"
      WhimsyLevel = var.whimsy_level
    },
    var.additional_tags
  )
  sensitive   = false
}
