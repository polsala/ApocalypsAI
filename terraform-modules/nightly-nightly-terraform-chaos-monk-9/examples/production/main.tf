# Example: Production Chaos Monkey Configuration

# Configure providers
provider "aws" {
  region = "us-east-1"
}

# Include the chaos monkey module
module "chaos_monkey" {
  source = "../.."
  
  # Enable chaos monkey
  enabled = true
  
  # Very low probability for production
  destruction_probability = 0.01
  
  # Run chaos only during off-peak hours
  chaos_window_start = "02:00"
  chaos_window_end   = "04:00"
  
  # Exclude all critical production resources
  excluded_resources = [
    "production-db",
    "production-rds",
    "elb-production",
    "monitoring-system",
    "backup-bucket",
    "ci-cd-pipeline",
    "auth-service"
  ]
  
  # Disable safe mode for real chaos
  safe_mode = false
  
  # Set log level to WARN to reduce noise
  log_level = "WARN"
  
  # AWS region
  aws_region = "us-east-1"
  
  # Limit to only 1 resource per run
  max_resources_per_run = 1
  
  # 2-hour cooldown between chaos events
  chaos_cooldown_minutes = 120
}

# Output the chaos monkey status
output "production_chaos_status" {
  value = {
    enabled           = module.chaos_monkey.chaos_enabled
    window_active     = module.chaos_monkey.chaos_window_active
    should_perform    = module.chaos_monkey.should_perform_chaos
    resources_found   = module.chaos_monkey.resources_discovered
    safe_mode         = module.chaos_monkey.safe_mode
    probability       = "1%"
    window_hours      = "02:00-04:00 UTC"
  }
}
