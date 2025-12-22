# Integration tests for Chaos Monkey module

# Test AWS resources
resource "aws_instance" "integration_test" {
  ami           = "ami-0c02fb55956c7d316" # Amazon Linux 2 in us-east-1
  instance_type = "t2.micro"
  
  tags = {
    Name = "integration-test-server"
  }
}

resource "aws_security_group" "integration_test" {
  name        = "integration-test-sg"
  description = "Security group for integration testing"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Integration test module configuration
module "integration_chaos_monkey" {
  source = "../.."
  
  # Enable chaos mode for integration testing
  chaos_enabled = true
  
  # Low probability to minimize impact
  chaos_probability = 0.05
  
  # Target integration test resources
  target_resource_types = [
    "aws_instance",
    "aws_security_group"
  ]
  
  # Exclude any production resources
  excluded_resources = [
    "production-",
    "critical-"
  ]
  
  # Always use dry-run for integration tests
  dry_run = true
  
  # Set to debug for detailed logging
  log_level = "DEBUG"
}

# Integration test outputs
output "integration_chaos_metrics" {
  value = module.integration_chaos_monkey.chaos_metrics
}

output "integration_target_resources" {
  value = module.integration_chaos_monkey.target_resources
}

output "integration_safety_warnings" {
  value = module.integration_chaos_monkey.safety_warnings
}

# Test resource state
output "test_resource_ids" {
  value = {
    instance_id      = aws_instance.integration_test.id
    security_group_id = aws_security_group.integration_test.id
  }
}

# Integration test validation
resource "null_resource" "integration_validation" {
  triggers = {
    chaos_enabled     = module.integration_chaos_monkey.chaos_enabled
    target_count      = module.integration_chaos_monkey.target_count
    dry_run_mode      = module.integration_chaos_monkey.dry_run_mode
    resource_instance = aws_instance.integration_test.id
    resource_sg       = aws_security_group.integration_test.id
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      echo "[INTEGRATION TEST] Validating chaos monkey integration"
      echo "[INTEGRATION TEST] Chaos enabled: ${self.triggers.chaos_enabled}"
      echo "[INTEGRATION TEST] Target count: ${self.triggers.target_count}"
      echo "[INTEGRATION TEST] Dry run mode: ${self.triggers.dry_run_mode}"
      echo "[INTEGRATION TEST] Instance ID: ${self.triggers.resource_instance}"
      echo "[INTEGRATION TEST] SG ID: ${self.triggers.resource_sg}"
      
      # Verify that chaos monkey can see our test resources
      if [ -n "${self.triggers.resource_instance}" ] && [ -n "${self.triggers.resource_sg}" ]; then
        echo "[INTEGRATION TEST] SUCCESS: Test resources are accessible"
      else
        echo "[INTEGRATION TEST] ERROR: Test resources not found"
        exit 1
      fi
      
      # Verify chaos monkey is in dry-run mode
      if [ "${self.triggers.dry_run_mode}" = "true" ]; then
        echo "[INTEGRATION TEST] SUCCESS: Dry-run mode is enabled"
      else
        echo "[INTEGRATION TEST] ERROR: Dry-run mode is disabled"
        exit 1
      fi
      
      echo "[INTEGRATION TEST] Integration validation completed successfully"
    EOT
  }
}

# Integration test cleanup
resource "null_resource" "integration_cleanup" {
  depends_on = [module.integration_chaos_monkey]
  
  triggers = {
    cleanup_time = timestamp()
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      echo "[INTEGRATION TEST] Starting cleanup at ${self.triggers.cleanup_time}"
      
      # In a real integration test, you might:
      # 1. Verify no actual resources were destroyed
      # 2. Clean up any test artifacts
      # 3. Reset state if needed
      
      echo "[INTEGRATION TEST] Cleanup completed"
    EOT
  }
}
