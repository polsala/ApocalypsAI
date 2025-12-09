# Output the chaos schedule
output "chaos_schedule" {
  description = "The cron schedule for chaos operations"
  value       = var.chaos_schedule
  sensitive   = false
}

# Output resource TTL
output "resource_ttl" {
  description = "Time to live for created chaos resources"
  value       = var.resource_ttl
  sensitive   = false
}

# Output maximum resources
output "max_resources" {
  description = "Maximum number of chaos resources"
  value       = var.max_resources
  sensitive   = false
}

# Output enabled providers
output "providers" {
  description = "Cloud providers enabled for chaos testing"
  value       = var.providers
  sensitive   = false
}

# Output chaos status
output "chaos_enabled" {
  description = "Whether chaos operations are enabled"
  value       = var.enable_chaos
  sensitive   = false
}

# Output resource types
output "resource_types" {
  description = "Types of resources created for chaos testing"
  value       = var.resource_types
  sensitive   = false
}
