# Portal configuration
variable "portal_name" {
  description = "Base name for the void portal"
  type        = string
  default     = "void-portal"
}

variable "providers" {
  description = "List of cloud providers to track"
  type        = list(string)
  default     = ["aws", "gcp", "azure"]
  
  validation {
    condition     = length(var.providers) > 0
    error_message = "At least one provider must be specified."
  }
}

# Resource tracking
variable "track_resources" {
  description = "Enable resource tracking across providers"
  type        = bool
  default     = true
}

# Auto cleanup
variable "auto_cleanup_days" {
  description = "Number of days after which to automatically clean up resources (0 to disable)"
  type        = number
  default     = 30
  
  validation {
    condition     = var.auto_cleanup_days >= 0
    error_message = "Auto cleanup days must be 0 or greater."
  }
}

# Advanced settings
variable "enable_debug" {
  description = "Enable debug output"
  type        = bool
  default     = false
}

variable "portal_severity" {
  description = "Severity level for portal monitoring"
  type        = string
  default     = "info"
  
  validation {
    condition     = contains(["debug", "info", "warn", "error"], var.portal_severity)
    error_message = "Portal severity must be one of: debug, info, warn, error."
  }
}
