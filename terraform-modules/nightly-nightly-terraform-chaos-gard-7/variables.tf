# AWS Region
variable "aws_region" {
  description = "AWS region for the chaos garden"
  type        = string
  default     = "us-east-1"
}

# Environment name for tagging
variable "environment" {
  description = "Environment name for tagging resources"
  type        = string
  default     = "staging"
}

# Chaos duration
variable "chaos_duration" {
  description = "How long chaos runs (e.g., 30m, 1h, 2h30m)"
  type        = string
  default     = "30m"
}

# Network chaos settings
variable "enable_network_chaos" {
  description = "Enable network latency chaos"
  type        = bool
  default     = true
}

variable "network_latency_ms" {
  description = "Network latency in milliseconds"
  type        = number
  default     = 200
}

# CPU chaos settings
variable "enable_cpu_chaos" {
  description = "Enable CPU stress chaos"
  type        = bool
  default     = true
}

variable "cpu_stress_duration" {
  description = "CPU stress duration (e.g., 10m, 30m)"
  type        = string
  default     = "10m"
}

# Random failure settings
variable "enable_random_failures" {
  description = "Enable random task failures"
  type        = bool
  default     = true
}

variable "failure_rate" {
  description = "Probability of random failures (0.0-1.0)"
  type        = number
  default     = 0.1
  validation {
    condition     = var.failure_rate >= 0 && var.failure_rate <= 1
    error_message = "Failure rate must be between 0.0 and 1.0."
  }
}

# Whimsy settings
variable "whimsy_level" {
  description = "Whimsy level: 'low', 'medium', 'high'"
  type        = string
  default     = "high"
  validation {
    condition     = contains(["low", "medium", "high"], var.whimsy_level)
    error_message = "Whimsy level must be 'low', 'medium', or 'high'."
  }
}

variable "chaos_garden_name" {
  description = "Name for your chaos garden"
  type        = string
  default     = "TheWhimsicalWasteland"
}

# ECS task settings
variable "task_cpu" {
  description = "CPU units for the ECS task"
  type        = number
  default     = 256
}

variable "task_memory" {
  description = "Memory for the ECS task (in MiB)"
  type        = number
  default     = 512
}

variable "chaos_task_count" {
  description = "Number of chaos tasks to run"
  type        = number
  default     = 1
}

# Container image
variable "chaos_container_image" {
  description = "Docker image for chaos container"
  type        = string
  default     = "gaiaadm/pumba:latest"
}

# Networking
variable "subnet_ids" {
  description = "List of subnet IDs for the ECS service"
  type        = list(string)
  default     = []
}

variable "security_group_ids" {
  description = "List of security group IDs for the ECS service"
  type        = list(string)
  default     = []
}

# Logging
variable "log_retention_days" {
  description = "Number of days to retain logs in CloudWatch"
  type        = number
  default     = 7
}

# Chaos scenarios
variable "chaos_scenarios" {
  description = "List of chaos scenarios to enable"
  type        = list(string)
  default     = ["network", "cpu", "random_failures"]
}

# Enable/disable specific chaos types
variable "enable_disk_chaos" {
  description = "Enable disk I/O chaos"
  type        = bool
  default     = false
}

variable "enable_memory_chaos" {
  description = "Enable memory stress chaos"
  type        = bool
  default     = false
}

variable "enable_time_chaos" {
  description = "Enable time manipulation chaos"
  type        = bool
  default     = false
}

# Advanced settings
variable "chaos_schedule_expression" {
  description = "CloudWatch Events schedule expression for chaos runs"
  type        = string
  default     = "rate(1 hour)"
}

variable "chaos_alarm_threshold" {
  description = "CPU utilization threshold for chaos failure alarms"
  type        = number
  default     = 90
}

variable "chaos_alarm_evaluation_periods" {
  description = "Number of evaluation periods for chaos alarms"
  type        = number
  default     = 2
}

# Tags
variable "additional_tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}

# Cost controls
variable "max_chaos_duration" {
  description = "Maximum allowed chaos duration to prevent runaway costs"
  type        = string
  default     = "4h"
  validation {
    condition     = can(regex("^\d+[hms]?$", var.max_chaos_duration))
    error_message = "Max chaos duration must be a valid duration (e.g., 1h, 30m, 2h30m)."
  }
}

# Notification settings
variable "notification_emails" {
  description = "List of email addresses for chaos notifications"
  type        = list(string)
  default     = []
}

variable "enable_slack_notifications" {
  description = "Enable Slack notifications for chaos events"
  type        = bool
  default     = false
}

variable "slack_webhook_url" {
  description = "Slack webhook URL for notifications"
  type        = string
  default     = ""
  sensitive   = true
}
