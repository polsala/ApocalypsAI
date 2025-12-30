# Test: Input Validation

# Test invalid probability (should fail)
# module "test_invalid_probability" {
#   source = "../.."
#   enabled = true
#   destruction_probability = 1.5  # Invalid: > 1.0
# }

# Test invalid time format (should fail)
# module "test_invalid_time" {
#   source = "../.."
#   enabled = true
#   chaos_window_start = "25:00"  # Invalid: > 23:59
# }

# Test valid configurations
module "test_valid_config" {
  source = "../.."
  
  enabled = true
  destruction_probability = 0.25
  chaos_window_start = "10:30"
  chaos_window_end   = "14:45"
  excluded_resources = ["test1", "test2", "test3"]
  safe_mode = true
  log_level = "DEBUG"
}

# Test outputs for valid configuration
output "valid_config_outputs" {
  value = {
    enabled = module.test_valid_config.chaos_enabled
    probability = module.test_valid_config.destruction_probability
    window_start = module.test_valid_config.chaos_window.start
    window_end = module.test_valid_config.chaos_window.end
    excluded_count = module.test_valid_config.excluded_resources_count
    safe_mode = module.test_valid_config.safe_mode
    log_level = module.test_valid_config.log_level
  }
}
