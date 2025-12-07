# Test file for Chaos Garden Terraform Module

# Test 1: Disabled chaos garden
module "test_disabled" {
  source = "../"
  
  chaos_level = 0
  enabled     = false
}

# Test 2: Low chaos level
module "test_low_chaos" {
  source = "../"
  
  chaos_level = 2
  enabled     = true
  protected_resources = ["test-db"]
}

# Test 3: High chaos level
module "test_high_chaos" {
  source = "../"
  
  chaos_level = 7
  enabled     = true
  protected_resources = ["critical-service"]
  chaos_schedule = "0 2 * * *"
}

# Test outputs
output "test_disabled_status" {
  value = module.test_disabled.chaos_status
}

output "test_low_chaos_status" {
  value = module.test_low_chaos.chaos_status
}

output "test_high_chaos_status" {
  value = module.test_high_chaos.chaos_status
}

output "test_low_chaos_severity" {
  value = module.test_low_chaos.chaos_severity
}

output "test_high_chaos_severity" {
  value = module.test_high_chaos.chaos_severity
}

output "test_protected_resources" {
  value = module.test_low_chaos.protected_resources
}

# Test validation
locals {
  validation_tests = {
    disabled_chaos = module.test_disabled.chaos_status == "Chaos Garden is DISABLED"
    low_chaos_enabled = contains(module.test_low_chaos.chaos_status, "ACTIVE")
    high_chaos_enabled = contains(module.test_high_chaos.chaos_status, "ACTIVE")
    low_chaos_severity = module.test_low_chaos.chaos_severity == "Moderate"
    high_chaos_severity = module.test_high_chaos.chaos_severity == "Severe"
    protected_resources_count = length(module.test_low_chaos.protected_resources) == 1
  }
}

output "validation_results" {
  value = local.validation_tests
}

output "all_tests_pass" {
  value = alltrue([
    local.validation_tests.disabled_chaos,
    local.validation_tests.low_chaos_enabled,
    local.validation_tests.high_chaos_enabled,
    local.validation_tests.low_chaos_severity,
    local.validation_tests.high_chaos_severity,
    local.validation_tests.protected_resources_count
  ])
}
