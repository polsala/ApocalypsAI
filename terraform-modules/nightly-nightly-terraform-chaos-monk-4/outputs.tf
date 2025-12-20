# Basic Configuration Outputs
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

output "chaos_duration" {
  description = "Duration of chaos events in minutes"
  value       = var.chaos_duration
}

output "dry_run_mode" {
  description = "Whether dry run mode is enabled"
  value       = var.dry_run
}

output "verbose_logging" {
  description = "Whether verbose logging is enabled"
  value       = var.verbose_logging
}

# Safety Configuration Outputs
output "minimum_instance_count" {
  description = "Minimum number of instances to keep running"
  value       = var.minimum_instance_count
}

output "circuit_breaker_threshold" {
  description = "Circuit breaker failure threshold"
  value       = var.circuit_breaker_threshold
}

output "maintenance_windows" {
  description = "Maintenance windows when chaos is disabled"
  value       = var.maintenance_windows
}

# Resource Counts
output "target_instance_count" {
  description = "Number of target instances"
  value       = length(var.target_instances)
}

output "target_service_count" {
  description = "Number of target services"
  value       = length(var.target_services)
}

output "target_database_count" {
  description = "Number of target databases"
  value       = length(var.target_databases)
}

# Cloud Provider Outputs
output "cloud_provider" {
  description = "Cloud provider being used"
  value       = var.cloud_provider
}

output "aws_region" {
  description = "AWS region for resources"
  value       = var.aws_region
  sensitive   = true
}

output "azure_location" {
  description = "Azure location for resources"
  value       = var.azure_location
  sensitive   = true
}

output "gcp_project" {
  description = "GCP project ID"
  value       = var.gcp_project
  sensitive   = true
}

output "gcp_zone" {
  description = "GCP zone for resources"
  value       = var.gcp_zone
  sensitive   = true
}

# Monitoring and Logging Outputs
output "log_group_name" {
  description = "CloudWatch Log Group for chaos events"
  value       = aws_cloudwatch_log_group.chaos_events.name
}

output "log_stream_name" {
  description = "CloudWatch Log Stream for chaos events"
  value       = aws_cloudwatch_log_stream.chaos_events_stream.name
}

output "lambda_function_arn" {
  description = "ARN of the chaos logger Lambda function"
  value       = aws_lambda_function.chaos_logger.arn
}

output "lambda_function_name" {
  description = "Name of the chaos logger Lambda function"
  value       = aws_lambda_function.chaos_logger.function_name
}

# EventBridge Outputs
output "event_rule_name" {
  description = "Name of the EventBridge rule for chaos scheduling"
  value       = var.enabled ? aws_cloudwatch_event_rule.chaos_schedule[0].name : ""
}

output "event_rule_arn" {
  description = "ARN of the EventBridge rule for chaos scheduling"
  value       = var.enabled ? aws_cloudwatch_event_rule.chaos_schedule[0].arn : ""
}

# Chaos Configuration Outputs
output "chaos_types" {
  description = "Types of chaos that will be performed"
  value       = var.chaos_types
}

output "chaos_probability" {
  description = "Calculated chaos probability based on level"
  value       = var.chaos_probability_override != -1 ? var.chaos_probability_override : {
    gentle  = 1
    medium  = 5
    extreme = 15
  }[var.chaos_level]
}

output "excluded_tags" {
  description = "Tags that exclude resources from chaos"
  value       = var.excluded_tags
}

output "included_tags" {
  description = "Tags that include resources for chaos"
  value       = var.included_tags
}

# Notification Outputs
output "notification_email" {
  description = "Email address for chaos event notifications"
  value       = var.notification_email
  sensitive   = true
}

output "slack_webhook_url" {
  description = "Slack webhook URL for chaos event notifications"
  value       = var.slack_webhook_url
  sensitive   = true
}

# Status Outputs
output "chaos_status" {
  description = "Current status of the chaos monkey"
  value       = {
    enabled           = var.enabled
    dry_run           = var.dry_run
    target_count      = length(var.target_instances) + length(var.target_services) + length(var.target_databases)
    safety_enabled    = var.minimum_instance_count > 0
    notifications_set = var.notification_email != "" || var.slack_webhook_url != ""
  }
}

output "readme_url" {
  description = "URL to the README documentation"
  value       = "https://github.com/polsala/ApocalypsAI/blob/main/terraform-modules/nightly-terraform-chaos-monkey/README.md"
}
