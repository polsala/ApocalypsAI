# Chaos Level Configuration
variable "chaos_level" {
  description = "Scale of chaos from 0 (no chaos) to 10 (maximum chaos)"
  type        = number
  default     = 0
  validation {
    condition     = var.chaos_level >= 0 && var.chaos_level <= 10
    error_message = "Chaos level must be between 0 and 10."
  }
}

# Protected Resources
variable "protected_resources" {
  description = "List of resource names to protect from chaos events"
  type        = list(string)
  default     = []
}

# Chaos Schedule
variable "chaos_schedule" {
  description = "Cron schedule for when chaos events can occur (optional)"
  type        = string
  default     = ""
}

# Enable/Disable
variable "enabled" {
  description = "Enable or disable the chaos garden entirely"
  type        = bool
  default     = true
}

# Provider Configuration
variable "provider_type" {
  description = "Cloud provider type (aws, gcp, azure, etc.)"
  type        = string
  default     = "aws"
}

# Resource Tags
variable "resource_tags" {
  description = "Tags to apply to chaos-related resources"
  type        = map(string)
  default     = {}
}
