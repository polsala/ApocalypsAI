# Example: Basic Chaos Monkey Configuration

# Configure providers
provider "aws" {
  region = "us-west-2"
}

# Include the chaos monkey module
module "chaos_monkey" {
  source = "../.."
  
  # Enable chaos monkey
  enabled = true
  
  # 10% chance of destroying a resource during each apply
  destruction_probability = 0.1
  
  # Only run chaos during business hours (UTC)
  chaos_window_start = "09:00"
  chaos_window_end   = "17:00"
  
  # Exclude critical resources from chaos
  excluded_resources = [
    "production-database",
    "backup-storage",
    "load-balancer"
  ]
  
  # Run in safe mode for testing
  safe_mode = true
  
  # Set log level to INFO
  log_level = "INFO"
  
  # AWS region
  aws_region = "us-west-2"
}

# Output the chaos monkey status
output "chaos_status" {
  value = {
    enabled           = module.chaos_monkey.chaos_enabled
    window_active     = module.chaos_monkey.chaos_window_active
    should_perform    = module.chaos_monkey.should_perform_chaos
    resources_found   = module.chaos_monkey.resources_discovered
    safe_mode         = module.chaos_monkey.safe_mode
  }
}
