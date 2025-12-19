# Chaos Monkey Module Outputs

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

output "target_resource_types" {
  description = "Resource types targeted for chaos"
  value       = var.target_resource_types
}

output "max_destructions_per_cycle" {
  description = "Maximum destructions per chaos cycle"
  value       = var.max_destructions_per_cycle
}

output "dry_run_mode" {
  description = "Whether dry run mode is enabled"
  value       = var.dry_run
}

output "chaos_lambda_name" {
  description = "Name of the chaos monkey lambda function"
  value       = var.chaos_enabled ? aws_lambda_function.chaos_monkey[0].function_name : ""
}

output "chaos_cloudwatch_rule" {
  description = "CloudWatch Events rule for chaos scheduling"
  value       = var.chaos_enabled ? aws_cloudwatch_event_rule.chaos_schedule[0].arn : ""
}

output "chaos_log_group" {
  description = "CloudWatch log group for chaos monkey logs"
  value       = var.chaos_enabled ? aws_cloudwatch_log_group.chaos_lambda_logs[0].name : ""
}
