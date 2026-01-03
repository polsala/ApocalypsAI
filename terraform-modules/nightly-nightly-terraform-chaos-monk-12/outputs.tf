# Chaos Monkey Outputs

output "chaos_status" {
  description = "Whether chaos engineering is enabled"
  value       = var.chaos_enabled
  sensitive   = false
}

output "chaos_log_group" {
  description = "CloudWatch log group for chaos events"
  value       = var.chaos_enabled ? "/aws/chaos-monkey/${terraform.workspace}" : "disabled"
  sensitive   = false
}

output "chaos_schedule" {
  description = "Scheduled chaos execution timing"
  value       = "Next chaos run in ${var.chaos_interval_hours} hours"
  sensitive   = false
}

output "chaos_resources_targeted" {
  description = "Resource types targeted for chaos"
  value       = var.target_resource_types
  sensitive   = false
}

output "chaos_exclusions" {
  description = "Resources excluded from chaos"
  value       = var.excluded_resources
  sensitive   = false
}

output "chaos_dry_run_mode" {
  description = "Whether chaos is running in dry-run mode"
  value       = var.dry_run
  sensitive   = false
}

output "chaos_metrics_enabled" {
  description = "Whether CloudWatch metrics are enabled"
  value       = var.enable_chaos_metrics
  sensitive   = false
}

output "chaos_notification_topic" {
  description = "SNS topic for chaos notifications"
  value       = var.chaos_notification_topic != "" ? var.chaos_notification_topic : "none"
  sensitive   = false
}

output "chaos_retention_days" {
  description = "Log retention period for chaos events"
  value       = var.chaos_retention_days
  sensitive   = false
}

output "chaos_execution_policy" {
  description = "IAM policy for chaos execution"
  value       = var.chaos_enabled ? "chaos-monkey-policy-${terraform.workspace}" : "none"
  sensitive   = false
}

output "chaos_region" {
  description = "AWS region for chaos operations"
  value       = var.aws_region
  sensitive   = false
}
