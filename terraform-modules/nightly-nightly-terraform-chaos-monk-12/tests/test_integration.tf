# Integration Tests for Chaos Monkey

variable "test_integration" {
  description = "Enable integration tests"
  type        = bool
  default     = false
}

variable "test_dry_run" {
  description = "Force dry run mode for integration tests"
  type        = bool
  default     = true
}

# Only run integration tests if enabled
locals {
  run_integration = var.test_integration
}

# Test resources for integration testing
resource "aws_instance" "integration_test_1" {
  count = local.run_integration ? 1 : 0
  
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"
  
  tags = {
    Name        = "integration-test-instance-1"
    Environment = "test"
    Purpose     = "chaos-integration-test"
  }
}

resource "aws_instance" "integration_test_2" {
  count = local.run_integration ? 1 : 0
  
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"
  
  tags = {
    Name        = "integration-test-instance-2"
    Environment = "test"
    Purpose     = "chaos-integration-test"
  }
}

# Integration test module
module "chaos_integration" {
  count = local.run_integration ? 1 : 0
  source = "../.."
  
  chaos_enabled = true
  dry_run       = var.test_dry_run
  chaos_interval_hours = 1
  max_resources_per_run = 2
  
  target_resource_types = [
    "aws_instance"
  ]
  
  excluded_resources = [
    "integration-test-instance-2" # Exclude one instance
  ]
}

# Integration test outputs
output "integration_test_status" {
  value       = local.run_integration ? module.chaos_integration[0].chaos_status : "disabled"
  description = "Integration test chaos status"
}

output "integration_test_log_group" {
  value       = local.run_integration ? module.chaos_integration[0].chaos_log_group : "disabled"
  description = "Integration test log group"
}

output "integration_test_exclusions" {
  value       = local.run_integration ? module.chaos_integration[0].chaos_exclusions : []
  description = "Integration test exclusions"
}
