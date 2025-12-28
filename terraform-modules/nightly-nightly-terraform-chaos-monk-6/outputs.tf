# Lambda function outputs
output "chaos_lambda_arn" {
  description = "ARN of the Chaos Monkey Lambda function"
  value       = aws_lambda_function.chaos_monkey.arn
  sensitive   = false
}

output "chaos_lambda_name" {
  description = "Name of the Chaos Monkey Lambda function"
  value       = aws_lambda_function.chaos_monkey.function_name
  sensitive   = false
}

# SNS topic outputs
output "chaos_sns_topic_arn" {
  description = "ARN of the Chaos Monkey SNS topic"
  value       = aws_sns_topic.chaos_notifications.arn
  sensitive   = false
}

output "chaos_sns_topic_name" {
  description = "Name of the Chaos Monkey SNS topic"
  value       = aws_sns_topic.chaos_notifications.name
  sensitive   = false
}

# CloudWatch Event Rule outputs
output "chaos_schedule_rule" {
  description = "CloudWatch Event Rule for Chaos Monkey schedule"
  value       = var.enabled ? aws_cloudwatch_event_rule.chaos_schedule[0].name : "disabled"
  sensitive   = false
}

output "chaos_schedule_expression" {
  description = "Cron expression for Chaos Monkey schedule"
  value       = var.chaos_schedule
  sensitive   = false
}

# CloudWatch Dashboard outputs
output "chaos_dashboard_name" {
  description = "Name of the Chaos Monkey CloudWatch dashboard"
  value       = var.enabled ? aws_cloudwatch_dashboard.chaos_dashboard[0].dashboard_name : "disabled"
  sensitive   = false
}

output "chaos_dashboard_url" {
  description = "URL of the Chaos Monkey CloudWatch dashboard"
  value       = var.enabled ? "https://${var.region}.console.aws.amazon.com/cloudwatch/home?region=${var.region}#dashboards:name=${aws_cloudwatch_dashboard.chaos_dashboard[0].dashboard_name}" : "disabled"
  sensitive   = false
}

# Configuration outputs
output "chaos_intensity" {
  description = "Chaos intensity percentage"
  value       = var.chaos_intensity
  sensitive   = false
}

output "chaos_target_resources" {
  description = "List of target resource types"
  value       = var.target_resources
  sensitive   = false
}

output "chaos_safe_mode" {
  description = "Whether safe mode is enabled"
  value       = var.safe_mode
  sensitive   = false
}

output "chaos_excluded_tags" {
  description = "List of excluded tag values"
  value       = var.excluded_tags
  sensitive   = false
}

# Status outputs
output "chaos_enabled" {
  description = "Whether Chaos Monkey is enabled"
  value       = var.enabled
  sensitive   = false
}

output "chaos_log_retention" {
  description = "CloudWatch log retention days"
  value       = var.log_retention_days
  sensitive   = false
}

output "chaos_notifications_enabled" {
  description = "Whether SNS notifications are enabled"
  value       = var.enable_notifications
  sensitive   = false
}

output "chaos_metrics_enabled" {
  description = "Whether CloudWatch metrics are enabled"
  value       = var.enable_metrics
  sensitive   = false
}

output "chaos_alarm_enabled" {
  description = "Whether CloudWatch alarm is enabled"
  value       = var.enable_alarm
  sensitive   = false
}

# Resource counts (for monitoring)
output "total_resources_targeted" {
  description = "Total number of resource types being targeted"
  value       = length(var.target_resources)
  sensitive   = false
}

output "excluded_tags_count" {
  description = "Number of excluded tag values"
  value       = length(var.excluded_tags)
  sensitive   = false
}

output "notification_emails_count" {
  description = "Number of notification email addresses configured"
  value       = length(var.notification_emails)
  sensitive   = false
}

# Security outputs
output "chaos_iam_role_arn" {
  description = "ARN of the IAM role used by Chaos Monkey Lambda"
  value       = aws_iam_role.chaos_lambda_role.arn
  sensitive   = false
}

output "chaos_iam_policy_arn" {
  description = "ARN of the IAM policy used by Chaos Monkey Lambda"
  value       = aws_iam_policy.chaos_lambda_policy.arn
  sensitive   = false
}

# Advanced configuration outputs
output "chaos_window" {
  description = "Chaos execution time window"
  value       = "${var.chaos_window_start}:00 - ${var.chaos_window_end}:00"
  sensitive   = false
}

output "chaos_max_terminations" {
  description = "Maximum terminations per run"
  value       = var.max_terminations_per_run
  sensitive   = false
}

output "chaos_min_time_between_runs" {
  description = "Minimum hours between chaos runs"
  value       = var.min_time_between_runs
  sensitive   = false
}

output "chaos_duration_limit" {
  description = "Maximum chaos execution duration in minutes"
  value       = var.chaos_duration_minutes
  sensitive   = false
}

# Tags outputs
output "chaos_tags" {
  description = "Tags applied to chaos-related resources"
  value       = var.chaos_tags
  sensitive   = false
}

output "excluded_resource_ids_count" {
  description = "Number of specifically excluded resource IDs"
  value       = length(var.excluded_resource_ids)
  sensitive   = false
}

# Dry run status
output "chaos_dry_run_only" {
  description = "Whether only dry runs are performed"
  value       = var.dry_run_only
  sensitive   = false
}
