# Configuration variables for Chaos Monkey module

variable "chaos_enabled" {
  description = "Enable/disable chaos mode"
  type        = bool
  default     = false
  validation {
    condition     = can(var.chaos_enabled)
    error_message = "chaos_enabled must be a boolean value."
  }
}

variable "chaos_probability" {
  description = "Probability (0-1) of destroying a resource"
  type        = number
  default     = 0.05
  validation {
    condition     = var.chaos_probability >= 0 && var.chaos_probability <= 1
    error_message = "chaos_probability must be between 0 and 1."
  }
}

variable "chaos_schedule" {
  description = "Cron schedule for chaos execution"
  type        = string
  default     = "0 3 * * *"
  validation {
    condition     = can(regex("^([0-9]|1[0-9]|2[0-3]|[0-9]-[0-9]|[0-9]/[0-9]|\*) ([0-9]|[1-2][0-9]|3[0-1]|[0-9]-[0-9]|[0-9]/[0-9]|\*) ([0-9]|1[0-2]|[0-9]-[0-9]|[0-9]/[0-9]|\*) ([0-6]|[0-6]-[0-6]|[0-6]/[0-6]|\*) ([0-9]|[1-2][0-9]|3[0-1]|[0-9]-[0-9]|[0-9]/[0-9]|\*)$", var.chaos_schedule))
    error_message = "chaos_schedule must be a valid cron expression."
  }
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
  validation {
    condition     = can(var.dry_run)
    error_message = "dry_run must be a boolean value."
  }
}

variable "log_level" {
  description = "Logging verbosity level"
  type        = string
  default     = "INFO"
  validation {
    condition     = contains(["DEBUG", "INFO", "WARN", "ERROR"], var.log_level)
    error_message = "log_level must be one of: DEBUG, INFO, WARN, ERROR."
  }
}

# Input validation for safety
validation "chaos_safety_check" {
  condition     = var.chaos_enabled == false || var.dry_run == true
  error_message = "Chaos mode is enabled without dry-run mode. This will destroy real resources! Set dry_run = true for safety."
}

# Additional safety validations
validation "probability_warning" {
  condition     = var.chaos_probability <= 0.5
  error_message = "Chaos probability is very high (${var.chaos_probability}). Consider lowering it to avoid excessive resource destruction."
  # Note: This is a warning, not an error, so we don't prevent execution
}

validation "excluded_resources_check" {
  condition     = length(var.excluded_resources) > 0
  error_message = "No excluded resources specified. Consider adding critical resources to excluded_resources to prevent accidental destruction."
  # Note: This is a warning for now
}
