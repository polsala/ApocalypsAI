# Chaos schedule variable
variable "chaos_schedule" {
  description = "Cron schedule for chaos operations (e.g., '0 2 * * *')"
  type        = string
  default     = "0 2 * * *"
}

# Resource TTL variable
variable "resource_ttl" {
  description = "Time to live for created resources (e.g., '24h', '7d')"
  type        = string
  default     = "24h"
}

# Maximum resources variable
variable "max_resources" {
  description = "Maximum number of chaos resources to create"
  type        = number
  default     = 5
  validation {
    condition     = var.max_resources > 0 && var.max_resources <= 20
    error_message = "max_resources must be between 1 and 20."
  }
}

# Cloud providers variable
variable "providers" {
  description = "List of cloud providers to use for chaos testing"
  type        = list(string)
  default     = ["aws"]
}

# Enable chaos variable
variable "enable_chaos" {
  description = "Enable or disable chaos operations"
  type        = bool
  default     = true
}

# Resource types variable
variable "resource_types" {
  description = "Types of resources to create for chaos testing"
  type        = list(string)
  default     = ["instance", "bucket", "database"]
}
