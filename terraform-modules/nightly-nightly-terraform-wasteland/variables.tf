#############################################
# Nightly Terraform Wasteland Variables
# Input parameters for survival infrastructure
#############################################

variable "region" {
  description = "AWS region for deploying survival infrastructure"
  type        = string
  default     = "us-east-1"
  
  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-\d+$", var.region))
    error_message = "Region must be a valid AWS region format (e.g., us-east-1, eu-west-1)."
  }
}

variable "environment" {
  description = "Environment name for resource tagging and naming"
  type        = string
  default     = "post-apocalypse"
  
  validation {
    condition     = length(var.environment) > 0 && length(var.environment) <= 50
    error_message = "Environment name must be between 1 and 50 characters."
  }
}

variable "water_tanks" {
  description = "Number of water storage tanks to deploy"
  type        = number
  default     = 1
  
  validation {
    condition     = var.water_tanks >= 0 && var.water_tanks <= 100
    error_message = "Water tanks must be between 0 and 100."
  }
}

variable "food_stores" {
  description = "Number of food storage facilities to deploy"
  type        = number
  default     = 1
  
  validation {
    condition     = var.food_stores >= 0 && var.food_stores <= 100
    error_message = "Food stores must be between 0 and 100."
  }
}

variable "power_generators" {
  description = "Number of backup power generators to deploy"
  type        = number
  default     = 1
  
  validation {
    condition     = var.power_generators >= 0 && var.power_generators <= 50
    error_message = "Power generators must be between 0 and 50."
  }
}

variable "perimeter_fencing" {
  description = "Enable perimeter security fencing"
  type        = bool
  default     = false
}

variable "watch_towers" {
  description = "Number of security watch towers to deploy"
  type        = number
  default     = 0
  
  validation {
    condition     = var.watch_towers >= 0 && var.watch_towers <= 20
    error_message = "Watch towers must be between 0 and 20."
  }
}

variable "radio_towers" {
  description = "Number of emergency communication radio towers to deploy"
  type        = number
  default     = 1
  
  validation {
    condition     = var.radio_towers >= 0 && var.radio_towers <= 10
    error_message = "Radio towers must be between 0 and 10."
  }
}

variable "emergency_frequency" {
  description = "Emergency radio frequency for communication"
  type        = string
  default     = "101.5MHz"
  
  validation {
    condition     = can(regex("^\d{2,3}\.\dMHz$", var.emergency_frequency))
    error_message = "Emergency frequency must be in format like '101.5MHz'."
  }
}

variable "create_monitoring" {
  description = "Enable infrastructure monitoring and alerting"
  type        = bool
  default     = true
}

variable "enable_logging" {
  description = "Enable detailed logging for all resources"
  type        = bool
  default     = true
}

variable "backup_retention_days" {
  description = "Number of days to retain backup data"
  type        = number
  default     = 365
  
  validation {
    condition     = var.backup_retention_days >= 1 && var.backup_retention_days <= 3650
    error_message = "Backup retention must be between 1 and 3650 days."
  }
}

variable "security_level" {
  description = "Security level for the survival compound (1-10)"
  type        = number
  default     = 5
  
  validation {
    condition     = var.security_level >= 1 && var.security_level <= 10
    error_message = "Security level must be between 1 and 10."
  }
}

variable "survival_priority" {
  description = "Priority level for survival resources (HIGH, MEDIUM, LOW)"
  type        = string
  default     = "HIGH"
  
  validation {
    condition     = contains(["HIGH", "MEDIUM", "LOW"], upper(var.survival_priority))
    error_message = "Survival priority must be HIGH, MEDIUM, or LOW."
  }
}

variable "resource_tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "enable_auto_scaling" {
  description = "Enable automatic scaling for critical resources"
  type        = bool
  default     = false
}

variable "maintenance_window" {
  description = "Preferred maintenance window for updates"
  type        = string
  default     = "Sun:02:00-Sun:04:00"
  
  validation {
    condition     = can(regex("^\w{3}:\d{2}:\d{2}-\w{3}:\d{2}:\d{2}$", var.maintenance_window))
    error_message = "Maintenance window must be in format like 'Sun:02:00-Sun:04:00'."
  }
}
