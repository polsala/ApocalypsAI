# Test configuration for Chaos Monkey module

terraform {
  required_version = ">= 1.0"
}

# Test variables
variable "test_chaos_enabled" {
  type    = bool
  default = true
}

variable "test_chaos_probability" {
  type    = number
  default = 0.1
}

variable "test_dry_run" {
  type    = bool
  default = true
}

# Test module configuration
module "test_chaos_monkey" {
  source = "../.."
  
  chaos_enabled     = var.test_chaos_enabled
  chaos_probability = var.test_chaos_probability
  dry_run          = var.test_dry_run
  
  # Minimal configuration for testing
  target_resource_types = ["aws_instance"]
  excluded_resources    = ["test-excluded"]
}

# Test outputs
output "test_chaos_enabled" {
  value = module.test_chaos_monkey.chaos_enabled
}

output "test_chaos_probability" {
  value = module.test_chaos_monkey.chaos_probability
}

output "test_target_count" {
  value = module.test_chaos_monkey.target_count
}

output "test_dry_run_mode" {
  value = module.test_chaos_monkey.dry_run_mode
}

output "test_chaos_metrics" {
  value = module.test_chaos_monkey.chaos_metrics
}

# Test validation rules
# Note: These would typically be tested with terraform validate
# and terraform plan in a CI/CD pipeline

# Test 1: Chaos enabled with dry-run should work
locals {
  test_1_should_pass = var.test_chaos_enabled && var.test_dry_run
}

# Test 2: Chaos enabled without dry-run should trigger validation warning
locals {
  test_2_should_warn = var.test_chaos_enabled && !var.test_dry_run
}

# Test 3: High probability should trigger warning
locals {
  test_3_high_prob = var.test_chaos_probability > 0.5
}

output "test_results" {
  value = {
    test_1_passes     = local.test_1_should_pass
    test_2_warns      = local.test_2_should_warn
    test_3_high_prob  = local.test_3_high_prob
    chaos_metrics     = module.test_chaos_monkey.chaos_metrics
  }
}
