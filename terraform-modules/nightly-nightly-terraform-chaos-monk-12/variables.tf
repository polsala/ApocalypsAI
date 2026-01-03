# Chaos Engineering Configuration

variable "chaos_enabled" {
  description = "Enable/disable chaos engineering"
  type        = bool
  default     = false
  validation {
    condition     = can(var.chaos_enabled)
    error_message = "Chaos enabled must be a boolean value."
  }
}

variable "chaos_interval_hours" {
  description = "Hours between chaos runs"
  type        = number
  default     = 1
  validation {
    condition     = var.chaos_interval_hours >= 0 && var.chaos_interval_hours <= 168
    error_message = "Chaos interval must be between 0 and 168 hours (1 week)."
  }
}

variable "max_resources_per_run" {
  description = "Maximum resources to terminate per run"
  type        = number
  default     = 1
  validation {
    condition     = var.max_resources_per_run >= 1 && var.max_resources_per_run <= 10
    error_message = "Max resources per run must be between 1 and 10."
  }
}

variable "target_resource_types" {
  description = "Resource types to target for chaos"
  type        = list(string)
  default     = []
  validation {
    condition     = length(var.target_resource_types) <= 20
    error_message = "Too many target resource types specified. Limit to 20 or fewer."
  }
}

variable "excluded_resources" {
  description = "Resource names to exclude from chaos"
  type        = list(string)
  default     = []
  validation {
    condition     = length(var.excluded_resources) <= 50
    error_message = "Too many excluded resources. Limit to 50 or fewer."
  }
}

variable "dry_run" {
  description = "Only log what would be destroyed, don't actually destroy"
  type        = bool
  default     = true
  validation {
    condition     = can(var.dry_run)
    error_message = "Dry run must be a boolean value."
  }
}

variable "aws_region" {
  description = "AWS region for chaos operations"
  type        = string
  default     = "us-east-1"
  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-[0-9]$", var.aws_region))
    error_message = "Invalid AWS region format."
  }
}

variable "environment" {
  description = "Environment tag for resource filtering"
  type        = string
  default     = "test"
  validation {
    condition     = contains(["test", "staging", "chaos"], var.environment)
    error_message = "Environment must be test, staging, or chaos for safety."
  }
}

variable "max_chaos_duration_minutes" {
  description = "Maximum duration for chaos execution in minutes"
  type        = number
  default     = 30
  validation {
    condition     = var.max_chaos_duration_minutes >= 1 && var.max_chaos_duration_minutes <= 1440
    error_message = "Max chaos duration must be between 1 minute and 24 hours."
  }
}

variable "chaos_schedule_cron" {
  description = "Cron expression for chaos execution schedule"
  type        = string
  default     = "0 2 * * *" # Daily at 2 AM
  validation {
    condition     = can(regex("^([0-9]|0[0-9]|1[0-9]|2[0-3]|\*) ?([0-9]|0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|\*) ?(\*|[1-9]|0[1-9]|[12][0-9]|3[01]) ?(\*|[1-9]|0[1-9]|1[0-2]) ?(\*|[0-7])$", var.chaos_schedule_cron))
    error_message = "Invalid cron expression format."
  }
}

variable "enable_chaos_metrics" {
  description = "Enable CloudWatch metrics for chaos events"
  type        = bool
  default     = true
}

variable "chaos_notification_topic" {
  description = "SNS topic ARN for chaos notifications"
  type        = string
  default     = ""
  validation {
    condition     = var.chaos_notification_topic == "" || can(regex("^arn:aws:sns:[a-z0-9-]+:[0-9]{12}:[a-zA-Z0-9-_]+$", var.chaos_notification_topic))
    error_message = "Invalid SNS topic ARN format."
  }
}

variable "chaos_retention_days" {
  description = "Log retention days for chaos events"
  type        = number
  default     = 30
  validation {
    condition     = var.chaos_retention_days >= 1 && var.chaos_retention_days <= 2557
    error_message = "Log retention must be between 1 day and 7 years."
  }
}
