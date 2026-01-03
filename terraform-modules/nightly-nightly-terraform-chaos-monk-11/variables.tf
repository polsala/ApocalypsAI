# Module configuration
variable "prefix" {
  description = "Prefix for resource names"
  type        = string
  default     = "nightly-chaos"
}

variable "chaos_schedule" {
  description = "CloudWatch Events schedule expression for chaos execution"
  type        = string
  default     = "cron(0 2 * * ? *)"  # Daily at 2 AM UTC
}

variable "resource_types" {
  description = "List of resource types to target for chaos"
  type        = list(string)
  default     = ["ec2"]
  
  validation {
    condition     = length(var.resource_types) > 0
    error_message = "At least one resource type must be specified."
  }
}

variable "exclude_tags" {
  description = "Map of tags to exclude from chaos (resources with these tags will be protected)"
  type        = map(string)
  default     = {}
}

variable "max_chaos_per_run" {
  description = "Maximum number of resources to terminate per execution"
  type        = number
  default     = 3
  
  validation {
    condition     = var.max_chaos_per_run > 0 && var.max_chaos_per_run <= 10
    error_message = "max_chaos_per_run must be between 1 and 10."
  }
}

variable "dry_run" {
  description = "Enable dry run mode (logs what would be terminated without actually doing it)"
  type        = bool
  default     = false
}

variable "enabled" {
  description = "Enable/disable the chaos monkey"
  type        = bool
  default     = true
}

variable "aws_region" {
  description = "AWS region for resource operations"
  type        = string
  default     = "us-east-1"
}

variable "enable_notifications" {
  description = "Enable SNS notifications for chaos events"
  type        = bool
  default     = false
}

variable "notification_email" {
  description = "Email address for chaos notifications (requires enable_notifications = true)"
  type        = string
  default     = ""
  
  validation {
    condition     = var.enable_notifications == false || (var.enable_notifications == true && var.notification_email != "")
    error_message = "notification_email must be provided when enable_notifications is true."
  }
}

variable "log_retention_days" {
  description = "Number of days to retain CloudWatch logs"
  type        = number
  default     = 7
  
  validation {
    condition     = var.log_retention_days in [1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653]
    error_message = "log_retention_days must be one of the supported values: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653."
  }
}

variable "create_dashboard" {
  description = "Create CloudWatch dashboard for chaos monkey metrics"
  type        = bool
  default     = false
}

# Output variables
output "chaos_lambda_arn" {
  description = "ARN of the chaos monkey Lambda function"
  value       = aws_lambda_function.chaos_monkey.arn
}

output "chaos_schedule_rule" {
  description = "CloudWatch Events rule name for chaos schedule"
  value       = aws_cloudwatch_event_rule.chaos_schedule.name
}

output "chaos_notifications_topic" {
  description = "SNS topic ARN for chaos notifications"
  value       = var.enable_notifications ? aws_sns_topic.chaos_notifications[0].arn : ""
  sensitive   = true
}

output "module_enabled" {
  description = "Whether the chaos monkey is enabled"
  value       = var.enabled
}
