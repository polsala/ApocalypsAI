# General configuration
variable "prefix" {
  description = "Prefix for all resources"
  type        = string
  default     = "nightly-chaos"
}

variable "enabled" {
  description = "Enable the Chaos Monkey"
  type        = bool
  default     = false
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# Chaos configuration
variable "chaos_schedule" {
  description = "Cron schedule for chaos events (AWS CloudWatch Events format)"
  type        = string
  default     = "0 2 * * *"  # Daily at 2 AM
}

variable "chaos_intensity" {
  description = "Percentage of unprotected resources to terminate (0-100)"
  type        = number
  default     = 5
  validation {
    condition     = var.chaos_intensity >= 0 && var.chaos_intensity <= 100
    error_message = "Chaos intensity must be between 0 and 100."
  }
}

variable "target_resources" {
  description = "List of resource types to target for chaos"
  type        = list(string)
  default     = ["aws_instance", "aws_rds_instance", "aws_ecs_service"]
}

variable "safe_mode" {
  description = "Enable safe mode (only log actions without actually terminating resources)"
  type        = bool
  default     = true
}

variable "excluded_tags" {
  description = "List of tag values that exclude resources from chaos"
  type        = list(string)
  default     = ["critical", "production-critical", "do-not-terminate"]
}

variable "log_retention_days" {
  description = "Number of days to retain CloudWatch logs"
  type        = number
  default     = 7
  validation {
    condition     = var.log_retention_days in [1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653]
    error_message = "Log retention days must be one of: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653."
  }
}

# Resource limits
variable "max_terminations_per_run" {
  description = "Maximum number of resources to terminate per chaos run"
  type        = number
  default     = 10
}

variable "min_time_between_runs" {
  description = "Minimum time in hours between chaos runs"
  type        = number
  default     = 1
}

# Notification configuration
variable "notification_emails" {
  description = "List of email addresses to notify about chaos events"
  type        = list(string)
  default     = []
}

variable "enable_notifications" {
  description = "Enable SNS notifications for chaos events"
  type        = bool
  default     = true
}

# Advanced configuration
variable "chaos_window_start" {
  description = "Start hour for chaos window (0-23)"
  type        = number
  default     = 2
  validation {
    condition     = var.chaos_window_start >= 0 && var.chaos_window_start <= 23
    error_message = "Chaos window start must be between 0 and 23."
  }
}

variable "chaos_window_end" {
  description = "End hour for chaos window (0-23)"
  type        = number
  default     = 6
  validation {
    condition     = var.chaos_window_end >= 0 && var.chaos_window_end <= 23
    error_message = "Chaos window end must be between 0 and 23."
  }
}

variable "enable_metrics" {
  description = "Enable CloudWatch metrics and dashboard"
  type        = bool
  default     = true
}

variable "enable_alarm" {
  description = "Enable CloudWatch alarm for failed executions"
  type        = bool
  default     = true
}

variable "custom_chaos_script" {
  description = "Custom Python script for chaos logic (overrides default)"
  type        = string
  default     = ""
}

variable "dry_run_only" {
  description = "Only perform dry runs (never actually terminate resources)"
  type        = bool
  default     = true
}

variable "chaos_tags" {
  description = "Tags to add to chaos events for tracking"
  type        = map(string)
  default     = {
    "chaos-monkey" = "enabled"
    "managed-by"   = "terraform"
  }
}

variable "excluded_resource_ids" {
  description = "List of specific resource IDs to exclude from chaos"
  type        = list(string)
  default     = []
}

variable "chaos_duration_minutes" {
  description = "Maximum duration in minutes for chaos execution"
  type        = number
  default     = 30
  validation {
    condition     = var.chaos_duration_minutes > 0 && var.chaos_duration_minutes <= 1440
    error_message = "Chaos duration must be between 1 and 1440 minutes."
  }
}
