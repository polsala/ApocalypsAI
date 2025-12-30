# Test: Basic Chaos Monkey Functionality

# Configure test providers
provider "aws" {
  region = "us-west-2"
}

# Test 1: Disabled chaos monkey
module "test_disabled" {
  source = "../.."
  
  enabled = false
  destruction_probability = 0.5
  safe_mode = true
}

# Test 2: Enabled with safe mode
module "test_safe_mode" {
  source = "../.."
  
  enabled = true
  destruction_probability = 1.0  # 100% chance
  safe_mode = true
  chaos_window_start = "00:00"
  chaos_window_end   = "23:59"
}

# Test 3: Configuration validation
module "test_validation" {
  source = "../.."
  
  enabled = true
  destruction_probability = 0.1
  safe_mode = true
  chaos_window_start = "09:00"
  chaos_window_end   = "17:00"
  excluded_resources = ["test-exclude"]
}

# Test outputs
output "test_disabled_status" {
  value = {
    enabled = module.test_disabled.chaos_enabled
    should_chaos = module.test_disabled.should_perform_chaos
  }
}

output "test_safe_mode_status" {
  value = {
    enabled = module.test_safe_mode.chaos_enabled
    safe_mode = module.test_safe_mode.safe_mode
    should_chaos = module.test_safe_mode.should_perform_chaos
  }
}

output "test_validation_status" {
  value = {
    enabled = module.test_validation.chaos_enabled
    excluded_count = module.test_validation.excluded_resources_count
    window = module.test_validation.chaos_window
  }
}
