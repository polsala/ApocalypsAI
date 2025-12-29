# Whether the chaos monkey is enabled
output "chaos_monkey_enabled" {
  description = "Whether the chaos monkey is enabled"
  value       = var.enabled
}

# Cron schedule for chaos execution
output "chaos_schedule" {
  description = "Cron schedule for chaos execution"
  value       = var.chaos_schedule
}

# Whether safe mode is enabled
output "safe_mode" {
  description = "Whether safe mode is enabled"
  value       = var.safe_mode
}

# Lambda function ARN
output "lambda_function_arn" {
  description = "ARN of the chaos monkey Lambda function"
  value       = var.enabled ? aws_lambda_function.chaos_monkey[0].arn : ""
  sensitive   = true
}

# Lambda function name
output "lambda_function_name" {
  description = "Name of the chaos monkey Lambda function"
  value       = var.enabled ? aws_lambda_function.chaos_monkey[0].function_name : ""
}

# CloudWatch Event Rule ARN
output "event_rule_arn" {
  description = "ARN of the CloudWatch Event Rule"
  value       = var.enabled ? aws_cloudwatch_event_rule.chaos_schedule[0].arn : ""
}

# CloudWatch Event Rule name
output "event_rule_name" {
  description = "Name of the CloudWatch Event Rule"
  value       = var.enabled ? aws_cloudwatch_event_rule.chaos_schedule[0].name : ""
}

# Number of resources that could be targeted
output "target_resource_count" {
  description = "Number of resources that could be targeted"
  value       = length(local.target_ec2_instances)
}

# Destruction probability
output "destruction_probability" {
  description = "Destruction probability configured for the chaos monkey"
  value       = var.destruction_probability
}

# Target resource types
output "target_resource_types" {
  description = "Resource types configured for targeting"
  value       = var.target_resource_types
}

# Maximum resources per run
output "max_resources_per_run" {
  description = "Maximum number of resources to destroy per chaos run"
  value       = var.max_resources_per_run
}

# Excluded resources
output "excluded_resources" {
  description = "Resource IDs excluded from chaos"
  value       = var.excluded_resources
  sensitive   = true
}

# AWS region
output "aws_region" {
  description = "AWS region for chaos operations"
  value       = var.aws_region
}

# Lambda memory size
output "lambda_memory_size" {
  description = "Memory size configured for the Lambda function"
  value       = var.lambda_memory_size
}

# Lambda timeout
output "lambda_timeout" {
  description = "Timeout configured for the Lambda function"
  value       = var.lambda_timeout
}

# Log retention days
output "log_retention_days" {
  description = "CloudWatch log retention days configured"
  value       = var.log_retention_days
}

# Notification email
output "notification_email" {
  description = "Email address configured for notifications"
  value       = var.notification_email
  sensitive   = true
}

# SNS topic ARN
output "sns_topic_arn" {
  description = "SNS topic ARN configured for notifications"
  value       = var.sns_topic_arn
  sensitive   = true
}
