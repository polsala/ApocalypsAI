# Chaos Status
output "chaos_status" {
  description = "Current status of the chaos garden"
  value       = local.chaos_enabled ? "Chaos Garden is ACTIVE (Level ${var.chaos_level})" : "Chaos Garden is DISABLED"
}

# Chaos Event Details
output "chaos_event" {
  description = "Type of chaos event that will be triggered"
  value       = local.chaos_enabled ? local.chaos_events[random_integer.chaos_event_type[0].result] : "No event"
  sensitive   = true
}

# Chaos Duration
output "chaos_duration_seconds" {
  description = "Duration of the chaos event in seconds"
  value       = local.chaos_enabled ? random_integer.chaos_duration[0].result : 0
  sensitive   = true
}

# Chaos Severity
output "chaos_severity" {
  description = "Severity level of the chaos event"
  value       = local.chaos_enabled ? local.chaos_severity[var.chaos_level] : "None"
}

# Protected Resources
output "protected_resources" {
  description = "List of resources protected from chaos events"
  value       = var.protected_resources
}

# Chaos Configuration Summary
output "chaos_summary" {
  description = "Summary of chaos configuration"
  value = {
    enabled           = var.enabled
    chaos_level       = var.chaos_level
    protected_count   = length(var.protected_resources)
    schedule          = var.chaos_schedule
    provider          = var.provider_type
  }
}

# Warning Messages
output "warnings" {
  description = "Any warnings related to chaos configuration"
  value = local.chaos_enabled && (var.chaos_level > 7) ? [
    "High chaos level detected - ensure proper monitoring is in place",
    "Consider using protected_resources for critical infrastructure"
  ] : local.chaos_enabled ? [
    "Chaos Garden is enabled - monitor your resources closely"
  ] : []
}

# Example Usage
output "example_usage" {
  description = "Example of how to use this module"
  value = <<-EOT
    module "chaos_garden" {
      source = "./modules/chaos-garden"
      
      chaos_level = 3
      protected_resources = ["production-db"]
      enabled = true
    }
  EOT
}
