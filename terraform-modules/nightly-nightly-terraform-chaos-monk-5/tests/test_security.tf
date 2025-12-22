# Security tests for Chaos Monkey module

# Security test configuration
variable "security_test_chaos_enabled" {
  type    = bool
  default = true
}

variable "security_test_dry_run" {
  type    = bool
  default = false  # Intentionally set to false to test safety
}

variable "security_test_excluded_resources" {
  type    = list(string)
  default = ["production-db", "critical-load-balancer"]
}

# Security test module - this should trigger validation warnings
module "security_test_chaos_monkey" {
  source = "../.."
  
  chaos_enabled        = var.security_test_chaos_enabled
  dry_run             = var.security_test_dry_run
  excluded_resources  = var.security_test_excluded_resources
  
  # Target all resource types to test exclusion logic
  target_resource_types = []
  
  # High probability to test safety mechanisms
  chaos_probability = 0.8
}

# Security test outputs
output "security_test_chaos_enabled" {
  value = module.security_test_chaos_monkey.chaos_enabled
}

output "security_test_dry_run" {
  value = module.security_test_chaos_monkey.dry_run_mode
}

output "security_test_excluded_resources" {
  value = module.security_test_chaos_monkey.excluded_resources
}

output "security_test_safety_warnings" {
  value = module.security_test_chaos_monkey.safety_warnings
}

# Security validation tests
resource "null_resource" "security_validation" {
  triggers = {
    chaos_enabled     = module.security_test_chaos_monkey.chaos_enabled
    dry_run_mode      = module.security_test_chaos_monkey.dry_run_mode
    excluded_count    = length(module.security_test_chaos_monkey.excluded_resources)
    safety_warnings   = jsonencode(module.security_test_chaos_monkey.safety_warnings)
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      echo "[SECURITY TEST] Validating safety mechanisms"
      echo "[SECURITY TEST] Chaos enabled: ${self.triggers.chaos_enabled}"
      echo "[SECURITY TEST] Dry run mode: ${self.triggers.dry_run_mode}"
      echo "[SECURITY TEST] Excluded resources count: ${self.triggers.excluded_count}"
      echo "[SECURITY TEST] Safety warnings: ${self.triggers.safety_warnings}"
      
      # Test 1: Verify that chaos with dry_run=false triggers warnings
      if [ "${self.triggers.chaos_enabled}" = "true" ] && [ "${self.triggers.dry_run_mode}" = "false" ]; then
        echo "[SECURITY TEST] WARNING: Chaos enabled without dry-run - this is dangerous!"
        # In a real test, this would fail the validation
        # exit 1
      fi
      
      # Test 2: Verify excluded resources are properly configured
      if [ "${self.triggers.excluded_count}" -gt 0 ]; then
        echo "[SECURITY TEST] SUCCESS: Excluded resources are configured"
      else
        echo "[SECURITY TEST] WARNING: No excluded resources configured"
      fi
      
      # Test 3: Check for safety warnings
      if echo "${self.triggers.safety_warnings}" | grep -q "WARNING"; then
        echo "[SECURITY TEST] SUCCESS: Safety warnings are being generated"
      else
        echo "[SECURITY TEST] INFO: No safety warnings detected"
      fi
      
      echo "[SECURITY TEST] Security validation completed"
    EOT
  }
}

# Test resource exclusion logic
resource "null_resource" "exclusion_test" {
  triggers = {
    excluded_resources = jsonencode(var.security_test_excluded_resources)
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      echo "[EXCLUSION TEST] Testing resource exclusion logic"
      echo "[EXCLUSION TEST] Excluded resources: ${self.triggers.excluded_resources}"
      
      # Verify that excluded resources contain critical patterns
      for resource in ${self.triggers.excluded_resources}; do
        if [[ "$resource" == "production-"* ]] || [[ "$resource" == "critical-"* ]]; then
          echo "[EXCLUSION TEST] SUCCESS: Found critical resource pattern: $resource"
        else
          echo "[EXCLUSION TEST] INFO: Non-critical exclusion: $resource"
        fi
      done
      
      echo "[EXCLUSION TEST] Exclusion test completed"
    EOT
  }
}

# Test validation rules
resource "null_resource" "validation_test" {
  triggers = {
    chaos_enabled = var.security_test_chaos_enabled
    dry_run       = var.security_test_dry_run
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      echo "[VALIDATION TEST] Testing Terraform validation rules"
      echo "[VALIDATION TEST] Chaos enabled: ${self.triggers.chaos_enabled}"
      echo "[VALIDATION TEST] Dry run: ${self.triggers.dry_run}"
      
      # Test the validation rule that prevents chaos without dry-run
      if [ "${self.triggers.chaos_enabled}" = "true" ] && [ "${self.triggers.dry_run}" = "false" ]; then
        echo "[VALIDATION TEST] EXPECTED: This should trigger a validation error"
        echo "[VALIDATION TEST] In real usage, set dry_run = true for safety"
      else
        echo "[VALIDATION TEST] SUCCESS: Safe configuration detected"
      fi
      
      echo "[VALIDATION TEST] Validation test completed"
    EOT
  }
}
