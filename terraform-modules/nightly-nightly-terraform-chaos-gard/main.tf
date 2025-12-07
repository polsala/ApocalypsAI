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
variable "chaos_level" {
  description = "Scale of chaos from 0 (no chaos) to 10 (maximum chaos)"
  type        = number
  default     = 0
  validation {
    condition     = var.chaos_level >= 0 && var.chaos_level <= 10
    error_message = "Chaos level must be between 0 and 10."
  }
}

variable "protected_resources" {
  description = "List of resource names to protect from chaos events"
  type        = list(string)
  default     = []
}

variable "chaos_schedule" {
  description = "Cron schedule for when chaos events can occur (optional)"
  type        = string
  default     = ""
}

variable "enabled" {
  description = "Enable or disable the chaos garden entirely"
  type        = bool
  default     = true
}

# Random resources for chaos events
resource "random_integer" "chaos_seed" {
  min = 1
  max = 1000000
}

resource "random_integer" "chaos_event_type" {
  count = var.enabled && var.chaos_level > 0 ? 1 : 0
  min   = 1
  max   = 8
}

resource "random_integer" "chaos_duration" {
  count = var.enabled && var.chaos_level > 0 ? 1 : 0
  min   = 60
  max   = 3600  # 1 minute to 1 hour
}

resource "random_integer" "chaos_target" {
  count = var.enabled && var.chaos_level > 0 ? 1 : 0
  min   = 1
  max   = 100
}

# Chaos event data
locals {
  chaos_events = {
    1 = "Network Latency"
    2 = "CPU Spike"
    3 = "Memory Pressure"
    4 = "Disk I/O Slowdown"
    5 = "Cosmic Ray Strike"
    6 = "Quantum Entanglement"
    7 = "Solar Flare"
    8 = "Meteor Shower"
  }
  
  chaos_severity = {
    for i in range(1, 11) : i => {
      1 = "Minor"
      2 = "Minor"
      3 = "Moderate"
      4 = "Moderate"
      5 = "Moderate"
      6 = "Severe"
      7 = "Severe"
      8 = "Severe"
      9 = "Critical"
      10 = "Critical"
    }[i]
  }
  
  chaos_enabled = var.enabled && var.chaos_level > 0
}

# Output chaos configuration
output "chaos_status" {
  value = local.chaos_enabled ? "Chaos Garden is ACTIVE (Level ${var.chaos_level})" : "Chaos Garden is DISABLED"
}

output "chaos_event" {
  value     = local.chaos_enabled ? local.chaos_events[random_integer.chaos_event_type[0].result] : "No event"
  sensitive = true
}

output "chaos_duration_seconds" {
  value     = local.chaos_enabled ? random_integer.chaos_duration[0].result : 0
  sensitive = true
}

output "chaos_severity" {
  value = local.chaos_enabled ? local.chaos_severity[var.chaos_level] : "None"
}

output "protected_resources" {
  value = var.protected_resources
}

# Null resource to trigger chaos events (for demonstration)
resource "null_resource" "chaos_trigger" {
  count = local.chaos_enabled ? 1 : 0
  
  triggers = {
    seed        = random_integer.chaos_seed.result
    event_type  = random_integer.chaos_event_type[0].result
    duration    = random_integer.chaos_duration[0].result
    target      = random_integer.chaos_target[0].result
  }
  
  provisioner "local-exec" {
    when    = destroy
    command = "echo 'Chaos event ${local.chaos_events[random_integer.chaos_event_type[0].result]} completed after ${random_integer.chaos_duration[0].result} seconds'"
  }
}

# Data source to check if chaos is scheduled
data "external" "chaos_schedule_check" {
  count = var.chaos_schedule != "" ? 1 : 0
  program = ["python3", "-c", <<-EOT
    import sys, json, datetime
    schedule = "${var.chaos_schedule}"
    # Simple check: if schedule contains current hour, allow chaos
    now = datetime.datetime.now()
    # This is a simplified implementation
    result = {"allowed": True, "current_time": now.isoformat()}
    print(json.dumps(result))
  EOT
  ]
}

# Warning if chaos is enabled in production-like environments
locals {
  environment_warning = local.chaos_enabled && contains(["prod", "production"], lower(var.chaos_schedule)) ? "WARNING: Chaos enabled in production environment!" : ""
}

output "environment_warning" {
  value = local.environment_warning
  sensitive = true
}
