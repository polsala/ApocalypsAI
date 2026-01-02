terraform {
  required_version = ">= 1.0"
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

provider "random" {}

# Input variables
variable "enabled" {
  description = "Enable chaos monkey functionality"
  type        = bool
  default     = false
}

variable "destruction_probability" {
  description = "Probability (0.0-1.0) of destroying a resource"
  type        = number
  default     = 0.05
  validation {
    condition     = var.destruction_probability >= 0 && var.destruction_probability <= 1
    error_message = "Destruction probability must be between 0 and 1."
  }
}

variable "target_resources" {
  description = "List of resource types to target for chaos"
  type        = list(string)
  default     = []
}

variable "excluded_resources" {
  description = "List of specific resources to exclude from chaos"
  type        = list(string)
  default     = []
}

variable "max_destructions_per_run" {
  description = "Maximum number of resources to destroy per run"
  type        = number
  default     = 3
}

# Local values for chaos logic
locals {
  # Get current timestamp for chaos events
  chaos_timestamp = formatdate("YYYY-MM-DD HH:mm:ss", timestamp())
  
  # Generate random number for chaos decision
  chaos_seed = random_id.chaos_seed.hex
  
  # Filter resources based on target types and exclusions
  eligible_resources = [
    for resource in data.terraform_state.current.values
    if can(regex("^(aws_|azure_|google_|azurerm_|google_|kubernetes_)", resource.type)) &&
       contains(var.target_resources, resource.type) &&
       !contains(var.excluded_resources, "${resource.type}.${resource.name}")
  ]
}

# Random ID for seeding chaos decisions
resource "random_id" "chaos_seed" {
  byte_length = 8
}

# Data source to read current Terraform state
# Note: This requires the terraform state to be accessible
# In practice, you might want to use terraform_remote_state
# or read from a state file

data "terraform_state" "current" {
  # This is a placeholder - in real usage, you'd configure
  # this to read from your actual state backend
  # For example, using terraform_remote_state:
  # backend = "s3"
  # config = {
  #   bucket = "my-terraform-state"
  #   key    = "path/to/state.tfstate"
  #   region = "us-east-1"
  # }
  
  # For demonstration, we'll create mock resources
  # In a real implementation, this would read from actual state
}

# Mock resources for demonstration (remove in real implementation)
resource "random_pet" "mock_resource" {
  count = var.enabled ? 5 : 0
  
  # This creates mock resources that the chaos monkey can target
  # In a real implementation, you'd have actual cloud resources here
}

# Chaos logic - destroy resources randomly
resource "null_resource" "chaos_destruction" {
  count = var.enabled && length(local.eligible_resources) > 0 ? var.max_destructions_per_run : 0
  
  # Randomly decide whether to destroy this resource
  triggers = {
    should_destroy = random_integer.chaos_decision[count.index].result < (var.destruction_probability * 100)
    resource_id    = local.eligible_resources[count.index].id
    timestamp      = local.chaos_timestamp
  }
  
  provisioner "local-exec" {
    when    = destroy
    command = "echo \"CHAOS MONKEY: Destroying resource ${self.triggers.resource_id} at ${self.triggers.timestamp}\""
  }
  
  provisioner "local-exec" {
    when    = create
    command = "echo \"CHAOS MONKEY: Resource ${self.triggers.resource_id} survived chaos at ${self.triggers.timestamp}\""
  }
}

# Random integer for chaos decisions
resource "random_integer" "chaos_decision" {
  count   = var.max_destructions_per_run
  min     = 0
  max     = 100
  seed    = "${local.chaos_seed}-${count.index}"
}

# Chaos report output
output "chaos_report" {
  description = "Report of chaos monkey activity"
  value = {
    enabled                    = var.enabled
    destruction_probability    = var.destruction_probability
    max_destructions_per_run = var.max_destructions_per_run
    eligible_resource_count  = length(local.eligible_resources)
    chaos_timestamp          = local.chaos_timestamp
    chaos_seed               = local.chaos_seed
    
    # Note: In a real implementation, you'd track actual destroyed resources
    # This is a simplified example
    destroyed_resources = var.enabled ? [
      for i in range(var.max_destructions_per_run) :
      if random_integer.chaos_decision[i].result < (var.destruction_probability * 100)
    ] : []
  }
  
  sensitive = false
}

# Safety warning output
output "chaos_warning" {
  description = "Safety warning about chaos monkey usage"
  value       = var.enabled ? "⚠️ CHAOS MONKEY IS ENABLED - RESOURCES MAY BE DESTROYED" : "✅ Chaos monkey is disabled"
  
  # Only show warning when enabled
  sensitive = var.enabled
}

# Resource inventory output
output "targetable_resources" {
  description = "Resources that could be targeted by chaos monkey"
  value       = local.eligible_resources
  
  # Only show when chaos is enabled for safety
  sensitive = !var.enabled
}
