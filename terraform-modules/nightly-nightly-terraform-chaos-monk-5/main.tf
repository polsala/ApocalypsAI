terraform {
  required_version = ">= 1.0"
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

# Configuration variables
variable "chaos_enabled" {
  description = "Enable/disable chaos mode"
  type        = bool
  default     = false
}

variable "chaos_probability" {
  description = "Probability (0-1) of destroying a resource"
  type        = number
  default     = 0.05
}

variable "chaos_schedule" {
  description = "Cron schedule for chaos execution"
  type        = string
  default     = "0 3 * * *"
}

variable "target_resource_types" {
  description = "Resource types to target (empty = all)"
  type        = list(string)
  default     = []
}

variable "excluded_resources" {
  description = "Resource names to exclude from chaos"
  type        = list(string)
  default     = []
}

variable "dry_run" {
  description = "Enable dry-run mode (no actual destruction)"
  type        = bool
  default     = true
}

variable "log_level" {
  description = "Logging verbosity level"
  type        = string
  default     = "INFO"
}

# Generate random number for chaos decision
resource "random_integer" "chaos_selector" {
  count  = var.chaos_enabled ? 1 : 0
  min    = 0
  max    = 100
  result = random_shuffle.chaos_targets.result[0]
}

# Get current Terraform state
data "terraform_remote_state" "current_state" {
  backend = "local"
  
  # Note: In practice, you'd configure this based on your state backend
  # For this example, we'll assume local state
}

# Identify resources to potentially target for chaos
locals {
  # This is a simplified example - in practice, you'd parse the state file
  # or use terraform state list command to get actual resources
  potential_targets = [
    "aws_instance.example",
    "aws_security_group.example",
    "aws_rds_instance.example"
  ]
  
  # Filter targets based on configuration
  filtered_targets = [for target in local.potential_targets :
    (length(var.target_resource_types) == 0 || 
     contains(var.target_resource_types, split(".", target)[0])) &&
    !contains(var.excluded_resources, split(".", target)[1])
  ]
  
  # Determine if chaos should occur based on probability
  chaos_should_occur = var.chaos_enabled && 
                      (var.dry_run || random_integer.chaos_selector[0].result / 100 < var.chaos_probability)
}

# Chaos execution logic
resource "null_resource" "chaos_execution" {
  count = local.chaos_should_occur ? 1 : 0
  
  triggers = {
    timestamp = timestamp()
    dry_run   = var.dry_run
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      #!/bin/bash
      echo "[INFO] Chaos Monkey executing at ${timestamp()}"
      echo "[INFO] Dry run mode: ${var.dry_run}"
      echo "[INFO] Target resources: ${join(", ", local.filtered_targets)}"
      
      if [ "${var.dry_run}" = "true" ]; then
        echo "[INFO] DRY RUN - No actual resources will be destroyed"
        for resource in ${join(" ", local.filtered_targets)}; do
          echo "[DRY RUN] Would destroy: $resource"
        done
      else
        echo "[WARNING] ACTUAL CHAOS - Resources will be destroyed!"
        for resource in ${join(" ", local.filtered_targets)}; do
          echo "[DESTROYING] $resource"
          # In a real implementation, you'd use terraform destroy -target
          # terraform destroy -target=$resource -auto-approve
        done
      fi
      
      echo "[INFO] Chaos execution completed"
    EOT
  }
}

# Resource recreation logic
resource "null_resource" "resource_recreation" {
  count = local.chaos_should_occur && !var.dry_run ? 1 : 0
  
  triggers = {
    chaos_execution_id = null_resource.chaos_execution[0].id
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      #!/bin/bash
      echo "[INFO] Recreating destroyed resources"
      # In a real implementation, you'd use terraform apply
      # terraform apply -auto-approve
      echo "[INFO] Resource recreation completed"
    EOT
  }
}

# Logging and metrics
resource "null_resource" "chaos_metrics" {
  count = var.chaos_enabled ? 1 : 0
  
  provisioner "local-exec" {
    command = <<-EOT
      #!/bin/bash
      echo "[METRICS] Chaos enabled: ${var.chaos_enabled}"
      echo "[METRICS] Chaos probability: ${var.chaos_probability}"
      echo "[METRICS] Dry run mode: ${var.dry_run}"
      echo "[METRICS] Target count: ${length(local.filtered_targets)}"
      echo "[METRICS] Execution time: ${timestamp()}"
      
      # Write metrics to file for monitoring systems
      cat << EOF > chaos_metrics.json
      {
        "enabled": ${var.chaos_enabled},
        "probability": ${var.chaos_probability},
        "dry_run": ${var.dry_run},
        "target_count": ${length(local.filtered_targets)},
        "execution_time": "${timestamp()}",
        "targets": [${join(", ", [for t in local.filtered_targets : "\"${t}\""])}]
      }
      EOF
    EOT
  }
}

# Outputs
output "chaos_enabled" {
  value = var.chaos_enabled
}

output "chaos_probability" {
  value = var.chaos_probability
}

output "target_count" {
  value = length(local.filtered_targets)
}

output "target_resources" {
  value = local.filtered_targets
}

output "dry_run_mode" {
  value = var.dry_run
}

output "chaos_metrics" {
  value = {
    enabled        = var.chaos_enabled
    probability    = var.chaos_probability
    dry_run        = var.dry_run
    target_count   = length(local.filtered_targets)
    target_resources = local.filtered_targets
    execution_time = timestamp()
  }
}

output "chaos_schedule" {
  value = var.chaos_schedule
}

output "excluded_resources" {
  value = var.excluded_resources
}
