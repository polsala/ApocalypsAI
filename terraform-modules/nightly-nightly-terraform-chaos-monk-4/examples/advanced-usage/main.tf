# Example: Advanced Chaos Monkey Configuration

# AWS Provider
provider "aws" {
  alias  = "primary"
  region = "us-east-1"
}

# Azure Provider (example)
# provider "azurerm" {
#   alias = "azure"
#   features {}
# }

# GCP Provider (example)
# provider "google" {
#   alias  = "gcp"
#   project = var.gcp_project
#   region  = var.gcp_region
# }

# AWS Chaos Monkey
module "aws_chaos_monkey" {
  source = "../.."
  
  # AWS-specific configuration
  cloud_provider = "aws"
  aws_region     = "us-east-1"
  
  # Chaos configuration
  chaos_level = "extreme"
  enabled     = true
  dry_run     = false
  
  # Target resources
  target_instances = [
    "i-0123456789abcdef0",
    "i-0987654321fedcba0",
    "i-11111111111111111",
    "i-22222222222222222",
    "i-33333333333333333"
  ]
  
  # Safety configuration
  minimum_instance_count = 3
  circuit_breaker_threshold = 5
  
  # Schedule (every 15 minutes during business hours)
  chaos_schedule = "cron(0/15 9-17 ? * MON-FRI *)"
  
  # Maintenance windows (disable chaos)
  maintenance_windows = [
    "cron(0 2 ? * *)",  # Daily at 2 AM
    "cron(0 0 ? * SUN *)" # Weekly on Sunday at midnight
  ]
  
  # Chaos types
  chaos_types = [
    "instance_termination",
    "instance_stop",
    "network_latency",
    "cpu_stress",
    "memory_stress",
    "disk_io_stress"
  ]
  
  # Advanced configuration
  chaos_probability_override = -1
  
  # Resource selection tags
  included_tags = {
    Environment = "production"
    Team        = "platform"
    ChaosReady  = "true"
  }
  
  excluded_tags = {
    Critical    = "true"
    Database    = "true"
    LoadBalancer = "true"
  }
  
  # Notifications
  notification_email = "platform-team@example.com"
  slack_webhook_url  = "https://hooks.slack.com/services/XXX/YYY/ZZZ"
  
  # Verbose logging
  verbose_logging = true
}

# Azure Chaos Monkey (example)
# module "azure_chaos_monkey" {
#   source = "../.."
#   
#   cloud_provider = "azure"
#   azure_location = "eastus"
#   
#   chaos_level = "medium"
#   enabled     = true
#   
#   # Azure-specific targets would go here
#   # target_vms = [...]
#   
#   # ... other configuration
# }

# GCP Chaos Monkey (example)
# module "gcp_chaos_monkey" {
#   source = "../.."
#   
#   cloud_provider = "gcp"
#   gcp_project    = var.gcp_project
#   gcp_zone       = "us-central1-a"
#   
#   chaos_level = "gentle"
#   enabled     = true
#   
#   # GCP-specific targets would go here
#   # target_instances = [...]
#   
#   # ... other configuration
# }

# Output configurations
output "aws_chaos_status" {
  value = module.aws_chaos_monkey.chaos_status
}

output "aws_chaos_log_group" {
  value = module.aws_chaos_monkey.log_group_name
}

output "aws_chaos_lambda" {
  value = module.aws_chaos_monkey.lambda_function_name
}

output "aws_chaos_schedule" {
  value = module.aws_chaos_monkey.chaos_schedule
}

output "aws_target_count" {
  value = module.aws_chaos_monkey.target_instance_count
}

# Example outputs for other providers (commented out)
# output "azure_chaos_status" {
#   value = module.azure_chaos_monkey.chaos_status
# }
# 
# output "gcp_chaos_status" {
#   value = module.gcp_chaos_monkey.chaos_status
# }
