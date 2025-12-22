# Outputs for Chaos Monkey module

output "chaos_enabled" {
  description = "Whether chaos mode is enabled"
  value       = var.chaos_enabled
  sensitive   = false
}

output "chaos_probability" {
  description = "The probability setting for chaos execution"
  value       = var.chaos_probability
  sensitive   = false
}

output "target_count" {
  description = "Number of resources targeted for chaos"
  value       = length(local.filtered_targets)
  sensitive   = false
}

output "target_resources" {
  description = "List of resources that could be affected by chaos"
  value       = local.filtered_targets
  sensitive   = false
}

output "dry_run_mode" {
  description = "Whether dry-run mode is enabled"
  value       = var.dry_run
  sensitive   = false
}

output "chaos_metrics" {
  description = "Metrics and statistics about chaos execution"
  value = {
    enabled        = var.chaos_enabled
    probability    = var.chaos_probability
    dry_run        = var.dry_run
    target_count   = length(local.filtered_targets)
    target_resources = local.filtered_targets
    execution_time = timestamp()
    schedule       = var.chaos_schedule
    excluded_count = length(var.excluded_resources)
  }
  sensitive = false
}

output "chaos_schedule" {
  description = "The cron schedule for chaos execution"
  value       = var.chaos_schedule
  sensitive   = false
}

output "excluded_resources" {
  description = "Resources excluded from chaos"
  value       = var.excluded_resources
  sensitive   = false
}

output "safety_warnings" {
  description = "Safety warnings and recommendations"
  value = [
    for warning in [
      var.chaos_enabled && !var.dry_run ? "WARNING: Chaos enabled without dry-run mode" : null,
      var.chaos_probability > 0.2 ? "WARNING: High chaos probability detected" : null,
      length(var.excluded_resources) == 0 ? "RECOMMENDATION: Add critical resources to excluded_resources" : null,
      !var.chaos_enabled ? "INFO: Chaos mode is disabled" : null
    ]
    : warning != null
  ]
  sensitive = false
}

# Conditional outputs based on chaos execution
output "last_chaos_execution" {
  description = "Timestamp of last chaos execution"
  value       = local.chaos_should_occur ? timestamp() : "No chaos execution this cycle"
  sensitive   = false
}

output "chaos_impact_summary" {
  description = "Summary of chaos impact"
  value = {
    resources_targeted = length(local.filtered_targets)
    chaos_occurred     = local.chaos_should_occur
    dry_run_mode       = var.dry_run
    excluded_count     = length(var.excluded_resources)
  }
  sensitive = false
}

# Debug output (only in debug mode)
output "debug_info" {
  description = "Debug information for troubleshooting"
  value = {
    potential_targets = local.potential_targets
    filtered_targets  = local.filtered_targets
    chaos_condition   = local.chaos_should_occur
    random_seed       = random_integer.chaos_selector[0].result
  }
  sensitive = false
  # Only show in debug mode
  depends_on = [var.log_level == "DEBUG" ? random_integer.chaos_selector : null]
}
