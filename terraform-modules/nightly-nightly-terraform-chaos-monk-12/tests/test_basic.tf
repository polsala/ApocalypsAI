# Basic Chaos Monkey Tests

# Test 1: Chaos disabled should not create resources
module "chaos_disabled" {
  source = "../.."
  
  chaos_enabled = false
  dry_run       = true
}

# Test 2: Chaos enabled with dry run
module "chaos_dry_run" {
  source = "../.."
  
  chaos_enabled = true
  dry_run       = true
  chaos_interval_hours = 1
  max_resources_per_run = 1
}

# Test 3: Chaos enabled with actual execution (use with caution)
module "chaos_enabled" {
  source = "../.."
  
  chaos_enabled = true
  dry_run       = false
  chaos_interval_hours = 1
  max_resources_per_run = 1
}

# Test 4: Chaos with exclusions
module "chaos_with_exclusions" {
  source = "../.."
  
  chaos_enabled = true
  dry_run       = true
  excluded_resources = [
    "test-exclude-1",
    "test-exclude-2"
  ]
}

# Test 5: Chaos with different resource types
module "chaos_resource_types" {
  source = "../.."
  
  chaos_enabled = true
  dry_run       = true
  target_resource_types = [
    "aws_instance",
    "aws_rds_instance"
  ]
}

# Test outputs
output "test_chaos_disabled_status" {
  value = module.chaos_disabled.chaos_status
}

output "test_chaos_dry_run_status" {
  value = module.chaos_dry_run.chaos_status
}

output "test_chaos_enabled_status" {
  value = module.chaos_enabled.chaos_status
}

output "test_chaos_exclusions" {
  value = module.chaos_with_exclusions.chaos_exclusions
}

output "test_chaos_resource_types" {
  value = module.chaos_resource_types.chaos_resources_targeted
}
