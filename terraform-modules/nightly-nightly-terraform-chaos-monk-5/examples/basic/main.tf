# Basic Chaos Monkey example

module "chaos_monkey" {
  source = "../.."
  
  # Enable chaos mode
  chaos_enabled = true
  
  # Low probability for testing
  chaos_probability = 0.05
  
  # Daily chaos at 3 AM
  chaos_schedule = "0 3 * * *"
  
  # Dry-run mode for safety
  dry_run = true
}

# Output basic information
output "chaos_status" {
  value = "Chaos Monkey is ${module.chaos_monkey.chaos_enabled ? "enabled" : "disabled"}"
}

output "target_count" {
  value = module.chaos_monkey.target_count
}
