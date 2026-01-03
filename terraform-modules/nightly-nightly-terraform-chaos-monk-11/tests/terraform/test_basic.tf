# Test: Basic Chaos Monkey Module

module "chaos_monkey_test" {
  source = "../.."
  
  prefix           = "test-chaos"
  chaos_schedule   = "rate(1 hour)"
  resource_types   = ["ec2"]
  max_chaos_per_run = 1
  dry_run          = true
}

# Test outputs
output "test_lambda_arn" {
  value = module.chaos_monkey_test.chaos_lambda_arn
}

output "test_schedule_rule" {
  value = module.chaos_monkey_test.chaos_schedule_rule
}

output "test_module_enabled" {
  value = module.chaos_monkey_test.module_enabled
}
