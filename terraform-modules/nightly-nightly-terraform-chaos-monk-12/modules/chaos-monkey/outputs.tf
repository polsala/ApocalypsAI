# Chaos Monkey Module Outputs

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
