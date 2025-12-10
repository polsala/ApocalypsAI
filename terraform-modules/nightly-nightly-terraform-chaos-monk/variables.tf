# Enable/disable chaos monkey
variable "enable_chaos" {
  description = "Enable chaos monkey execution"
  type        = bool
  default     = false
  validation {
    condition     = can(regex("^(true|false)$", tostring(var.enable_chaos)))
    error_message = "enable_chaos must be true or false."
  }
}

# Chaos probability (0.0 to 1.0)
variable "chaos_probability" {
  description = "Probability of chaos event (0.0 to 1.0)"
  type        = number
  default     = 0.1
  validation {
    condition     = var.chaos_probability >= 0 && var.chaos_probability <= 1
    error_message = "chaos_probability must be between 0.0 and 1.0."
  }
}

# AWS region
variable "aws_region" {
  description = "AWS region for chaos operations"
  type        = string
  default     = "us-east-1"
  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-\d+$", var.aws_region))
    error_message = "aws_region must be a valid AWS region format."
  }
}

# Target environment
variable "target_environment" {
  description = "Environment tag to target for chaos"
  type        = string
  default     = "staging"
}

# Exclusion tag key
variable "exclusion_tag_key" {
  description = "Tag key to exclude from chaos"
  type        = string
  default     = "Environment"
}

# Exclusion tag value
variable "exclusion_tag_value" {
  description = "Tag value to exclude from chaos"
  type        = string
  default     = "production"
}

# Target resource types
variable "target_resource_types" {
  description = "List of resource types to target for chaos"
  type        = list(string)
  default     = ["aws_instance"]
}

# Chaos window start hour
variable "chaos_window_start" {
  description = "Start hour for chaos window (0-23)"
  type        = number
  default     = 9
  validation {
    condition     = var.chaos_window_start >= 0 && var.chaos_window_start <= 23
    error_message = "chaos_window_start must be between 0 and 23."
  }
}

# Chaos window end hour
variable "chaos_window_end" {
  description = "End hour for chaos window (0-23)"
  type        = number
  default     = 17
  validation {
    condition     = var.chaos_window_end >= 0 && var.chaos_window_end <= 23
    error_message = "chaos_window_end must be between 0 and 23."
  }
}

# Maximum resources to terminate per execution
variable "max_resources_per_execution" {
  description = "Maximum number of resources to terminate per execution"
  type        = number
  default     = 1
  validation {
    condition     = var.max_resources_per_execution >= 0
    error_message = "max_resources_per_execution must be a non-negative number."
  }
}
