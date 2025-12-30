# Environment configuration
variable "environment_name" {
  description = "Name of the environment (e.g., production, staging)"
  type        = string
  default     = "nightly"
}

variable "enabled" {
  description = "Enable chaos monkey functionality"
  type        = bool
  default     = false
}

variable "chaos_probability" {
  description = "Probability (0.0-1.0) of chaos per hour"
  type        = number
  default     = 0.01
  validation {
    condition     = var.chaos_probability >= 0 && var.chaos_probability <= 1
    error_message = "Chaos probability must be between 0 and 1."
  }
}

variable "target_resource_types" {
  description = "Resource types to target for chaos"
  type        = list(string)
  default     = ["aws_instance"]
}

variable "excluded_tags" {
  description = "Tags that exclude resources from chaos"
  type        = map(string)
  default     = {}
}

variable "safe_mode" {
  description = "Enable safety checks and confirmations"
  type        = bool
  default     = true
}

variable "time_window_start" {
  description = "Start hour for chaos (0-23)"
  type        = number
  default     = 9
  validation {
    condition     = var.time_window_start >= 0 && var.time_window_start <= 23
    error_message = "Time window start must be between 0 and 23."
  }
}

variable "time_window_end" {
  description = "End hour for chaos (0-23)"
  type        = number
  default     = 17
  validation {
    condition     = var.time_window_end >= 0 && var.time_window_end <= 23
    error_message = "Time window end must be between 0 and 23."
  }
}

variable "alarm_sns_topic_arn" {
  description = "SNS topic ARN for chaos event alarms"
  type        = string
  default     = ""
}

# Optional: VPC configuration for Lambda
variable "subnet_ids" {
  description = "Subnet IDs for Lambda VPC configuration"
  type        = list(string)
  default     = []
}

variable "security_group_ids" {
  description = "Security Group IDs for Lambda VPC configuration"
  type        = list(string)
  default     = []
}
