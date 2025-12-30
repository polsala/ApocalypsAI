# Basic status outputs
output "chaos_enabled" {
  description = "Whether chaos monkey is enabled"
  value       = var.enabled
  sensitive   = false
}

output "chaos_window_active" {
  description = "Whether current time is within chaos window"
  value       = local.chaos_window_active
  sensitive   = false
}

output "should_perform_chaos" {
  description = "Whether chaos should be performed this run"
  value       = local.should_chaos
  sensitive   = false
}

output "resources_discovered" {
  description = "Number of resources discovered for potential chaos"
  value       = var.enabled ? length(data.aws_instances.all[0].ids) : 0
  sensitive   = false
}

output "safe_mode" {
  description = "Whether running in safe mode (no actual destruction)"
  value       = var.safe_mode
  sensitive   = false
}

# Configuration outputs
output "destruction_probability" {
  description = "Current destruction probability setting"
  value       = var.destruction_probability
  sensitive   = false
}

output "chaos_window" {
  description = "Current chaos window configuration"
  value = {
    start = var.chaos_window_start
    end   = var.chaos_window_end
  }
  sensitive   = false
}

output "excluded_resources_count" {
  description = "Number of resources excluded from chaos"
  value       = length(var.excluded_resources)
  sensitive   = false
}

# Provider-specific outputs
output "aws_region" {
  description = "AWS region being monitored"
  value       = var.aws_region
  sensitive   = false
}

output "gcp_project" {
  description = "GCP project being monitored"
  value       = var.gcp_project
  sensitive   = false
}

output "azure_subscription_id" {
  description = "Azure subscription being monitored"
  value       = var.azure_subscription_id
  sensitive   = false
}

# Advanced configuration outputs
output "max_resources_per_run" {
  description = "Maximum resources that can be destroyed per run"
  value       = var.max_resources_per_run
  sensitive   = false
}

output "chaos_cooldown_minutes" {
  description = "Chaos cooldown period in minutes"
  value       = var.chaos_cooldown_minutes
  sensitive   = false
}

# Debug outputs (only shown in debug mode)
output "debug_info" {
  description = "Debug information (only shown when log_level is DEBUG)"
  value = var.log_level == "DEBUG" ? {
    current_timestamp = timestamp()
    current_time      = local.current_time
    destruction_threshold = local.destruction_threshold
    chaos_seed        = var.chaos_seed.result
    resource_types    = var.resource_types
  } : null
  sensitive   = false
}
