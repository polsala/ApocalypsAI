# Production Chaos Monkey Variables

variable "chaos_notification_topic" {
  description = "SNS topic ARN for chaos notifications"
  type        = string
  default     = "arn:aws:sns:us-east-1:123456789012:production-chaos-notifications"
}

variable "dry_run" {
  description = "Enable dry run mode for safety"
  type        = bool
  default     = true
}
