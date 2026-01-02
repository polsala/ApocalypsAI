# Test file for Chaos Monkey Terraform Module

# Test 1: Verify module can be instantiated with minimal config
module "chaos_monkey_minimal" {
  source = "../"
  
  # Minimal configuration
  enabled = false
}

# Test 2: Verify module with full configuration
module "chaos_monkey_full" {
  source = "../"
  
  enabled                    = true
  destruction_probability    = 0.1
  target_resources          = ["aws_instance", "aws_s3_bucket"]
  excluded_resources        = ["aws_s3_bucket.critical"]
  max_destructions_per_run  = 2
  chaos_schedule            = "weekdays"
  dry_run                   = true
  backup_before_destruction = true
  min_resource_age_hours    = 2
  chaos_duration_minutes    = 15
  excluded_regions          = ["us-east-1"]
  chaos_tags = {
    Environment = "test"
  }
}

# Test 3: Verify safety validations
# This should fail validation if enabled in production
module "chaos_monkey_production" {
  source = "../"
  
  enabled = true
  environment = "production"  # This should trigger validation error
}

# Test 4: Verify probability validation
module "chaos_monkey_invalid_prob" {
  source = "../"
  
  enabled = true
  destruction_probability = 1.5  # This should trigger validation error
}

# Test 5: Verify max destructions validation
module "chaos_monkey_invalid_max" {
  source = "../"
  
  enabled = true
  max_destructions_per_run = 15  # This should trigger validation error
}

# Test outputs
output "minimal_config_outputs" {
  value = module.chaos_monkey_minimal.chaos_status
}

output "full_config_outputs" {
  value = module.chaos_monkey_full.chaos_status
}

output "minimal_config_warnings" {
  value = module.chaos_monkey_minimal.safety_warnings
}

output "full_config_warnings" {
  value = module.chaos_monkey_full.safety_warnings
}

# Test that outputs are properly formatted
output "output_format_test" {
  value = {
    has_enabled_field        = contains(keys(module.chaos_monkey_full.chaos_status), "enabled")
    has_probability_field    = contains(keys(module.chaos_monkey_full.chaos_status), "destruction_probability")
    has_max_destructions_field = contains(keys(module.chaos_monkey_full.chaos_status), "max_destructions_per_run")
    has_schedule_field       = contains(keys(module.chaos_monkey_full.chaos_status), "chaos_schedule")
  }
}
