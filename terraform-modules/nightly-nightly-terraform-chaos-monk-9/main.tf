terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0"
    }
  }
}

# Random provider for chaos selection
provider "random" {}

# Variables
variable "enabled" {
  description = "Enable/disable chaos monkey"
  type        = bool
  default     = false
}

variable "destruction_probability" {
  description = "Probability (0.0-1.0) of destroying a resource"
  type        = number
  default     = 0.05
  validation {
    condition     = var.destruction_probability >= 0 && var.destruction_probability <= 1
    error_message = "Destruction probability must be between 0.0 and 1.0."
  }
}

variable "chaos_window_start" {
  description = "Start time for chaos window (HH:MM format)"
  type        = string
  default     = "00:00"
}

variable "chaos_window_end" {
  description = "End time for chaos window (HH:MM format)"
  type        = string
  default     = "23:59"
}

variable "excluded_resources" {
  description = "List of resource names to exclude from chaos"
  type        = list(string)
  default     = []
}

variable "safe_mode" {
  description = "Run in safe mode (no actual destruction)"
  type        = bool
  default     = true
}

variable "log_level" {
  description = "Logging level (DEBUG, INFO, WARN, ERROR)"
  type        = string
  default     = "INFO"
  validation {
    condition     = contains(["DEBUG", "INFO", "WARN", "ERROR"], var.log_level)
    error_message = "Log level must be one of: DEBUG, INFO, WARN, ERROR."
  }
}

# Data sources to discover existing resources

data "aws_instances" "all" {
  filter {
    name   = "instance-state-name"
    values = ["running"]
  }
  count = var.enabled ? 1 : 0
}

# Random number generator for chaos selection
resource "random_integer" "chaos_seed" {
  count  = var.enabled ? 1 : 0
  min    = 0
  max    = 100
  result = random_integer.chaos_seed[0].result
}

# Chaos logic
locals {
  # Check if current time is within chaos window
  current_hour = format("%02d", timeadd(timestamp(), "0s").hour)
  current_minute = format("%02d", timeadd(timestamp(), "0s").minute)
  current_time = "${current_hour}:${current_minute}"
  
  chaos_window_active = (
    var.current_time >= var.chaos_window_start &&
    var.current_time <= var.chaos_window_end
  )
  
  # Convert probability to percentage for comparison
  destruction_threshold = floor(var.destruction_probability * 100)
  
  # Should we perform chaos?
  should_chaos = (
    var.enabled &&
    var.chaos_window_active &&
    var.chaos_seed.result <= var.destruction_threshold
  )
}

# Chaos events log
resource "null_resource" "chaos_log" {
  count = var.enabled ? 1 : 0
  
  triggers = {
    timestamp = timestamp()
    enabled   = var.enabled
    chaos_active = local.should_chaos
    probability  = var.destruction_probability
    resources_discovered = length(data.aws_instances.all[0].ids)
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      echo "[${timestamp()}] Chaos Monkey Status:" >> chaos_log.txt
      echo "  Enabled: ${var.enabled}" >> chaos_log.txt
      echo "  Chaos Window Active: ${local.chaos_window_active}" >> chaos_log.txt
      echo "  Destruction Probability: ${var.destruction_probability}" >> chaos_log.txt
      echo "  Should Perform Chaos: ${local.should_chaos}" >> chaos_log.txt
      echo "  Resources Discovered: ${length(data.aws_instances.all[0].ids)}" >> chaos_log.txt
      echo "" >> chaos_log.txt
    EOT
  }
}

# Resource destruction logic
resource "null_resource" "chaos_destruction" {
  count = var.enabled && local.should_chaos ? 1 : 0
  
  depends_on = [null_resource.chaos_log]
  
  provisioner "local-exec" {
    command = <<-EOT
      echo "[${timestamp()}] CHAOS EVENT: Selecting resource for destruction..." >> chaos_log.txt
      
      # Get list of resources
      resources=("${join(",", data.aws_instances.all[0].ids)}")
      
      # Filter out excluded resources
      available_resources=()
      for resource in "${resources[@]}"; do
        excluded=false
        for excluded_name in "${join(",", var.excluded_resources)}"; do
          if [[ "$resource" == *"$excluded_name"* ]]; then
            excluded=true
            break
          fi
        done
        if [ "$excluded" = false ]; then
          available_resources+=("$resource")
        fi
      done
      
      # Select random resource
      if [ ${#available_resources[@]} -gt 0 ]; then
        random_index=$((RANDOM % ${#available_resources[@]}))
        selected_resource="${available_resources[$random_index]}"
        
        echo "Selected resource for destruction: $selected_resource" >> chaos_log.txt
        
        if [ "${var.safe_mode}" = true ]; then
          echo "[SAFE MODE] Would destroy: $selected_resource" >> chaos_log.txt
        else
          echo "[DESTRUCTIVE MODE] Destroying: $selected_resource" >> chaos_log.txt
          aws ec2 terminate-instances --instance-ids "$selected_resource" --region "${data.aws_instances.all[0].region}" || true
        fi
      else
        echo "No available resources for destruction (all excluded)" >> chaos_log.txt
      fi
    EOT
  }
}

# Outputs
output "chaos_enabled" {
  description = "Whether chaos monkey is enabled"
  value       = var.enabled
}

output "chaos_window_active" {
  description = "Whether current time is within chaos window"
  value       = local.chaos_window_active
}

output "should_perform_chaos" {
  description = "Whether chaos should be performed this run"
  value       = local.should_chaos
}

output "resources_discovered" {
  description = "Number of resources discovered for potential chaos"
  value       = var.enabled ? length(data.aws_instances.all[0].ids) : 0
}

output "safe_mode" {
  description = "Whether running in safe mode (no actual destruction)"
  value       = var.safe_mode
}
