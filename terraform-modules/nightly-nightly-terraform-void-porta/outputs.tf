# Basic portal information
output "portal_id" {
  description = "Unique identifier for the void portal"
  value       = random_id.portal_id.hex
}

output "portal_name" {
  description = "Whimsical name for the void portal"
  value       = "${var.portal_name}-${random_pet.void_portal.id}-${random_string.portal_name.result}"
}

# Resource tracking information
output "tracked_resources" {
  description = "Inventory of tracked resources across providers"
  value       = local.resource_inventory
}

output "tracked_providers" {
  description = "List of providers being tracked"
  value       = var.providers
}

# Cleanup configuration
output "cleanup_schedule" {
  description = "Cron expression for automatic resource cleanup"
  value       = local.cleanup_cron
}

output "auto_cleanup_enabled" {
  description = "Whether automatic cleanup is enabled"
  value       = var.auto_cleanup_days > 0
}

# Portal status and metadata
output "portal_status" {
  description = "Current status of the void portal"
  value = {
    active          = true
    providers_count = length(var.providers)
    tracking_enabled = var.track_resources
    auto_cleanup    = var.auto_cleanup_days > 0 ? "enabled" : "disabled"
    portal_type     = "whimsical"
    created_at      = timestamp()
  }
}

output "portal_metadata" {
  description = "Additional metadata about the portal"
  value = {
    module_version = "1.0.0"
    terraform_version = terraform.version
    supported_providers = var.providers
    debug_enabled = var.enable_debug
  }
}

# Conditional outputs based on configuration
output "resource_tracker_id" {
  description = "ID of the resource tracker (only if tracking is enabled)"
  value       = var.track_resources ? null_resource.resource_tracker[0].id : null
  sensitive   = true
}

output "cleanup_hour" {
  description = "Hour when cleanup runs (only if enabled)"
  value       = var.auto_cleanup_days > 0 ? random_integer.cleanup_hour[0].result : null
}

output "cleanup_minute" {
  description = "Minute when cleanup runs (only if enabled)"
  value       = var.auto_cleanup_days > 0 ? random_integer.cleanup_minute[0].result : null
}
