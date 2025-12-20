# Example: Basic Chaos Monkey Configuration

# Configure AWS provider
provider "aws" {
  region = "us-east-1"
}

# Import the chaos monkey module
module "chaos_monkey" {
  source = "../.."
  
  # Basic configuration
  chaos_level = "medium"
  enabled     = true
  dry_run     = false
  
  # Target resources
  target_instances = [
    "i-0123456789abcdef0",
    "i-0987654321fedcba0",
    "i-11111111111111111"
  ]
  
  # Safety configuration
  minimum_instance_count = 2
  
  # Schedule (every 30 minutes)
  chaos_schedule = "cron(0/30 * * * ? *)"
  
  # Chaos configuration
  chaos_duration = 5
  chaos_types    = ["instance_termination", "instance_stop"]
  
  # Notifications
  notification_email = "ops-team@example.com"
  
  # Tags for resource selection
  included_tags = {
    Environment = "production"
    Team        = "platform"
  }
  
  excluded_tags = {
    Critical = "true"
  }
}

# Output the chaos monkey status
output "chaos_monkey_status" {
  value = module.chaos_monkey.chaos_status
}

output "chaos_log_group" {
  value = module.chaos_monkey.log_group_name
}

output "chaos_lambda_arn" {
  value = module.chaos_monkey.lambda_function_arn
}
