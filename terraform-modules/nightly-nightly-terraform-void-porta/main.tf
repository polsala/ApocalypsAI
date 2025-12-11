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

# Generate a unique portal identifier
resource "random_id" "portal_id" {
  byte_length = 16
}

# Create the void portal resource
resource "random_pet" "void_portal" {
  prefix    = "void"
  separator = "-"
}

# Generate a whimsical portal name
resource "random_string" "portal_name" {
  length  = 8
  upper   = false
  special = false
  number  = false
}

# Create resource inventory map
locals {
  supported_providers = var.providers
  
  resource_inventory = {
    for provider in var.providers :
    provider => {
      count        = 0
      last_updated = timestamp()
      resources    = []
    }
  }
}

# Create cleanup schedule if enabled
resource "random_integer" "cleanup_hour" {
  count  = var.auto_cleanup_days > 0 ? 1 : 0
  min    = 0
  max    = 23
}

resource "random_integer" "cleanup_minute" {
  count  = var.auto_cleanup_days > 0 ? 1 : 0
  min    = 0
  max    = 59
}

# Output the cleanup schedule
locals {
  cleanup_cron = var.auto_cleanup_days > 0 ? "${random_integer.cleanup_minute[0].result} ${random_integer.cleanup_hour[0].result} */${var.auto_cleanup_days} * *" : "disabled"
}

# Track resource changes
resource "null_resource" "resource_tracker" {
  count = var.track_resources ? 1 : 0
  
  triggers = {
    portal_id     = random_id.portal_id.hex
    last_updated  = timestamp()
    tracked_count = length(keys(local.resource_inventory))
  }
}

# Output portal information
output "portal_id" {
  description = "Unique identifier for the void portal"
  value       = random_id.portal_id.hex
}

output "portal_name" {
  description = "Whimsical name for the void portal"
  value       = "${var.portal_name}-${random_pet.void_portal.id}-${random_string.portal_name.result}"
}

output "tracked_resources" {
  description = "Inventory of tracked resources across providers"
  value       = local.resource_inventory
}

output "cleanup_schedule" {
  description = "Cron expression for automatic resource cleanup"
  value       = local.cleanup_cron
}

output "portal_status" {
  description = "Current status of the void portal"
  value = {
    active          = true
    providers_count = length(var.providers)
    tracking_enabled = var.track_resources
    auto_cleanup    = var.auto_cleanup_days > 0 ? "enabled" : "disabled"
    portal_type     = "whimsical"
  }
}
