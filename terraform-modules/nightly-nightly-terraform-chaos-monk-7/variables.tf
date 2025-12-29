# Enable/disable the chaos monkey
variable "enabled" {
  description = "Enable/disable the chaos monkey"
  type        = bool
  default     = false
}

# Probability of destroying a resource
variable "destruction_probability" {
  description = "Probability (0.0-1.0) of destroying a resource"
  type        = number
  default     = 0.05
  validation {
    condition     = var.destruction_probability >= 0 && var.destruction_probability <= 1
    error_message = "Destruction probability must be between 0 and 1."
  }
}

# Resource types to target
variable "target_resource_types" {
  description = "Resource types to target for chaos"
  type        = list(string)
  default     = []
}

# Chaos schedule
variable "chaos_schedule" {
  description = "Cron schedule for chaos execution"
  type        = string
  default     = "0 2 * * *"
}

# Safe mode
variable "safe_mode" {
  description = "Log actions without actually destroying resources"
  type        = bool
  default     = true
}

# Maximum resources per run
variable "max_resources_per_run" {
  description = "Maximum number of resources to destroy per chaos run"
  type        = number
  default     = 3
}

# Excluded resources
variable "excluded_resources" {
  description = "Resource IDs to exclude from chaos"
  type        = list(string)
  default     = []
}

# AWS region
variable "aws_region" {
  description = "AWS region for chaos operations"
  type        = string
  default     = "us-east-1"
}

# Output format
variable "output_format" {
  description = "Output format for chaos results (json, text)"
  type        = string
  default     = "json"
}

# Notification email (optional)
variable "notification_email" {
  description = "Email address for chaos execution notifications"
  type        = string
  default     = ""
  validation {
    condition     = var.notification_email == "" || can(regex("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", var.notification_email))
    error_message = "Invalid email format."
  }
}

# SNS topic ARN for notifications (optional)
variable "sns_topic_arn" {
  description = "SNS topic ARN for chaos execution notifications"
  type        = string
  default     = ""
  validation {
    condition     = var.sns_topic_arn == "" || can(regex("^arn:aws:sns:[a-z0-9-]+:\\d{12}:[a-zA-Z0-9-_]+$", var.sns_topic_arn))
    error_message = "Invalid SNS topic ARN format."
  }
}

# CloudWatch log retention
variable "log_retention_days" {
  description = "Number of days to retain CloudWatch logs"
  type        = number
  default     = 30
  validation {
    condition     = var.log_retention_days > 0 && var.log_retention_days <= 2557
    error_message = "Log retention must be between 1 and 2557 days."
  }
}

# Lambda memory size
variable "lambda_memory_size" {
  description = "Memory size for the chaos monkey Lambda function"
  type        = number
  default     = 128
  validation {
    condition     = var.lambda_memory_size >= 128 && var.lambda_memory_size <= 10240
    error_message = "Lambda memory size must be between 128 and 10240 MB."
  }
}

# Lambda timeout
variable "lambda_timeout" {
  description = "Timeout for the chaos monkey Lambda function"
  type        = number
  default     = 300
  validation {
    condition     = var.lambda_timeout > 0 && var.lambda_timeout <= 900
    error_message = "Lambda timeout must be between 1 and 900 seconds."
  }
}
