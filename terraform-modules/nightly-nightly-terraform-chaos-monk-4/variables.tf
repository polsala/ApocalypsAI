# Chaos Level Configuration
variable "chaos_level" {
  description = "Level of chaos to introduce (gentle, medium, extreme)"
  type        = string
  default     = "medium"
  validation {
    condition     = contains(["gentle", "medium", "extreme"], var.chaos_level)
    error_message = "Chaos level must be one of: gentle, medium, extreme."
  }
}

# Enable/Disable Chaos Monkey
variable "enabled" {
  description = "Whether chaos monkey is enabled"
  type        = bool
  default     = true
}

# Target Resources
variable "target_instances" {
  description = "List of EC2 instance IDs to target for chaos"
  type        = list(string)
  default     = []
}

variable "target_services" {
  description = "List of service names to target for chaos"
  type        = list(string)
  default     = []
}

variable "target_databases" {
  description = "List of database instance IDs to target for chaos"
  type        = list(string)
  default     = []
}

# Safety Configuration
variable "minimum_instance_count" {
  description = "Minimum number of instances to keep running"
  type        = number
  default     = 1
}

variable "maintenance_windows" {
  description = "List of cron expressions for maintenance windows when chaos is disabled"
  type        = list(string)
  default     = []
}

variable "circuit_breaker_threshold" {
  description = "Number of consecutive failures before disabling chaos"
  type        = number
  default     = 3
}

# Scheduling
variable "chaos_schedule" {
  description = "Cron expression for when chaos can occur"
  type        = string
  default     = "cron(0/30 * * * ? *)" # Every 30 minutes
}

variable "chaos_duration" {
  description = "How long chaos events last (in minutes)"
  type        = number
  default     = 5
}

# Mode Configuration
variable "dry_run" {
  description = "Enable dry run mode (no actual disruption)"
  type        = bool
  default     = false
}

variable "verbose_logging" {
  description = "Enable verbose logging for debugging"
  type        = bool
  default     = false
}

# Cloud Provider Configuration
variable "cloud_provider" {
  description = "Cloud provider (aws, azure, gcp)"
  type        = string
  default     = "aws"
  validation {
    condition     = contains(["aws", "azure", "gcp"], var.cloud_provider)
    error_message = "Cloud provider must be one of: aws, azure, gcp."
  }
}

# AWS-specific variables
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

# Azure-specific variables
variable "azure_location" {
  description = "Azure location for resources"
  type        = string
  default     = "eastus"
}

# GCP-specific variables
variable "gcp_project" {
  description = "GCP project ID"
  type        = string
  default     = ""
}

variable "gcp_zone" {
  description = "GCP zone for resources"
  type        = string
  default     = "us-central1-a"
}

# Notification Configuration
variable "notification_email" {
  description = "Email address for chaos event notifications"
  type        = string
  default     = ""
}

variable "slack_webhook_url" {
  description = "Slack webhook URL for chaos event notifications"
  type        = string
  default     = ""
}

# Advanced Configuration
variable "chaos_types" {
  description = "Types of chaos to perform (termination, latency, cpu, memory)"
  type        = list(string)
  default     = ["termination"]
}

variable "chaos_probability_override" {
  description = "Override the default chaos probability (0-100)"
  type        = number
  default     = -1
  validation {
    condition     = var.chaos_probability_override == -1 || (var.chaos_probability_override >= 0 && var.chaos_probability_override <= 100)
    error_message = "Chaos probability override must be between 0 and 100, or -1 to use default."
  }
}

variable "excluded_tags" {
  description = "Tags that exclude resources from chaos"
  type        = map(string)
  default     = {}
}

variable "included_tags" {
  description = "Tags that include resources for chaos (must match all)"
  type        = map(string)
  default     = {}
}
