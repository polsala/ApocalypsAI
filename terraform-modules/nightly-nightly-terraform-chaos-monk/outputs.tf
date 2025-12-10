# Chaos monkey execution status
output "chaos_enabled" {
  description = "Whether chaos monkey is enabled"
  value       = var.enable_chaos
  sensitive   = false
}

# Chaos probability
output "chaos_probability" {
  description = "Current chaos probability setting"
  value       = var.chaos_probability
  sensitive   = false
}

# Last chaos execution result
output "last_chaos_result" {
  description = "Result of last chaos execution"
  value       = var.enable_chaos ? "Executed" : "Skipped"
  sensitive   = false
}

# Chaos window
output "chaos_window" {
  description = "Active chaos execution window"
  value       = "${var.chaos_window_start}:00 - ${var.chaos_window_end}:00"
  sensitive   = false
}

# Exclusion criteria
output "exclusion_criteria" {
  description = "Resources excluded from chaos"
  value       = {
    tag_key   = var.exclusion_tag_key
    tag_value = var.exclusion_tag_value
  }
  sensitive   = false
}

# Safety warning
output "safety_warning" {
  description = "Safety warning for chaos operations"
  value       = <<-EOT
    ⚠️  SAFETY WARNING ⚠️
    
    This module will randomly terminate cloud resources.
    Ensure you have:
    1. Set enable_chaos = false for production environments
    2. Properly configured exclusion tags
    3. Backups and recovery procedures in place
    4. Team awareness and approval
    
    Use at your own risk!
  EOT
  sensitive   = false
}
