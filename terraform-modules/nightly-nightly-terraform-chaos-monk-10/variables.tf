# Enable chaos monkey functionality
variable "enabled" {
  description = "Enable chaos monkey functionality - WARNING: This will randomly destroy resources"
  type        = bool
  default     = false
  
  validation {
    condition     = var.enabled == false || var.environment == "development" || var.environment == "staging"
    error_message = "Chaos monkey can only be enabled in development or staging environments."
  }
}

# Environment variable for safety
variable "environment" {
  description = "Current environment (development, staging, production)"
  type        = string
  default     = "development"
}

# Destruction probability
variable "destruction_probability" {
  description = "Probability (0.0-1.0) of destroying a resource during each run"
  type        = number
  default     = 0.05
  
  validation {
    condition     = var.destruction_probability >= 0 && var.destruction_probability <= 1
    error_message = "Destruction probability must be a number between 0 and 1."
  }
}

# Target resources
variable "target_resources" {
  description = "List of resource types to target for chaos (e.g., aws_instance, aws_rds_instance)"
  type        = list(string)
  default     = []
  
  validation {
    condition     = length(var.target_resources) > 0 || var.enabled == false
    error_message = "You must specify target_resources when chaos monkey is enabled."
  }
}

# Excluded resources
variable "excluded_resources" {
  description = "List of specific resources to exclude from chaos (format: resource_type.resource_name)"
  type        = list(string)
  default     = []
}

# Maximum destructions per run
variable "max_destructions_per_run" {
  description = "Maximum number of resources to destroy per Terraform run"
  type        = number
  default     = 3
  
  validation {
    condition     = var.max_destructions_per_run > 0 && var.max_destructions_per_run <= 10
    error_message = "Max destructions per run must be between 1 and 10."
  }
}

# Chaos schedule
variable "chaos_schedule" {
  description = "Schedule for when chaos can occur (e.g., "weekdays", "weekends", "always")"
  type        = string
  default     = "always"
  
  validation {
    condition     = contains(["always", "weekdays", "weekends"], var.chaos_schedule)
    error_message = "Chaos schedule must be one of: always, weekdays, weekends."
  }
}

# Backup before destruction
variable "backup_before_destruction" {
  description = "Create backups before destroying resources (when supported)"
  type        = bool
  default     = true
}

# Notification webhook
variable "notification_webhook" {
  description = "Webhook URL to send chaos events notifications"
  type        = string
  default     = ""
  
  validation {
    condition     = var.notification_webhook == "" || can(regex("^https://", var.notification_webhook))
    error_message = "Notification webhook must be a valid HTTPS URL."
  }
}

# Dry run mode
variable "dry_run" {
  description = "Enable dry run mode - logs what would be destroyed but doesn't actually destroy"
  type        = bool
  default     = false
}

# Resource age filter
variable "min_resource_age_hours" {
  description = "Minimum age (in hours) of resources before they can be targeted by chaos"
  type        = number
  default     = 1
  
  validation {
    condition     = var.min_resource_age_hours >= 0
    error_message = "Minimum resource age must be 0 or greater."
  }
}

# Chaos tags
variable "chaos_tags" {
  description = "Tags that resources must have to be eligible for chaos"
  type        = map(string)
  default     = {}
}

# Excluded regions
variable "excluded_regions" {
  description = "List of regions to exclude from chaos operations"
  type        = list(string)
  default     = []
}

# Chaos duration
variable "chaos_duration_minutes" {
  description = "Maximum duration (in minutes) that chaos can run during each Terraform apply"
  type        = number
  default     = 30
  
  validation {
    condition     = var.chaos_duration_minutes > 0 && var.chaos_duration_minutes <= 120
    error_message = "Chaos duration must be between 1 and 120 minutes."
  }
}
