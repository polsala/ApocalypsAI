terraform {
  required_version = ">= 1.0"
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "random" {}

# Generate random resource names
generator "string" "resource_name" {
  length  = 16
  special = false
  upper   = false
}

# Chaos configuration variables
variable "chaos_schedule" {
  description = "Cron schedule for chaos operations"
  type        = string
  default     = "0 2 * * *"
}

variable "resource_ttl" {
  description = "Time to live for created resources"
  type        = string
  default     = "24h"
}

variable "max_resources" {
  description = "Maximum number of resources to create"
  type        = number
  default     = 5
}

variable "providers" {
  description = "List of cloud providers to use"
  type        = list(string)
  default     = ["aws"]
}

# Random resource selector
resource "random_integer" "resource_selector" {
  min = 1
  max = 3
}

# Create random resources based on selector
resource "random_pet" "chaos_resource" {
  count = var.max_resources
  
  # Only create if selector matches
  lifecycle {
    ignore_changes = [
      count
    ]
  }
}

# Output created resources
output "chaos_resources" {
  description = "List of created chaos resources"
  value       = random_pet.chaos_resource[*].id
}

output "chaos_schedule" {
  description = "Current chaos schedule"
  value       = var.chaos_schedule
}

output "resource_ttl" {
  description = "Resource time to live"
  value       = var.resource_ttl
}
