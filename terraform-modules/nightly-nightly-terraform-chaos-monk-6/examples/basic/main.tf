# Basic Chaos Monkey Example

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Basic Chaos Monkey configuration
module "chaos_monkey" {
  source = "../.."
  
  # Basic configuration
  prefix = "basic-chaos"
  enabled = true
  
  # Chaos settings
  chaos_schedule = "0 2 * * *"  # Daily at 2 AM
  chaos_intensity = 5            # 5% of resources
  safe_mode = true              # Safe mode enabled
  
  # Target resources
  target_resources = [
    "aws_instance",
    "aws_rds_instance"
  ]
  
  # Excluded tags
  excluded_tags = [
    "critical",
    "production-critical",
    "do-not-terminate"
  ]
  
  # Logging
  log_retention_days = 7
  
  # Limits
  max_terminations_per_run = 5
  min_time_between_runs = 6
  
  # Notifications
  enable_notifications = true
  notification_emails = [
    "admin@example.com"
  ]
  
  # Metrics and monitoring
  enable_metrics = true
  enable_alarm = true
  
  # Chaos window
  chaos_window_start = 2
  chaos_window_end = 6
  
  # Duration limit
  chaos_duration_minutes = 30
  
  # Custom tags
  chaos_tags = {
    "Environment" = "staging"
    "Team"       = "platform"
  }
}

# Output basic information
output "chaos_status" {
  description = "Basic Chaos Monkey status"
  value = {
    enabled = module.chaos_monkey.chaos_enabled
    intensity = module.chaos_monkey.chaos_intensity
    safe_mode = module.chaos_monkey.chaos_safe_mode
    targets = module.chaos_monkey.chaos_target_resources
    dashboard_url = module.chaos_monkey.chaos_dashboard_url
  }
}
