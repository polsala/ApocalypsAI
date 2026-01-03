# Chaos Monkey Module Variables

variable "chaos_enabled" {
  description = "Enable/disable chaos engineering"
  type        = bool
  default     = false
}

variable "chaos_interval_hours" {
  description = "Hours between chaos runs"
  type        = number
  default     = 1
}

variable "max_resources_per_run" {
  description = "Maximum resources to terminate per run"
  type        = number
  default     = 1
}

variable "target_resource_types" {
  description = "Resource types to target for chaos"
  type        = list(string)
  default     = []
}

variable "excluded_resources" {
  description = "Resource names to exclude from chaos"
  type        = list(string)
  default     = []
}

variable "dry_run" {
  description = "Only log what would be destroyed, don't actually destroy"
  type        = bool
  default     = true
}

variable "aws_region" {
  description = "AWS region for chaos operations"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment tag for resource filtering"
  type        = string
  default     = "test"
}

variable "chaos_retention_days" {
  description = "Log retention days for chaos events"
  type        = number
  default     = 30
}
