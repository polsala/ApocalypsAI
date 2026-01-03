# Security Tests for Chaos Monkey

variable "test_security" {
  description = "Enable security tests"
  type        = bool
  default     = false
}

variable "test_dry_run" {
  description = "Force dry run mode for security tests"
  type        = bool
  default     = true
}

# Security test configurations
locals {
  run_security = var.test_security
}

# Test 1: Security - No production resources should be targeted
module "chaos_security_production" {
  count = local.run_security ? 1 : 0
  source = "../.."
  
  chaos_enabled = true
  dry_run       = var.test_dry_run
  
  # Should exclude all production resources
  excluded_resources = [
    "production-db",
    "production-app",
    "production-api",
    "prod-",
    "prod_"
  ]
}

# Test 2: Security - Resource type validation
module "chaos_security_types" {
  count = local.run_security ? 1 : 0
  source = "../.."
  
  chaos_enabled = true
  dry_run       = var.test_dry_run
  
  # Only target safe resource types
  target_resource_types = [
    "aws_instance",
    "aws_autoscaling_group"
  ]
}

# Test 3: Security - Rate limiting
module "chaos_security_rate_limit" {
  count = local.run_security ? 1 : 0
  source = "../.."
  
  chaos_enabled = true
  dry_run       = var.test_dry_run
  
  # Conservative rate limiting
  chaos_interval_hours = 24
  max_resources_per_run = 1
}

# Security test outputs
output "security_production_exclusions" {
  value       = local.run_security ? module.chaos_security_production[0].chaos_exclusions : []
  description = "Production resource exclusions"
}

output "security_target_types" {
  value       = local.run_security ? module.chaos_security_types[0].chaos_resources_targeted : []
  description = "Targeted resource types for security"
}

output "security_rate_limit" {
  value       = local.run_security ? "${module.chaos_security_rate_limit[0].chaos_schedule}" : "disabled"
  description = "Rate limiting configuration"
}

# Security validation
resource "null_resource" "security_validation" {
  count = local.run_security ? 1 : 0
  
  triggers = {
    production_excluded = contains(module.chaos_security_production[0].chaos_exclusions, "production-db")
    safe_resource_types = contains(module.chaos_security_types[0].chaos_resources_targeted, "aws_instance")
    rate_limited = module.chaos_security_rate_limit[0].chaos_schedule != ""
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      echo "=== SECURITY VALIDATION ===" >> security_validation.log
      echo "Production resources excluded: ${self.triggers.production_excluded}" >> security_validation.log
      echo "Safe resource types targeted: ${self.triggers.safe_resource_types}" >> security_validation.log
      echo "Rate limiting enabled: ${self.triggers.rate_limited}" >> security_validation.log
      echo "=== VALIDATION COMPLETE ===" >> security_validation.log
    EOT
  }
}
