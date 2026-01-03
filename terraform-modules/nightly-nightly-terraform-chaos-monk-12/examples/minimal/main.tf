# Minimal Chaos Monkey Example

# Configure providers
provider "aws" {
  region = "us-east-1"
}

# Minimal Chaos Monkey Module
module "chaos_monkey" {
  source = "../.."
  
  # Enable chaos engineering
  chaos_enabled = true
  
  # Minimal configuration
  chaos_interval_hours = 1
  max_resources_per_run = 1
  
  # Only target EC2 instances
  target_resource_types = ["aws_instance"]
  
  # Dry run mode for safety
  dry_run = true
}

# Minimal test instance
resource "aws_instance" "test" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"
  
  tags = {
    Name        = "chaos-test-instance"
    Environment = "test"
    Purpose     = "chaos-testing"
  }
}

# Output minimal configuration
output "minimal_chaos_config" {
  value = {
    enabled  = module.chaos_monkey.chaos_status
    log_group = module.chaos_monkey.chaos_log_group
    schedule = module.chaos_monkey.chaos_schedule
    dry_run  = var.dry_run
  }
}
