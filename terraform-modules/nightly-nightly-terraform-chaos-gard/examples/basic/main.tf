# Basic Chaos Garden Example

module "chaos_garden" {
  source = "../.."
  
  # Enable chaos with moderate level
  chaos_level = 3
  enabled     = true
  
  # Protect critical resources
  protected_resources = [
    "production-database",
    "auth-service",
    "user-api"
  ]
  
  # Optional: Set chaos schedule (daily at 2 AM)
  chaos_schedule = "0 2 * * *"
  
  # Add some tags
  resource_tags = {
    Environment = "staging"
    Team        = "SRE"
    Purpose     = "chaos-testing"
  }
}

# Output the chaos configuration
output "chaos_info" {
  value = {
    status    = module.chaos_garden.chaos_status
    event     = module.chaos_garden.chaos_event
    duration  = module.chaos_garden.chaos_duration_seconds
    severity  = module.chaos_garden.chaos_severity
    protected = module.chaos_garden.protected_resources
  }
}

# Example warning output
output "chaos_warnings" {
  value = module.chaos_garden.warnings
}
