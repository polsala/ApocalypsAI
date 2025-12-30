# Enable/disable chaos monkey
variable "enabled" {
  description = "Enable/disable chaos monkey"
  type        = bool
  default     = false
}

# Probability of destroying a resource
variable "destruction_probability" {
  description = "Probability (0.0-1.0) of destroying a resource"
  type        = number
  default     = 0.05
  validation {
    condition     = var.destruction_probability >= 0 && var.destruction_probability <= 1
    error_message = "Destruction probability must be between 0.0 and 1.0."
  }
}

# Chaos window configuration
variable "chaos_window_start" {
  description = "Start time for chaos window (HH:MM format)"
  type        = string
  default     = "00:00"
  validation {
    condition     = can(regex("^([01]?[0-9]|2[0-3]):[0-5][0-9]$", var.chaos_window_start))
    error_message = "Chaos window start must be in HH:MM format (24-hour)."
  }
}

variable "chaos_window_end" {
  description = "End time for chaos window (HH:MM format)"
  type        = string
  default     = "23:59"
  validation {
    condition     = can(regex("^([01]?[0-9]|2[0-3]):[0-5][0-9]$", var.chaos_window_end))
    error_message = "Chaos window end must be in HH:MM format (24-hour)."
  }
}

# Resource exclusion list
variable "excluded_resources" {
  description = "List of resource names to exclude from chaos"
  type        = list(string)
  default     = []
}

# Safety and logging
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

# Provider-specific configurations
variable "aws_region" {
  description = "AWS region for resource discovery"
  type        = string
  default     = "us-east-1"
}

variable "gcp_project" {
  description = "GCP project for resource discovery"
  type        = string
  default     = ""
}

variable "azure_subscription_id" {
  description = "Azure subscription ID for resource discovery"
  type        = string
  default     = ""
}

# Advanced configuration
variable "max_resources_per_run" {
  description = "Maximum number of resources to destroy per chaos run"
  type        = number
  default     = 1
  validation {
    condition     = var.max_resources_per_run >= 0
    error_message = "Max resources per run must be non-negative."
  }
}

variable "chaos_cooldown_minutes" {
  description = "Minimum time between chaos events (in minutes)"
  type        = number
  default     = 60
  validation {
    condition     = var.chaos_cooldown_minutes >= 0
    error_message = "Chaos cooldown must be non-negative."
  }
}

variable "resource_types" {
  description = "List of resource types to include in chaos (empty means all)"
  type        = list(string)
  default     = []
}
