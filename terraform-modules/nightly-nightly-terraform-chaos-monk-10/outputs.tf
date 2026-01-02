# Chaos monkey status report
output "chaos_status" {
  description = "Current status of the chaos monkey"
  value = {
    enabled                    = var.enabled
    environment               = var.environment
    destruction_probability   = var.destruction_probability
    max_destructions_per_run  = var.max_destructions_per_run
    chaos_schedule            = var.chaos_schedule
    dry_run                   = var.dry_run
    backup_before_destruction = var.backup_before_destruction
    notification_webhook      = var.notification_webhook != "" ? "configured" : "not configured"
    min_resource_age_hours    = var.min_resource_age_hours
    chaos_duration_minutes    = var.chaos_duration_minutes
    excluded_regions_count    = length(var.excluded_regions)
    chaos_tags_count          = length(var.chaos_tags)
  }
}

# Safety warnings
output "safety_warnings" {
  description = "Safety warnings and recommendations"
  value = [
    var.enabled ? "⚠️ CHAOS MONKEY IS ENABLED - RESOURCES MAY BE DESTROYED" : "✅ Chaos monkey is disabled",
    var.environment == "production" ? "🚨 WARNING: You are in production environment" : "",
    var.dry_run ? "📝 Dry run mode is enabled - no actual destruction will occur" : "",
    var.backup_before_destruction ? "💾 Backup before destruction is enabled" : "⚠️ Backup before destruction is disabled",
    length(var.target_resources) == 0 ? "⚠️ No target resources specified" : "",
    var.destruction_probability > 0.2 ? "🚨 High destruction probability detected" : "",
    var.max_destructions_per_run > 5 ? "🚨 High maximum destructions per run detected" : ""
  ]
  
  # Only show warnings when relevant
  sensitive = var.enabled || var.environment == "production"
}

# Resource inventory
output "eligible_resources" {
  description = "Resources that are eligible for chaos operations"
  value = local.eligible_resources
  
  # Only show when chaos is enabled and not in production
  sensitive = !var.enabled || var.environment == "production"
}

# Chaos configuration summary
output "configuration_summary" {
  description = "Summary of chaos monkey configuration"
  value = {
    chaos_enabled             = var.enabled
    target_resource_types     = var.target_resources
    excluded_resource_count   = length(var.excluded_resources)
    excluded_regions          = var.excluded_regions
    chaos_tags                = var.chaos_tags
    schedule                  = var.chaos_schedule
    duration_limit            = "${var.chaos_duration_minutes} minutes"
    age_filter                = "${var.min_resource_age_hours} hours"
  }
}

# Emergency disable instructions
output "emergency_disable" {
  description = "Instructions to disable chaos monkey in emergency"
  value = "To disable chaos monkey immediately, set 'enabled = false' in your Terraform variables and run 'terraform apply'."
  
  sensitive = var.enabled
}

# Last chaos event
output "last_chaos_event" {
  description = "Timestamp of the last chaos event"
  value       = local.chaos_timestamp
  
  # Only show when chaos has been active
  sensitive = !var.enabled
}
