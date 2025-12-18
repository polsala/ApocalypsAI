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

variable "enabled" {
  description = "Enable chaos monkey"
  type        = bool
  default     = false
}

variable "intensity" {
  description = "Probability (0-1) of destroying each resource"
  type        = number
  default     = 0.1
}

variable "resources" {
  description = "List of resource IDs to potentially destroy"
  type        = list(string)
  default     = []
}

variable "safe_mode" {
  description = "When true, only logs actions without destroying resources"
  type        = bool
  default     = true
}

resource "random_integer" "chaos_selector" {
  count  = var.enabled ? length(var.resources) : 0
  min    = 0
  max    = 100
  result = var.intensity * 100
}

resource "null_resource" "chaos_action" {
  count = var.enabled ? length(var.resources) : 0
  
  triggers = {
    resource_id = var.resources[count.index]
    should_destroy = (
      var.safe_mode ? false : (
        random_integer.chaos_selector[count.index].result < var.intensity * 100
      )
    )
  }
  
  provisioner "local-exec" {
    when    = destroy
    command = var.safe_mode ? "echo [SAFE MODE] Would destroy ${self.triggers.resource_id}" : "echo [CHAOS] Destroying ${self.triggers.resource_id}"
  }
  
  provisioner "local-exec" {
    when    = create
    command = var.safe_mode ? "echo [SAFE MODE] Would recreate ${self.triggers.resource_id}" : "echo [CHAOS] Recreating ${self.triggers.resource_id}"
  }
}

output "chaos_summary" {
  description = "Summary of chaos actions"
  value = {
    enabled     = var.enabled
    intensity   = var.intensity
    safe_mode   = var.safe_mode
    resources   = var.resources
    chaos_count = var.enabled ? length(var.resources) : 0
  }
}
