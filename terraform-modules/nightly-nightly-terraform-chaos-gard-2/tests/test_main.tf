# Basic test to verify the chaos garden module can be planned
# This is a placeholder for more comprehensive testing

module "chaos_garden_test" {
  source = "../"
  
  region          = "us-east-1"
  environment   = "test"
  chaos_level   = "low"
  
  enable_network_chaos = true
  enable_compute_chaos = true
  enable_storage_chaos = true
  
  instance_count = 1
  
  notification_email = "test@example.com"
  destroy_after_hours = 1
  
  tags = {
    test = "true"
    purpose = "chaos-garden-testing"
  }
}

# Test that outputs are properly generated
output "test_chaos_garden_name" {
  value = module.chaos_garden_test.chaos_garden_name
}

output "test_chaos_garden_summary" {
  value = module.chaos_garden_test.chaos_garden_summary
}

# Test that resources are tagged correctly
# (This would be verified by the test runner checking resource tags)
